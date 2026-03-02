#!/usr/bin/env python3
"""
飞书机器人处理器 - 简化版

场景：
用户在飞书群 @OpenHands 机器人说：
  "创建一个用户登录功能，支持 JWT 认证"

机器人自动：
1. 提取任务描述
2. 创建 GitHub Issue
3. Issue 标题：@openhands-agent 任务：创建用户登录功能
4. Issue 正文：任务描述 + 项目规范引用

使用方式：
1. 配置飞书机器人 Webhook
2. 机器人收到 @ 消息时调用此脚本
3. 脚本自动创建 Issue
"""

import os
import json
import logging
from typing import Dict, Any

import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_OWNER = os.getenv('GITHUB_OWNER', 'openhandsRoywnOrg')
GITHUB_REPO = os.getenv('GITHUB_REPO', 'myResume')

# 项目规范引用（简化版）
PROJECT_DOCS = """
## 📚 AI Agent 必读规范

在开始编码前，**必须**阅读以下文档：

1. **[AGENTS.md](../AGENTS.md)** - AI 开发指南（⭐ 最重要）
2. **[ARCHITECTURE_PLAN.md](../ARCHITECTURE_PLAN.md)** - 架构设计
3. **[backend/README.md](../backend/README.md)** - 后端目录结构
4. **[docs/ISSUE_GUIDELINES.md](../docs/ISSUE_GUIDELINES.md)** - Issue 解决指南

### ⚠️ 重要规则
- ✅ 所有新代码必须有单元测试（覆盖率 > 80%）
- ✅ 遵循现有代码风格（类型注解、docstring）
- ✅ 不要修改与任务无关的文件
- ✅ 提交前运行所有测试：`pytest`

### 📁 目录结构规则
```
新模型 → backend/app/models/
新服务 → backend/app/services/
新 API → backend/app/api/v1/
新测试 → backend/tests/unit/
```

@openhands-agent 请开始实现
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_issue_from_message(
    task_description: str,
    creator: str = "Unknown"
) -> Dict[str, Any]:
    """
    从飞书消息创建 GitHub Issue
    
    Args:
        task_description: 任务描述（飞书消息内容）
        creator: 创建人（飞书用户名）
    
    Returns:
        GitHub Issue 数据
    """
    # 清理任务描述
    task_description = task_description.strip()
    
    # 生成 Issue 标题
    # 格式：@openhands-agent 任务：{任务描述}
    if len(task_description) > 50:
        short_desc = task_description[:50] + "..."
    else:
        short_desc = task_description
    
    title = f"@openhands-agent 任务：{short_desc}"
    
    # 构建 Issue 正文
    body = f"""
## 📋 任务描述

{task_description}

---

{PROJECT_DOCS}

---

## ℹ️ 自动化信息

- **创建方式**: 飞书机器人
- **创建人**: {creator}
"""
    
    # 调用 GitHub API
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues"
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    
    data = {
        'title': title,
        'body': body,
        'labels': ['ai-agent', 'from-feishu']
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=30)
    response.raise_for_status()
    
    issue = response.json()
    
    logger.info(f"Issue 创建成功：#{issue['number']} - {title}")
    
    return issue


def handle_feishu_message(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理飞书消息事件
    
    Args:
        event_data: 飞书事件数据
    
    Returns:
        处理结果
    """
    # 飞书事件数据结构（示例）
    # {
    #     "schema": "v2",
    #     "header": {
    #         "message_id": "xxx",
    #         "message_type": "text"
    #     },
    #     "event": {
    #         "message": {
    #             "content": "{\"text\":\"@OpenHands 创建用户登录功能\"}",
    #             "mentions": ["ou_xxxxx"]
    #         },
    #         "sender": {
    #             "name": "张三"
    #         }
    #     }
    # }
    
    try:
        # 提取消息内容
        event = event_data.get('event', {})
        message = event.get('message', {})
        sender = event.get('sender', {})
        
        # 解析消息内容（JSON 格式）
        content_str = message.get('content', '{}')
        content = json.loads(content_str)
        text = content.get('text', '')
        
        # 检查是否 @了机器人
        mentions = message.get('mentions', [])
        if not mentions:
            logger.info("消息未 @机器人，忽略")
            return {'success': False, 'reason': 'not_mentioned'}
        
        # 提取任务描述（去掉 @机器人 部分）
        task_description = text.replace('@OpenHands', '').replace('@openhands', '').strip()
        
        if not task_description:
            logger.warning("任务描述为空")
            return {'success': False, 'reason': 'empty_description'}
        
        # 获取创建人
        creator = sender.get('name', 'Unknown')
        
        # 创建 Issue
        issue = create_issue_from_message(task_description, creator)
        
        return {
            'success': True,
            'issue_number': issue['number'],
            'issue_url': issue['html_url'],
            'title': issue['title']
        }
        
    except Exception as e:
        logger.error(f"处理飞书消息失败：{str(e)}", exc_info=True)
        return {'success': False, 'error': str(e)}


# Flask Web 服务器（用于接收飞书 Webhook）
def create_flask_app():
    """创建 Flask 应用"""
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route('/webhook/feishu', methods=['POST'])
    def feishu_webhook():
        """飞书 Webhook 端点"""
        data = request.json
        logger.info(f"收到飞书 Webhook: {data}")
        
        # 处理消息
        result = handle_feishu_message(data)
        
        if result.get('success'):
            return jsonify({
                'code': 0,
                'msg': 'success',
                'data': result
            })
        else:
            return jsonify({
                'code': 1,
                'msg': result.get('reason', result.get('error', 'unknown error'))
            }), 200  # 飞书要求返回 200
    
    @app.route('/health', methods=['GET'])
    def health():
        """健康检查"""
        return jsonify({'status': 'ok'})
    
    return app


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='飞书机器人处理器')
    parser.add_argument('--port', type=int, default=5000, help='监听端口')
    parser.add_argument('--test', action='store_true', help='测试模式')
    
    args = parser.parse_args()
    
    if args.test:
        # 测试模式
        print("🧪 测试模式：创建测试 Issue")
        
        try:
            issue = create_issue_from_message(
                task_description="创建一个计算两个数之和的函数",
                creator="Test User"
            )
            
            print(f"✅ Issue 创建成功：#{issue['number']}")
            print(f"🔗 URL: {issue['html_url']}")
            
        except Exception as e:
            print(f"❌ 测试失败：{str(e)}")
    
    else:
        # 运行 Flask 服务器
        app = create_flask_app()
        print(f"🚀 飞书机器人服务器启动在端口 {args.port}")
        print(f"Webhook URL: http://localhost:{args.port}/webhook/feishu")
        print("按 Ctrl+C 停止服务器")
        
        app.run(host='0.0.0.0', port=args.port, debug=False)
