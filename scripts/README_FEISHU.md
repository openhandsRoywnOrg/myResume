# 飞书集成指南

## 📋 概述

本指南介绍如何配置飞书自动化，将飞书表单转换为 GitHub Issue，并自动触发 OpenHands Agent 处理。

## 🏗️ 架构

```
┌─────────────┐
│  飞书表单   │
│  填写任务   │
└──────┬──────┘
       │
       │ Webhook
       ▼
┌─────────────────────────┐
│ feishu_webhook.py       │
│ - 解析飞书数据          │
│ - 添加规范引用          │
│ - 调用 GitHub API       │
└──────┬──────────────────┘
       │
       │ GitHub API
       ▼
┌─────────────────────────┐
│ GitHub Issue            │
│ - 包含规范引用          │
│ - ai-agent 标签         │
│ - @openhands-agent      │
└──────┬──────────────────┘
       │
       │ GitHub Actions
       ▼
┌─────────────────────────┐
│ OpenHands Agent         │
│ - 读取规范文档          │
│ - 实现功能              │
│ - 创建 PR               │
└─────────────────────────┘
```

## 🔧 配置步骤

### 步骤 1: 准备环境

#### 1.1 安装依赖

```bash
cd scripts
pip install requests python-dotenv
```

#### 1.2 配置环境变量

创建 `.env` 文件：

```bash
# GitHub 配置
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_OWNER=openhandsRoywnOrg
GITHUB_REPO=myResume

# 服务器配置
WEBHOOK_PORT=8080
```

**获取 GitHub Token**：
1. 访问 https://github.com/settings/tokens
2. 生成新 token
3. 选择 scopes: `repo`, `workflow`
4. 复制 token 到 `.env`

### 步骤 2: 部署 Webhook 服务器

#### 选项 A: 本地开发

```bash
# 运行服务器
python feishu_webhook.py --port 8080

# 测试模式
python feishu_webhook.py --test
```

#### 选项 B: 云服务器部署

使用 ngrok 暴露本地服务：

```bash
# 安装 ngrok
# macOS
brew install ngrok

# 启动 ngrok
ngrok http 8080
```

记录 ngrok 提供的 URL，例如：`https://abc123.ngrok.io`

#### 选项 C: 云函数部署

使用 AWS Lambda / 阿里云函数计算：

```python
# lambda_function.py
from feishu_webhook import FeishuWebhookHandler
import json

def lambda_handler(event, context):
    handler = FeishuWebhookHandler(None, None, None)
    
    # 解析请求
    body = json.loads(event['body'])
    issue_data = handler.parse_feishu_data(body)
    issue = handler.create_github_issue(issue_data)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'success': True,
            'issue_number': issue['number']
        })
    }
```

### 步骤 3: 配置飞书自动化

#### 3.1 创建飞书表单

在飞书多维表格中创建表单，包含以下字段：

| 字段名 | 字段类型 | 必填 | 说明 |
|--------|----------|------|------|
| 任务标题 | 文本 | ✅ | Issue 标题 |
| 任务描述 | 多行文本 | ✅ | 详细描述 |
| 具体要求 | 多行文本 | ✅ | 功能要求列表 |
| 验收标准 | 多行文本 | ✅ | 如何判断完成 |
| 复杂度 | 单选 | ✅ | 简单/中等/复杂 |
| 实现提示 | 多行文本 | ❌ | 给 AI 的建议 |
| 约束条件 | 多行文本 | ❌ | 实现限制 |

#### 3.2 配置飞书自动化

1. 进入飞书多维表格
2. 点击"自动化" → "创建自动化"
3. 配置触发条件：
   - **触发事件**: 当记录创建时
   - **筛选条件**: 表单名称 = "创建 Issue"

4. 添加动作：
   - **动作类型**: 发送 Webhook
   - **URL**: `https://your-server.com/webhook` (ngrok 地址或云服务器地址)
   - **请求方法**: POST
   - **请求头**:
     ```
     Content-Type: application/json
     ```
   - **请求体**（JSON）:
     ```json
     {
       "title": "{{任务标题}}",
       "task_description": "{{任务描述}}",
       "requirements": "{{具体要求}}",
       "acceptance": "{{验收标准}}",
       "complexity": "{{复杂度}}",
       "hints": "{{实现提示}}",
       "constraints": "{{约束条件}}",
       "creator": "{{创建人}}",
       "created_at": "{{创建时间}}"
     }
     ```

5. 测试自动化
6. 启用自动化

### 步骤 4: 测试完整流程

#### 4.1 测试 Webhook

```bash
# 使用 curl 测试
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "title": "测试任务",
    "task_description": "测试描述",
    "requirements": "- 要求 1\n- 要求 2",
    "acceptance": "- [ ] 测试 1\n- [ ] 测试 2",
    "complexity": "简单"
  }'
```

预期响应：
```json
{
  "success": true,
  "issue_number": 123,
  "issue_url": "https://github.com/.../issues/123"
}
```

#### 4.2 测试飞书表单

1. 在飞书填写表单
2. 提交表单
3. 检查 GitHub Issue 是否创建
4. 检查 Issue 是否包含：
   - ✅ 规范引用
   - ✅ ai-agent 标签
   - ✅ 任务信息
   - ✅ @openhands-agent

#### 4.3 测试 OpenHands 自动触发

1. 确认 Issue 有 `ai-agent` 标签
2. 检查 GitHub Actions 是否触发
3. 查看 Actions 日志
4. 等待 AI 创建 PR
5. Review PR

## 📝 使用示例

### 示例 1: 创建简单任务

**飞书表单填写**：

```
任务标题：添加用户注册功能
任务描述：需要实现用户注册功能，支持邮箱注册
具体要求：
- 支持邮箱和密码注册
- 密码需要加密存储
- 发送验证邮件
验收标准：
- [ ] 可以正常注册
- [ ] 密码加密存储
- [ ] 有单元测试
- [ ] 测试覆盖率 > 80%
复杂度：中等
```

**生成的 GitHub Issue**：

```markdown
## 📚 AI Agent 必读规范

[自动包含规范引用...]

---

## 📋 任务信息

### 描述
需要实现用户注册功能，支持邮箱注册

### 要求
- 支持邮箱和密码注册
- 密码需要加密存储
- 发送验证邮件

### 验收标准
- [ ] 可以正常注册
- [ ] 密码加密存储
- [ ] 有单元测试
- [ ] 测试覆盖率 > 80%

@openhands-agent 请开始实现
```

### 示例 2: 创建复杂任务

**飞书表单填写**：

```
任务标题：实现 AI 模拟面试功能
任务描述：集成 LLM API，实现 AI 模拟面试
具体要求：
- 支持选择面试类别
- AI 根据类别提问
- 支持多轮对话
- 提供评分和反馈
验收标准：
- [ ] 可以选择面试类别
- [ ] AI 正常提问
- [ ] 支持 5 轮以上对话
- [ ] 提供评分和反馈
- [ ] 有完整的测试
复杂度：复杂
实现提示：
- 参考现有的 LLM 集成代码
- 使用状态管理对话流程
约束条件：
- 不能修改现有的 API 结构
- 必须使用现有的认证系统
```

## 🚨 故障排查

### 问题 1: Webhook 不响应

**检查**：
1. 服务器是否运行
2. 端口是否正确
3. 防火墙设置
4. ngrok 是否过期

**解决**：
```bash
# 检查服务器
ps aux | grep feishu_webhook

# 重启服务器
python feishu_webhook.py --port 8080
```

### 问题 2: Issue 创建失败

**检查**：
1. GitHub Token 是否有效
2. Token 权限是否足够
3. 网络连接

**解决**：
```bash
# 测试 GitHub API
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/user
```

### 问题 3: 规范引用未显示

**检查**：
1. PROJECT_DOCS 变量是否正确
2. build_issue_body 方法是否调用

**解决**：
查看日志：
```bash
tail -f openhands_agent.log
```

### 问题 4: OpenHands 未自动触发

**检查**：
1. Issue 是否有 `ai-agent` 标签
2. GitHub Actions 是否启用
3. 工作流配置是否正确

**解决**：
```bash
# 手动触发工作流
gh workflow run openhands-auto.yml -f issue_number=123
```

## 🔐 安全建议

### 1. 保护 Webhook

添加签名验证：

```python
def verify_signature(self, payload, signature):
    """验证飞书签名"""
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

### 2. 限制访问

使用 IP 白名单：

```python
ALLOWED_IPS = ['feishu-ip-1', 'feishu-ip-2']

def do_POST(self):
    if self.client_address[0] not in ALLOWED_IPS:
        self.send_response(403)
        return
```

### 3. 使用 HTTPS

生产环境必须使用 HTTPS：

```bash
# 使用 Let's Encrypt
certbot --nginx -d your-domain.com
```

## 📊 监控和日志

### 添加监控

```python
import prometheus_client

# 定义指标
ISSUE_CREATED = prometheus_client.Counter(
    'issues_created_total',
    'Total issues created'
)

WEBHOOK_ERRORS = prometheus_client.Counter(
    'webhook_errors_total',
    'Total webhook errors'
)

# 在创建 Issue 时记录
ISSUE_CREATED.inc()
```

### 查看日志

```bash
# 实时查看日志
tail -f openhands_agent.log

# 搜索错误
grep ERROR openhands_agent.log

# 统计 Issue 数量
grep "Issue 创建成功" openhands_agent.log | wc -l
```

## 📚 参考资源

- [飞书自动化文档](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN)
- [GitHub API 文档](https://docs.github.com/en/rest/issues)
- [OpenHands 文档](https://docs.openhands.dev/)

---

**最后更新**: 2026-03-01
**版本**: 0.1.0
