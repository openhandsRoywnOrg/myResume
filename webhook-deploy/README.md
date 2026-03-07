# Webhook Server v2.0 - 部署文档

## 📦 文件说明

本目录包含部署 OpenHands Webhook Server 所需的关键文件：

- `webhook_server_v2.0.py` - Webhook 服务器主程序
- `deploy-webhook-v2.sh` - 自动部署脚本

## ⚡ 快速部署

### 1. 前置要求

确保已安装 OpenHands CLI：

```bash
# 检查是否安装
openhands --version

# 如果未安装
pip install openhands-ai
```

### 2. 配置环境变量

```bash
# 🔐 必须设置：生成强密码 Secret
openssl rand -hex 32
export WEBHOOK_SECRET="your-secret-here"

# 可选：如果需要覆盖 LLM 配置
export LLM_API_KEY="your-api-key"
export LLM_MODEL="openai/qwen3.5-plus"
export LLM_BASE_URL="https://coding.dashscope.aliyuncs.com/v1"
```

**⚠️ 重要安全提示**：
- `WEBHOOK_SECRET` **必须设置**，否则服务无法启动
- `WEBHOOK_SECRET` 必须与 GitHub Workflow 中的 `secrets.OPENHANDS_WEBHOOK_SECRET` 一致
- 使用强密码（至少 32 位随机字符）
- 不要将 secret 提交到版本控制系统

### 3. 运行部署脚本

```bash
chmod +x deploy-webhook-v2.sh
./deploy-webhook-v2.sh
```

### 4. 验证部署

```bash
# 健康检查
curl http://localhost:5001/health

# 查看日志
docker logs -f openhands-webhook-server
```

## 🔧 手动部署

如果不想使用自动部署脚本：

```bash
# 1. 停止旧容器
docker stop openhands-webhook-server 2>/dev/null || true
docker rm openhands-webhook-server 2>/dev/null || true

# 2. 创建日志目录
sudo mkdir -p /app/logs
sudo chmod 777 /app/logs

# 3. 启动容器
docker run -d \
  --name openhands-webhook-server \
  --restart unless-stopped \
  -p 5001:5001 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /app/logs:/app/logs \
  -v $(pwd)/webhook_server_v2.0.py:/app/webhook_server.py:ro \
  -v $HOME/.openhands:/root/.openhands \
  -e WEBHOOK_SECRET="$WEBHOOK_SECRET" \
  python:3.12-slim \
  python /app/webhook_server.py

# 4. 验证
curl http://localhost:5001/health
```

## 🧪 测试

### 创建测试 Issue

```bash
curl -X POST "https://api.github.com/repos/YOUR_ORG/YOUR_REPO/issues" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -d '{
    "title": "[测试] Webhook v2.0",
    "body": "测试 OpenHands Webhook Server",
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

## 📝 配置 GitHub Workflow

确保你的 `.github/workflows/openhands-resolver.yml` 配置正确：

```yaml
name: Forward to OpenHands Server

on:
  issues:
    types: [labeled]
  pull_request:
    types: [labeled]
  issue_comment:
    types: [created]

permissions:
  contents: write
  pull-requests: write
  issues: write

jobs:
  forward-event:
    runs-on: ubuntu-latest
    steps:
      - name: Forward to Webhook Server
        run: |
          SIGNATURE="sha256=$(echo -n "$GITHUB_PAYLOAD" | openssl dgst -sha256 -hmac "$WEBHOOK_SECRET" | awk '{print $2}')"
          
          curl -v -X POST "YOUR_SERVER_URL/webhook/github" \
            -H "Content-Type: application/json" \
            -H "X-GitHub-Event: $GITHUB_EVENT" \
            -H "X-Hub-Signature-256: $SIGNATURE" \
            -d "$GITHUB_PAYLOAD"
        env:
          WEBHOOK_SECRET: ${{ secrets.OPENHANDS_WEBHOOK_SECRET }}
          WEBHOOK_URL: ${{ secrets.OPENHANDS_SERVER_URL }}
          GITHUB_EVENT: ${{ github.event_name }}
          GITHUB_PAYLOAD: ${{ toJSON(github.event) }}
```

### 设置 GitHub Secrets

在 GitHub 仓库中设置以下 Secrets：

1. **OPENHANDS_WEBHOOK_SECRET** - 与 `WEBHOOK_SECRET` 环境变量相同
2. **OPENHANDS_SERVER_URL** - Webhook 服务器的公网 URL

## 🔒 安全建议

1. **使用强 Secret**
   ```bash
   # 生成随机 secret
   openssl rand -hex 32
   ```

2. **不要提交 Secret**
   - 使用环境变量
   - 使用 GitHub Secrets
   - 不要硬编码在代码中

3. **限制访问**
   - 使用防火墙限制 5001 端口访问
   - 只允许 GitHub Actions IP 访问
   - 使用反向代理（nginx）

4. **定期更新**
   - 定期更换 Secret
   - 监控日志中的异常

## 📊 预期日志输出

成功的日志应该显示：

```
2026-03-07 XX:XX:XX - INFO - 收到事件 - Type: issues, Delivery: xxx, Action: labeled
2026-03-07 XX:XX:XX - INFO - 触发条件满足 - issues.labeled - Issue #42
2026-03-07 XX:XX:XX - INFO - 触发 OpenHands Headless - Issue #42
2026-03-07 XX:XX:XX - INFO - 命令：openhands --headless -t "Please fix GitHub issue #42..."
2026-03-07 XX:XX:XX - INFO - OpenHands 处理成功 - Issue #42
```

## 🆘 故障排查

### 问题 1: `openhands: command not found`

```bash
# 解决：安装 OpenHands CLI
pip install openhands-ai
```

### 问题 2: 签名验证失败

```bash
# 检查：确保 GitHub Secret 与 WEBHOOK_SECRET 一致
echo $WEBHOOK_SECRET
# 对比 GitHub Settings -> Secrets -> OPENHANDS_WEBHOOK_SECRET
```

### 问题 3: 配置缺失

```bash
# 检查配置文件
ls -la ~/.openhands/

# 如果没有配置文件，运行一次 openhands 进行初始化
openhands --headless -t "test"
```

## 📚 参考文档

- [OpenHands CLI Command Reference](https://docs.openhands.dev/openhands/usage/cli/command-reference)
- [OpenHands Headless Mode](https://docs.openhands.dev/openhands/usage/cli/headless)
- [GitHub Webhook 文档](https://docs.github.com/en/developers/webhooks-and-events)

---

**版本**: v2.0  
**日期**: 2026-03-07  
**状态**: ✅ 生产就绪
