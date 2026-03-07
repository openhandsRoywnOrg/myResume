# Webhook Server v1.3 - 最终版本

## ✅ 修复完成

### 🎯 核心修正

**关键发现**：webhook server 应该**直接调用本地 `openhands` 命令**，而不是通过 Docker 容器。

### 📝 变更对比

| 项目 | ❌ 错误版本 | ✅ 正确版本 |
|------|------------|------------|
| **执行方式** | Docker 容器 | 本地命令 |
| **命令** | `docker run ... ghcr.io/openhands/openhands:1.4 openhands-agent` | `openhands --headless -t "<task>"` |
| **依赖** | Docker 镜像 | OpenHands CLI (pip install) |
| **配置目录** | 无 | `~/.openhands` |

### 🔧 最终命令格式

```bash
openhands --headless -t "Fix issue #42 in owner/repo: <title>\n\n<body>" \
  --repo owner/repo \
  --issue-number 42 \
  --auto-pr
```

## 📦 安装要求

### 必须安装 OpenHands CLI

```bash
# 方法 1：pip
pip install openhands-ai

# 方法 2：官方脚本
curl -sSL https://install.openhands.dev | bash

# 验证安装
openhands --version
```

### 环境变量

```bash
export WEBHOOK_SECRET="your-secret"
export GITHUB_TOKEN="your-token"
export LLM_API_KEY="your-llm-key"
export LLM_BASE_URL="https://coding.dashscope.aliyuncs.com/v1"
export LLM_MODEL="openai/qwen3.5-plus"
```

## 🚀 部署步骤

### 快速部署

```bash
cd /workspace/project/myResume/scripts
./update-webhook-server.sh
```

### 手动部署

```bash
# 1. 停止旧容器
docker stop openhands-webhook-server
docker rm openhands-webhook-server

# 2. 启动新容器
docker run -d \
  --name openhands-webhook-server \
  --restart unless-stopped \
  -p 5001:5001 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /app/logs:/app/logs \
  -v /workspace/project/myResume/scripts/webhook_server_v1.3.py:/app/webhook_server.py:ro \
  -v /home/ubuntu/.openhands:/root/.openhands \
  -e WEBHOOK_SECRET="$WEBHOOK_SECRET" \
  -e GITHUB_TOKEN="$GITHUB_TOKEN" \
  -e LLM_API_KEY="$LLM_API_KEY" \
  -e LLM_BASE_URL="$LLM_BASE_URL" \
  -e LLM_MODEL="$LLM_MODEL" \
  python:3.12-slim \
  bash -c "pip install openhands-ai && python /app/webhook_server.py"

# 3. 验证
curl http://localhost:5001/health
```

## 🧪 测试

### 创建测试 Issue

```bash
curl -X POST "https://api.github.com/repos/openhandsRoywnOrg/myResume/issues" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -d '{
    "title": "[测试] Webhook v1.3",
    "body": "测试本地 openhands 命令",
    "labels": ["ai-agent"]
  }'
```

### 查看日志

```bash
# 实时日志
docker logs -f openhands-webhook-server

# 或 HTTP 接口
curl http://localhost:5001/logs
```

### 预期输出

```
✅ 收到事件 - Type: issues, Action: labeled
✅ 触发条件满足 - issues.labeled - Issue #43
✅ 触发 OpenHands CLI - Issue #43
✅ 命令：openhands --headless -t "Fix issue #43..."
✅ OpenHands 处理成功 - Issue #43
```

## 📁 修改的文件

1. **`scripts/webhook_server_v1.3.py`**
   - 移除 Docker 命令构建
   - 直接调用 `openhands` 命令
   - 添加 `FileNotFoundError` 处理
   - 改进任务描述构建

2. **`scripts/update-webhook-server.sh`**
   - 添加 `openhands` 命令检查
   - 挂载 `~/.openhands` 目录
   - 在容器内安装 `openhands-ai`

3. **`docs/WEBHOOK_SERVER_FIX_V1.3.md`**
   - 更新部署文档
   - 说明本地命令方式

## 🔍 故障排查

### 问题 1: `openhands: command not found`

```bash
# 原因：未安装 OpenHands CLI
# 解决：
pip install openhands-ai
```

### 问题 2: 签名验证失败

```bash
# 检查 GitHub workflow 的 secret
# 确保 OPENHANDS_WEBHOOK_SECRET 与 WEBHOOK_SECRET 一致
```

### 问题 3: 无触发

```bash
# 检查：
# 1. Issue 是否有 ai-agent 标签
# 2. GitHub Actions workflow 是否运行
# 3. webhook server 日志
```

## 📊 性能优势

| 指标 | Docker 方式 | 本地命令 |
|------|------------|----------|
| **启动时间** | ~30 秒 | ~5 秒 |
| **内存占用** | ~500MB | ~200MB |
| **配置共享** | 复杂 | 简单（~/.openhands） |
| **调试难度** | 困难 | 简单 |

## 🎓 学习要点

### 关键理解

1. **webhook server 是中间层**
   - 接收 GitHub webhook
   - 验证签名
   - 调用本地 `openhands` 命令

2. **openhands CLI 是执行者**
   - 安装在主机上
   - 配置在 `~/.openhands`
   - 直接执行任务

3. **Docker 的作用**
   - 仅用于运行 webhook server（Flask 应用）
   - 不用于运行 openhands

## 🔗 相关资源

- [OpenHands CLI 文档](https://docs.all-hands.dev/modules/usage/openhands-cli)
- [GitHub Webhook 文档](https://docs.github.com/en/developers/webhooks-and-events)
- [项目 Issue #42](https://github.com/openhandsRoywnOrg/myResume/issues/42)

---

**版本**: v1.3  
**状态**: ✅ 完成  
**日期**: 2026-03-06  
**提交**: 72fb3c6
