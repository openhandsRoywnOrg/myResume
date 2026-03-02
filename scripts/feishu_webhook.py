#!/usr/bin/env python3
"""
飞书 Webhook 处理器 - 将飞书表单转换为 GitHub Issue

这个脚本接收飞书自动化发送的 Webhook，
解析表单数据，创建包含规范引用的 GitHub Issue。

使用场景：
1. 用户在飞书填写"创建 Issue"表单
2. 飞书自动化发送 Webhook 到这个脚本
3. 脚本解析数据并创建 GitHub Issue
4. Issue 自动包含项目规范引用
5. OpenHands Agent 自动处理 Issue
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# GitHub 配置
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_OWNER = os.getenv('GITHUB_OWNER', 'openhandsRoywnOrg')
GITHUB_REPO = os.getenv('GITHUB_REPO', 'myResume')

# 项目规范文档引用
PROJECT_DOCS = """
## 📚 AI Agent 必读规范

在开始编码前，**必须**阅读以下文档：

### 核心规范
1. **[AGENTS.md](../AGENTS.md)** - AI 开发指南（⭐ 最重要）
   - 代码质量要求
   - 文件组织规则
   - Issue 解决流程
   - 常见错误示例

2. **[ARCHITECTURE_PLAN.md](../ARCHITECTURE_PLAN.md)** - 架构设计
   - 项目目标架构
   - 目录结构说明
   - 分层设计原则

3. **[backend/README.md](../backend/README.md)** - 后端目录结构
   - 模块职责说明
   - 添加新功能的流程

4. **[docs/ISSUE_GUIDELINES.md](../docs/ISSUE_GUIDELINES.md)** - Issue 解决指南
   - 7 步解决流程
   - 代码规范示例
   - 测试编写指南

### ⚠️ 重要规则

- ✅ **所有新代码必须有单元测试**（覆盖率 > 80%）
- ✅ **遵循现有代码风格**（类型注解、docstring）
- ✅ **不要修改与任务无关的文件**
- ✅ **提交前运行所有测试**：`pytest`
- ✅ **代码必须通过 flake8 和 mypy 检查**

### 📁 目录结构规则

```
新模型 → backend/app/models/
新服务 → backend/app/services/
新 API → backend/app/api/v1/
新钩子 → backend/app/hooks/
新工具 → backend/app/utils/
新测试 → backend/tests/unit/ 或 backend/tests/integration/
```
"""


class FeishuWebhookHandler(BaseHTTPRequestHandler):
    """飞书 Webhook 请求处理器"""
    
    def do_POST(self):
        """处理 POST 请求"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            # 解析 JSON 数据
            data = json.loads(body)
            
            # 记录日志
            logger.info(f"收到飞书 Webhook: {data.get('title', 'Unknown')}")
            
            # 处理飞书数据
            issue_data = self.parse_feishu_data(data)
            
            # 创建 GitHub Issue
            issue = self.create_github_issue(issue_data)
            
            # 返回成功响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                'success': True,
                'issue_number': issue.get('number'),
                'issue_url': issue.get('html_url')
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
            logger.info(f"Issue 创建成功：#{issue.get('number')}")
            
        except Exception as e:
            logger.error(f"处理 Webhook 失败：{str(e)}", exc_info=True)
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                'success': False,
                'error': str(e)
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def parse_feishu_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析飞书表单数据
        
        Args:
            data: 飞书 Webhook 数据
            
        Returns:
            GitHub Issue 数据字典
        """
        # 飞书表单字段映射（根据实际表单调整）
        # 示例数据结构：
        # {
        #     "title": "实现用户登录功能",
        #     "task_description": "需要实现用户登录...",
        #     "requirements": "- 支持用户名密码登录\n- 支持 JWT 认证",
        #     "acceptance": "- [ ] 可以正常登录\n- [ ] 有单元测试",
        #     "complexity": "中等"
        # }
        
        title = data.get('title', '')
        if not title.startswith('[AI Task]:'):
            title = f"[AI Task]: {title}"
        
        # 构建 Issue 正文
        body = self.build_issue_body(data)
        
        # 确定标签
        labels = ['ai-agent', 'automated', 'from-feishu']
        
        # 根据复杂度添加标签
        complexity = data.get('complexity', '')
        if '简单' in complexity:
            labels.append('complexity:low')
        elif '中等' in complexity:
            labels.append('complexity:medium')
        elif '复杂' in complexity:
            labels.append('complexity:high')
        
        return {
            'title': title,
            'body': body,
            'labels': labels
        }
    
    def build_issue_body(self, data: Dict[str, Any]) -> str:
        """
        构建 Issue 正文（包含规范引用）
        
        Args:
            data: 飞书表单数据
            
        Returns:
            格式化的 Issue 正文
        """
        # 提取表单字段
        task_description = data.get('task_description', '无描述')
        requirements = data.get('requirements', '无具体要求')
        acceptance = data.get('acceptance', '无验收标准')
        hints = data.get('hints', '')
        constraints = data.get('constraints', '')
        
        # 构建正文
        body = f"""
{PROJECT_DOCS}

---

## 📋 任务信息

### 描述
{task_description}

### 要求
{requirements}

### 验收标准
{acceptance}

"""
        
        # 添加可选部分
        if hints:
            body += f"""
### 💡 实现提示
{hints}

"""
        
        if constraints:
            body += f"""
### ⚠️ 约束条件
{constraints}

"""
        
        # 添加自动创建说明
        body += f"""
---

## 🤖 自动化信息

- **创建方式**: 飞书自动化
- **创建时间**: {data.get('created_at', 'Unknown')}
- **创建人**: {data.get('creator', 'Unknown')}

@openhands-agent 请开始实现
"""
        
        return body
    
    def create_github_issue(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用 GitHub API 创建 Issue
        
        Args:
            issue_data: Issue 数据
            
        Returns:
            GitHub API 返回的 Issue 数据
            
        Raises:
            requests.exceptions.RequestException: API 调用失败
        """
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues"
        
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Feishu-Webhook-Handler'
        }
        
        response = requests.post(url, json=issue_data, headers=headers, timeout=30)
        response.raise_for_status()
        
        return response.json()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        logger.info("%s - %s", self.address_string(), format % args)


def run_server(port: int = 8080):
    """
    运行 Webhook 服务器
    
    Args:
        port: 监听端口
    """
    server_address = ('', port)
    httpd = HTTPServer(server_address, FeishuWebhookHandler)
    
    logger.info(f"飞书 Webhook 服务器启动在端口 {port}")
    logger.info(f"Webhook URL: http://localhost:{port}/webhook")
    logger.info("按 Ctrl+C 停止服务器")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("服务器停止")
        httpd.shutdown()


def create_issue_from_feishu(
    title: str,
    task_description: str,
    requirements: str,
    acceptance: str,
    complexity: str = '中等',
    hints: str = '',
    constraints: str = '',
    creator: str = 'Unknown'
) -> Dict[str, Any]:
    """
    直接从飞书数据创建 Issue（用于命令行或脚本调用）
    
    Args:
        title: 任务标题
        task_description: 任务描述
        requirements: 要求
        acceptance: 验收标准
        complexity: 复杂度
        hints: 实现提示
        constraints: 约束条件
        creator: 创建人
        
    Returns:
        GitHub API 返回的 Issue 数据
    """
    # 构建飞书数据格式
    feishu_data = {
        'title': title,
        'task_description': task_description,
        'requirements': requirements,
        'acceptance': acceptance,
        'complexity': complexity,
        'hints': hints,
        'constraints': constraints,
        'creator': creator,
        'created_at': json.dumps({'now': True})  # 简化处理
    }
    
    # 解析数据
    handler = FeishuWebhookHandler(None, None, None)
    issue_data = handler.parse_feishu_data(feishu_data)
    
    # 创建 Issue
    issue = handler.create_github_issue(issue_data)
    
    return issue


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='飞书 Webhook 处理器')
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='监听端口 (默认：8080)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='运行测试模式'
    )
    
    args = parser.parse_args()
    
    if args.test:
        # 测试模式：创建一个测试 Issue
        print("🧪 测试模式：创建测试 Issue")
        
        try:
            issue = create_issue_from_feishu(
                title='测试任务：创建一个简单的函数',
                task_description='创建一个计算两个数之和的函数',
                requirements='- 函数必须有类型注解\n- 函数必须有 docstring',
                acceptance='- [ ] 函数正常工作\n- [ ] 有单元测试\n- [ ] 测试通过',
                complexity='简单',
                creator='Test User'
            )
            
            print(f"✅ Issue 创建成功：#{issue['number']}")
            print(f"🔗 URL: {issue['html_url']}")
            
        except Exception as e:
            print(f"❌ 测试失败：{str(e)}")
    else:
        # 运行服务器
        run_server(args.port)
