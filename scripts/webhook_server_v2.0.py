#!/usr/bin/env python3
"""
GitHub Webhook 服务器 - 触发 OpenHands CLI (Headless 模式)
版本：v2.0 - 基于官方文档修正

支持触发条件：
- Issue 添加标签：ai-agent 或 fix-me
- PR 添加标签：ai-agent
- Issue 评论：包含 @openhands-agent
- PR 审查：包含 @openhands-agent
- PR 审查评论：包含 @openhands-agent

文档参考：
- https://docs.openhands.dev/openhands/usage/cli/command-reference
- https://docs.openhands.dev/openhands/usage/cli/headless
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

# 去重机制（5 分钟窗口）
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


def build_task_description(issue_number: int, repo: str, title: str, body: str) -> str:
    """
    构建任务描述
    
    根据官方文档，task 应该清晰描述需要完成的工作
    """
    task = f"Please fix GitHub issue #{issue_number} in repository {repo}\n\n"
    task += f"Issue Title: {title}\n\n"
    
    if body:
        # 限制 body 长度，避免命令过长
        body_preview = body[:1000] if len(body) > 1000 else body
        task += f"Issue Description:\n{body_preview}\n\n"
    
    task += "Please analyze the issue, implement the necessary code changes, and create a pull request if needed."
    
    return task


def trigger_openhands_headless(task_description: str, issue_number: int) -> tuple[bool, str]:
    """
    触发 OpenHands CLI (Headless 模式)
    
    根据官方文档，正确的命令格式：
    openhands --headless -t "<task>" --exit-without-confirmation
    
    可选：--json 用于结构化输出
    
    Returns:
        (success, message)
    """
    try:
        # ✅ 正确的命令格式（基于官方文档）
        # 注意：不需要传 LLM 和 GitHub token，这些在 ~/.openhands/ 中配置
        cmd = [
            'openhands',
            '--headless',
            '-t', task_description,
            '--exit-without-confirmation'
        ]
        
        # 可选：添加 --json 用于结构化输出（便于解析）
        # cmd.append('--json')
        
        logger.info(f"触发 OpenHands Headless - Issue #{issue_number}")
        logger.info(f"命令：openhands --headless -t \"Please fix GitHub issue #{issue_number}...\"")
        
        # 执行命令
        # 注意：需要继承环境变量（LLM_API_KEY 等可能在环境中）
        env = os.environ.copy()
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1800,  # 30 分钟超时
            env=env
        )
        
        if result.returncode == 0:
            logger.info(f"OpenHands 处理成功 - Issue #{issue_number}")
            # 记录输出（限制长度）
            output = result.stdout[:1000] if result.stdout else "无输出"
            logger.info(f"输出：{output}")
            return True, f"成功处理 Issue #{issue_number}"
        else:
            logger.error(f"OpenHands 处理失败 - Issue #{issue_number}")
            logger.error(f"STDOUT: {result.stdout[:500] if result.stdout else 'None'}")
            logger.error(f"STDERR: {result.stderr[:500] if result.stderr else 'None'}")
            return False, f"处理失败：{result.stderr[:500] if result.stderr else result.stdout[:500]}"
            
    except subprocess.TimeoutExpired:
        logger.error(f"OpenHands 执行超时 - Issue #{issue_number}")
        return False, "执行超时（30 分钟）"
    except FileNotFoundError:
        logger.error(f"openhands 命令未找到 - 请确保已安装 OpenHands CLI")
        logger.error(f"安装方法：pip install openhands-ai")
        return False, "openhands 命令未找到，请先安装 OpenHands CLI (pip install openhands-ai)"
    except Exception as e:
        logger.error(f"执行出错：{str(e)}")
        return False, f"执行错误：{str(e)}"


def should_trigger_issue_event(data: dict) -> bool:
    """检查 Issue 事件是否应该触发"""
    action = data.get('action', '')
    
    # 支持 opened 和 labeled 两种情况
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
    # 触发关键词
    triggers = ['@openhands-agent', '/fix', '/openhands']
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
        'service': 'openhands-webhook-server-v2',
        'version': '2.0 (Headless Mode)'
    }), 200


@app.route('/webhook/github', methods=['POST'])
def webhook():
    """接收 GitHub Webhook"""
    signature = request.headers.get('X-Hub-Signature-256')
    delivery = request.headers.get('X-GitHub-Delivery')
    event = request.headers.get('X-GitHub-Event')
    
    # 检查重复事件
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
    
    # 判断是否满足触发条件
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
    
    # 提取 Issue 信息
    issue_number = None
    issue_title = ''
    issue_body = ''
    repo = ''
    
    if 'issue' in data:
        issue_number = data['issue'].get('number')
        issue_title = data['issue'].get('title', '')
        issue_body = data['issue'].get('body', '') or ''
        repo = data['repository'].get('full_name', '')
    elif 'pull_request' in data:
        issue_number = data['pull_request'].get('number')
        issue_title = data['pull_request'].get('title', '')
        issue_body = data['pull_request'].get('body', '') or ''
        repo = data['repository'].get('full_name', '')
    
    if not issue_number:
        logger.error("无法提取 Issue 号码")
        return jsonify({'error': 'Cannot extract issue number'}), 400
    
    logger.info(f"触发条件满足 - {event_type} - Issue #{issue_number}")
    
    # 构建任务描述
    task_description = build_task_description(issue_number, repo, issue_title, issue_body)
    logger.info(f"任务描述：{task_description[:200]}...")
    
    # 异步执行 OpenHands
    def run_async():
        success, message = trigger_openhands_headless(task_description, issue_number)
        logger.info(f"异步执行结果 - 成功：{success}, 消息：{message}")
        
        # 可选：在 GitHub Issue 上添加评论
        # if success:
        #     add_github_comment(repo, issue_number, "✅ OpenHands 已完成处理")
        # else:
        #     add_github_comment(repo, issue_number, f"❌ OpenHands 处理失败：{message}")
    
    thread = threading.Thread(target=run_async)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'status': 'accepted',
        'event_type': event_type,
        'issue_number': issue_number,
        'message': 'OpenHands 正在处理中 (Headless Mode)',
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
    logger.info("=" * 60)
    logger.info("OpenHands Webhook 服务器启动 v2.0")
    logger.info("模式：Headless (无 UI)")
    logger.info("参考文档:")
    logger.info("  - https://docs.openhands.dev/openhands/usage/cli/command-reference")
    logger.info("  - https://docs.openhands.dev/openhands/usage/cli/headless")
    logger.info(f"监听端口：5001")
    logger.info(f"Webhook 路径：/webhook/github")
    logger.info(f"健康检查：/health")
    logger.info(f"日志文件：{log_file}")
    logger.info("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
