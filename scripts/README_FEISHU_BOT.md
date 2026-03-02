# 飞书机器人使用指南

## 🎯 使用场景

**你在飞书群里说**：
```
@OpenHands 创建一个用户登录功能，支持 JWT 认证
```

**机器人自动**：
1. 创建 GitHub Issue
2. 标题：`@openhands-agent 任务：创建用户登录功能`
3. 正文：包含任务描述 + **项目规范引用**
4. 自动添加 `ai-agent` 标签
5. GitHub Actions 自动触发 OpenHands 处理

---

## 🔧 快速开始

### 1. 安装依赖

```bash
cd scripts
pip install requests flask python-dotenv
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
# GitHub 配置
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_OWNER=openhandsRoywnOrg
GITHUB_REPO=myResume
```

### 3. 测试

```bash
python feishu_bot.py --test
```

### 4. 运行服务器

```bash
python feishu_bot.py --port 5000
```

### 5. 配置飞书机器人

在飞书开放平台配置：
- **事件订阅**: 接收消息
- **Webhook URL**: `http://your-server:5000/webhook/feishu`

---

## 📝 飞书消息格式

### 示例 1: 简单任务

**飞书消息**：
```
@OpenHands 添加用户注册功能
```

**生成的 Issue**：
- 标题：`@openhands-agent 任务：添加用户注册功能`
- 正文：包含任务描述 + 规范引用

### 示例 2: 详细任务

**飞书消息**：
```
@OpenHands 实现 JWT 认证系统，要求：
1. 支持 access token 和 refresh token
2. token 过期时间可配置
3. 有完整的单元测试
```

**生成的 Issue**：
- 标题：`@openhands-agent 任务：实现 JWT 认证系统...`
- 正文：完整描述 + 规范引用

---

## 🤖 完整流程

```
飞书群消息
   ↓
@OpenHands 创建用户登录功能
   ↓
飞书机器人 (feishu_bot.py)
   ↓
提取任务描述 + 添加规范引用
   ↓
调用 GitHub API 创建 Issue
   ↓
Issue 自动包含：
- 任务描述
- AGENTS.md 等规范文档引用
- ai-agent 标签
   ↓
GitHub Actions 检测到 ai-agent 标签
   ↓
OpenHands Agent 自动读取规范
   ↓
AI 遵循规范编写代码
   ↓
自动创建 PR
```

---

## 📋 关键代码

### 自动添加规范引用

```python
PROJECT_DOCS = """
## 📚 AI Agent 必读规范

1. **[AGENTS.md](../AGENTS.md)** - AI 开发指南（⭐ 最重要）
2. **[ARCHITECTURE_PLAN.md](../ARCHITECTURE_PLAN.md)** - 架构设计
3. **[backend/README.md](../backend/README.md)** - 后端目录结构
4. **[docs/ISSUE_GUIDELINES.md](../docs/ISSUE_GUIDELINES.md)** - Issue 解决指南

### ⚠️ 重要规则
- ✅ 所有新代码必须有单元测试
- ✅ 遵循现有代码风格
...

@openhands-agent 请开始实现
"""

def create_issue_from_message(task_description, creator):
    body = f"""
## 📋 任务描述

{task_description}

---

{PROJECT_DOCS}  ← 自动添加规范引用
"""
```

---

## 🚨 注意事项

1. **飞书机器人需要配置事件订阅**
   - 订阅 `message` 事件
   - 配置机器人被 @ 时触发

2. **服务器需要公网访问**
   - 使用 ngrok 或云服务器
   - 飞书才能访问 Webhook

3. **GitHub Token 权限**
   - 需要 `repo` 权限
   - 需要 `workflow` 权限

---

## 💡 简化方案对比

### 之前的复杂方案（已删除）
- ❌ 需要飞书表单
- ❌ 需要配置多维表格
- ❌ 需要复杂的字段映射

### 现在的简化方案
- ✅ 直接在群里 @机器人
- ✅ 自动提取消息内容
- ✅ 自动添加规范引用
- ✅ 简单直接

---

## 🔗 参考

- [飞书机器人文档](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN)
- Issue 示例：https://github.com/openhandsRoywnOrg/myResume/issues/6
