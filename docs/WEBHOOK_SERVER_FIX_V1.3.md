# Webhook 服务器修复 - v1.3

## 📋 修复内容

### 主要变更

1. **✅ 更新 OpenHands 启动命令**
   - 旧命令：`docker run ... ghcr.io/openhands/openhands:1.4 openhands-agent --issue-number 42 --auto-pr`
   - **新命令**：`openhands --headless -t "<task>" --repo <repo> --issue-number 42 --auto-pr`
   - **关键**：直接执行本地 `openhands` 命令，不再使用 Docker

2. **✅ 改进任务描述构建**
   - 现在会提取 Issue 标题和描述
   - 构建更详细的任务描述传递给 OpenHands
   - 格式：`Fix issue #42 in owner/repo: <title>\n\n<body>`

3. **✅ 添加 FileNotFoundError 处理**
   - 如果 `openhands` 命令未找到，会返回友好的错误信息
   - 提示用户安装 OpenHands CLI

4. **✅ 保留所有之前的修复**
   - 支持 Issue 创建时带标签（`opened` 事件）
   - 支持 PR 创建时带标签
   - 评论触发关键词扩展
   - 事件去重机制
   - 签名验证日志

## 🚀 部署方法

### 前置要求

**必须安装 OpenHands CLI**：

```bash
# 方法 1：使用 pip
pip install openhands-ai

# 方法 2：使用官方安装脚本
curl -sSL https://install.openhands.dev | bash

# 验证安装
openhands --version
```

### 方法 1：使用自动部署脚本（推荐）

```bash
# 1. 设置环境变量
export WEBHOOK_SECRET="your-webhook-secret"
export GITHUB_TOKEN="your-github-token"
export LLM_API_KEY="your-llm-api-key"
export LLM_BASE_URL="https://coding.dashscope.aliyuncs.com/v1"
export LLM_MODEL="openai/qwen3.5-plus"

# 2. 运行部署脚本
cd /workspace/project/myResume/scripts
chmod +x update-webhook-server.sh
./update-webhook-server.sh
```

### 方法 2：手动部署

```bash
# 1. 停止旧容器
docker stop openhands-webhook-server
docker rm openhands-webhook-server

# 2. 创建日志目录
sudo mkdir -p /app/logs
sudo chmod 777 /app/logs

# 3. 启动新容器
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
  -e WORKSPACE_PATH="/workspace" \
  python:3.12-slim \
  bash -c "pip install openhands-ai && python /app/webhook_server.py"

# 4. 验证
curl http://localhost:5001/health
```

## 📝 命令格式说明

### 新的命令结构

```bash
openhands --headless -t "<task description>" \
  --repo <repository> \
  --issue-number <number> \
  --auto-pr
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--headless` | 无头模式（无 GUI） | 必需 |
| `-t` | 任务描述 | `"Fix issue #42: Bug in login"` |
| `--repo` | 仓库名称 | `openhandsRoywnOrg/myResume` |
| `--issue-number` | Issue 编号 | `42` |
| `--auto-pr` | 自动创建 PR | 可选 |

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `GITHUB_TOKEN` | GitHub API Token | 必需 |
| `LLM_API_KEY` | LLM API Key | 必需 |
| `LLM_BASE_URL` | LLM API 基础 URL | `https://coding.dashscope.aliyuncs.com/v1` |
| `LLM_MODEL` | LLM 模型名称 | `openai/qwen3.5-plus` |
| `WEBHOOK_SECRET` | Webhook 签名密钥 | 必需 |
| `WORKSPACE_PATH` | 工作目录路径 | `/workspace` |

## 🧪 测试方法

### 1. 创建测试 Issue

```bash
curl -X POST "https://api.github.com/repos/openhandsRoywnOrg/myResume/issues" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{
    "title": "[测试] Webhook v1.3 测试",
    "body": "测试新的 openhands --headless -t 命令",
    "labels": ["ai-agent"]
  }'
```

### 2. 查看日志

```bash
# 实时查看日志
docker logs -f openhands-webhook-server

# 或者通过 HTTP 接口
curl http://localhost:5001/logs
```

### 3. 验证触发

访问 GitHub Actions 查看 workflow 运行：
https://github.com/openhandsRoywnOrg/myResume/actions

## 📊 预期日志输出

成功的日志应该显示：

```
2026-03-06 XX:XX:XX - __main__ - INFO - 收到事件 - Type: issues, Delivery: xxx, Action: labeled
2026-03-06 XX:XX:XX - __main__ - INFO - 触发条件满足 - issues.labeled - Issue #43
2026-03-06 XX:XX:XX - __main__ - INFO - 触发 OpenHands CLI - Issue #43 - Repo: openhandsRoywnOrg/myResume
2026-03-06 XX:XX:XX - __main__ - INFO - 命令：docker run ... openhands --headless -t "Fix issue #43: ..."
2026-03-06 XX:XX:XX - werkzeug - INFO - POST /webhook/github HTTP/1.1" 202 -
```

## 🔧 故障排查

### 问题 1：命令仍然报错 `command not found`

**解决方案**：
```bash
# 确认镜像版本
docker images | grep openhands

# 如果是旧版本，强制拉取新版本
docker pull ghcr.io/openhands/openhands:1.9

# 重启容器
docker restart openhands-webhook-server
```

### 问题 2：签名验证失败

**解决方案**：
```bash
# 检查 GitHub workflow 中的 secret
# 确保 OPENHANDS_WEBHOOK_SECRET 与 webhook 服务器的 WEBHOOK_SECRET 一致

# 查看 webhook 服务器配置
docker exec openhands-webhook-server env | grep WEBHOOK
```

### 问题 3：OpenHands 执行超时

**解决方案**：
```bash
# 增加超时时间（在 webhook_server_v1.3.py 中修改）
timeout=3600  # 改为 60 分钟

# 或者检查 LLM API 配额
curl -H "Authorization: Bearer $LLM_API_KEY" \
  $LLM_BASE_URL/v1/models
```

## 📈 性能优化建议

1. **使用本地缓存镜像**
   ```bash
   docker pull ghcr.io/openhands/openhands:1.9
   docker tag ghcr.io/openhands/openhands:1.9 openhands:latest
   ```

2. **增加并发处理**
   ```python
   # 在 webhook_server.py 中
   app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
   ```

3. **使用持久化日志**
   ```bash
   # 定期清理日志
   docker exec openhands-webhook-server \
     bash -c "tail -n 1000 /app/logs/webhook.log > /app/logs/webhook.log.tmp && \
              mv /app/logs/webhook.log.tmp /app/logs/webhook.log"
   ```

## 📚 参考资源

- [OpenHands 官方文档](https://github.com/All-Hands-AI/OpenHands)
- [OpenHands CLI 使用指南](https://docs.all-hands.dev/modules/usage/openhands-cli)
- [GitHub Webhook 文档](https://docs.github.com/en/developers/webhooks-and-events)

---

**更新时间**: 2026-03-06  
**版本**: v1.3  
**主要改进**: 使用 `openhands --headless -t` 命令
