#!/usr/bin/env python3
"""
GitHub Webhook 服务器 - 触发 OpenHands CLI
修复版本：v1.3 - 使用 openhands --headless -t 命令
"""

from flask import Flask, request, jsonify
import subprocess
import os
import hmac
import hashlib
import logging
import threading
import json
from datetime import datetime, timedelta
from typing import Optional

app = Flask(__name__)

# ==================== 配置 ====================
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', '2d52d08e4ee7a0bdc559ea6274411da54df57ced')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
LLM_API_KEY = os.environ.get('LLM_API_KEY')
LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://coding.dashscope.aliyuncs.com/v1')
LLM_MODEL = os.environ.get('LLM_MODEL', 'openai/qwen3.5-plus')

# 日志配置
log_file = '/app/logs/webhook.log'
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 去重机制
processed_events = {}

def is_duplicate_event(delivery_id: str) -> bool:
    """检查是否是重复事件"""
    if not delivery_id:
        return False
    
    now = datetime.utcnow()
    cutoff = now - timedelta(minutes=5)
    
    # 清理过期记录
    processed_events_copy = dict(processed_events)
    for k, v in processed_events_copy.items():
        if v < cutoff:
            del processed_events[k]
    
    if delivery_id in processed_events:
        return True
    
    processed_events[delivery_id] = now
    return False


def verify_signature(payload: bytes, signature: str) -> bool:
    """验证 GitHub Webhook 签名"""
    if not signature:
        logger.warning("签名为空")
        return False
    
    expected = 'sha256=' + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    result = hmac.compare_digest(expected, signature)
    if not result:
        logger.warning(f"签名不匹配")
    return result


def trigger_openhands_cli(event_type: str, event_data: dict) -> tuple[bool, str]:
    """
    触发 OpenHands CLI
    
    使用命令：openhands --headless -t "<task>"
    
    Returns:
        (success, message)
    """
    try:
        # 提取 Issue 号码
        issue_number = None
        if 'issue' in event_data:
            issue_number = event_data['issue'].get('number')
        elif 'pull_request' in event_data:
            issue_number = event_data['pull_request'].get('number')
        
        if not issue_number:
            return False, "无法提取 Issue 号码"
        
        repo = event_data.get('repository', {}).get('full_name', 'openhandsRoywnOrg/myResume')
        issue_title = event_data.get('issue', {}).get('title', 'No title')
        issue_body = event_data.get('issue', {}).get('body', 'No description')
        
        # ✅ 构建任务描述
        task_description = f"Fix issue #{issue_number} in {repo}: {issue_title}\n\n{issue_body[:500] if issue_body else 'No description'}"
        
        # ✅ 修复：直接执行本地 openhands 命令（不是 Docker）
        # 命令格式：openhands --headless -t "<task>"
        cmd = [
            'openhands',
            '--headless',
            '-t', task_description,
            '--repo', repo,
            '--issue-number', str(issue_number),
            '--auto-pr'
        ]
        
        logger.info(f"触发 OpenHands CLI - Issue #{issue_number} - Repo: {repo}")
        logger.info(f"命令：{' '.join(cmd)}")
        
        # 执行命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1800,  # 30 分钟超时
            env={**os.environ}  # 继承当前环境变量
        )
        
        if result.returncode == 0:
            logger.info(f"OpenHands 处理成功 - Issue #{issue_number}")
            # 记录输出（限制长度）
            output = result.stdout[:1000] if result.stdout else "无输出"
            logger.info(f"输出：{output}")
            return True, f"成功处理 Issue #{issue_number}"
        else:
            logger.error(f"OpenHands 处理失败 - Issue #{issue_number}: {result.stderr}")
            return False, f"处理失败：{result.stderr[:500]}"
            
    except subprocess.TimeoutExpired:
        logger.error(f"OpenHands 执行超时 - Issue #{issue_number}")
        return False, "执行超时（30 分钟）"
    except FileNotFoundError:
        logger.error(f"openhands 命令未找到 - 请确保已安装 OpenHands CLI")
        return False, "openhands 命令未找到，请先安装 OpenHands CLI"
    except Exception as e:
        logger.error(f"执行出错：{str(e)}")
        return False, f"执行错误：{str(e)}"


def should_trigger_issue_event(data: dict) -> bool:
    """检查 Issue 事件是否应该触发"""
    action = data.get('action', '')
    
    # ✅ 支持 opened 和 labeled 两种情况
    if action not in ['opened', 'labeled']:
        return False
    
    labels = [l['name'] for l in data['issue'].get('labels', [])]
    return 'ai-agent' in labels or 'fix-me' in labels


def should_trigger_pr_event(data: dict) -> bool:
    """检查 PR 事件是否应该触发"""
    action = data.get('action', '')
    if action not in ['opened', 'labeled']:
        return False
    
    labels = [l['name'] for l in data['pull_request'].get('labels', [])]
    return 'ai-agent' in labels


def should_trigger_comment_event(data: dict) -> bool:
    """检查评论事件是否应该触发"""
    action = data.get('action', '')
    if action != 'created':
        return False
    
    comment = data.get('comment', {}).get('body', '')
    # ✅ 添加更多触发关键词
    triggers = ['@openhands-agent', '/fix', '/openhands', '请处理']
    return any(trigger in comment for trigger in triggers)


def should_trigger_review_event(data: dict) -> bool:
    """检查审查事件是否应该触发"""
    if data.get('action') == 'submitted':
        review = data.get('review', {}).get('body', '')
        return '@openhands-agent' in review if review else False
    
    return False


def should_trigger_review_comment_event(data: dict) -> bool:
    """检查审查评论事件是否应该触发"""
    if data.get('action') == 'created':
        comment = data.get('comment', {}).get('body', '')
        return '@openhands-agent' in comment if comment else False
    
    return False


# ==================== 路由 ====================
@app.route('/health', methods=['GET'])
def health():
    """健康检查端点"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'openhands-webhook-server'
    }), 200


@app.route('/webhook/github', methods=['POST'])
def webhook():
    """接收 GitHub Webhook"""
    signature = request.headers.get('X-Hub-Signature-256')
    delivery = request.headers.get('X-GitHub-Delivery')
    event = request.headers.get('X-GitHub-Event')
    
    # ✅ 检查重复事件
    if is_duplicate_event(delivery):
        logger.info(f"重复事件，忽略 - Delivery: {delivery}")
        return jsonify({'status': 'duplicate'}), 200
    
    payload = request.get_data()
    content_type = request.headers.get('Content-Type', '')
    
    if not verify_signature(payload, signature):
        logger.warning(f"签名验证失败 - IP: {request.remote_addr}")
        return jsonify({'error': 'Invalid signature'}), 401
    
    try:
        if 'application/json' in content_type:
            data = request.json
        else:
            data = json.loads(payload.decode('utf-8'))
    except Exception as e:
        logger.error(f"解析 JSON 失败：{e}")
        return jsonify({'error': 'Invalid JSON'}), 400
    
    logger.info(f"收到事件 - Type: {event}, Delivery: {delivery}, Action: {data.get('action')}")
    
    should_trigger = False
    event_type = ''
    
    if event == 'issues':
        if should_trigger_issue_event(data):
            should_trigger = True
            event_type = 'issues.labeled'
    
    elif event == 'pull_request':
        if should_trigger_pr_event(data):
            should_trigger = True
            event_type = 'pull_request.labeled'
    
    elif event == 'issue_comment':
        if should_trigger_comment_event(data):
            should_trigger = True
            event_type = 'issue_comment.created'
    
    elif event == 'pull_request_review':
        if should_trigger_review_event(data):
            should_trigger = True
            event_type = 'pull_request_review.submitted'
    
    elif event == 'pull_request_review_comment':
        if should_trigger_review_comment_event(data):
            should_trigger = True
            event_type = 'pull_request_review_comment.created'
    
    if not should_trigger:
        logger.info(f"事件不满足触发条件 - {event}")
        return jsonify({
            'status': 'ignored',
            'reason': 'Event does not match trigger conditions'
        }), 200
    
    issue_number = None
    if 'issue' in data:
        issue_number = data['issue'].get('number')
    elif 'pull_request' in data:
        issue_number = data['pull_request'].get('number')
    
    logger.info(f"触发条件满足 - {event_type} - Issue #{issue_number}")
    
    def run_async():
        success, message = trigger_openhands_cli(event_type, data)
        logger.info(f"异步执行结果 - 成功：{success}, 消息：{message}")
    
    thread = threading.Thread(target=run_async)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'status': 'accepted',
        'event_type': event_type,
        'issue_number': issue_number,
        'message': 'OpenHands 正在处理中',
        'timestamp': datetime.utcnow().isoformat()
    }), 202


@app.route('/logs', methods=['GET'])
def get_logs():
    """查看最近的日志"""
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            last_lines = lines[-100:] if len(lines) > 100 else lines
            return jsonify({
                'logs': ''.join(last_lines),
                'total_lines': len(lines)
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== 主程序 ====================
if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("OpenHands Webhook 服务器启动 v1.3")
    logger.info(f"命令模式：openhands --headless -t")
    logger.info(f"监听端口：5001")
    logger.info("=" * 50)
    
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
