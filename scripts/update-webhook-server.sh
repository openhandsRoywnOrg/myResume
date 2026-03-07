#!/bin/bash
# Webhook 服务器更新脚本 - v1.3
# 使用本地 openhands --headless -t 命令

set -e

echo "======================================"
echo "Webhook 服务器更新 - v1.3"
echo "======================================"

# 1. 检查 openhands 命令是否存在
echo "🔍 检查 OpenHands CLI 安装..."
if ! command -v openhands &> /dev/null; then
    echo "❌ 错误：openhands 命令未找到！"
    echo "请先安装 OpenHands CLI："
    echo "   pip install openhands-ai"
    echo "或者："
    echo "   curl -sSL https://install.openhands.dev | bash"
    exit 1
fi

echo "✅ OpenHands CLI 已安装：$(which openhands)"
openhands --version || true

# 2. 停止现有容器
echo "📦 停止现有容器..."
docker stop openhands-webhook-server 2>/dev/null || true
docker rm openhands-webhook-server 2>/dev/null || true

# 3. 复制新版本的 webhook 服务器代码
echo "📝 复制 webhook 服务器代码..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WEBHOOK_CODE="$SCRIPT_DIR/webhook_server_v1.3.py"

if [ ! -f "$WEBHOOK_CODE" ]; then
    echo "❌ 错误：找不到 webhook 服务器代码 $WEBHOOK_CODE"
    exit 1
fi

# 4. 创建日志目录
echo "📁 创建日志目录..."
sudo mkdir -p /app/logs
sudo chmod 777 /app/logs

# 5. 启动新容器（使用 Python 镜像，不需要 Docker in Docker）
echo "🚀 启动新的 webhook 服务器..."
docker run -d \
    --name openhands-webhook-server \
    --restart unless-stopped \
    -p 5001:5001 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /app/logs:/app/logs \
    -v "$WEBHOOK_CODE:/app/webhook_server.py:ro" \
    -v /home/ubuntu/.openhands:/root/.openhands \
    -e WEBHOOK_SECRET="$WEBHOOK_SECRET" \
    -e GITHUB_TOKEN="$GITHUB_TOKEN" \
    -e LLM_API_KEY="$LLM_API_KEY" \
    -e LLM_BASE_URL="$LLM_BASE_URL" \
    -e LLM_MODEL="$LLM_MODEL" \
    -e WORKSPACE_PATH="/workspace" \
    python:3.12-slim \
    bash -c "pip install openhands-ai && python /app/webhook_server.py"

# 6. 等待启动
echo "⏳ 等待服务启动..."
sleep 5

# 7. 健康检查
echo "🏥 执行健康检查..."
if curl -f http://localhost:5001/health; then
    echo "✅ Webhook 服务器启动成功！"
    echo ""
    echo "======================================"
    echo "服务信息："
    echo "  - 端口：5001"
    echo "  - 健康检查：http://localhost:5001/health"
    echo "  - 日志查看：http://localhost:5001/logs"
    echo "  - 命令模式：openhands --headless -t"
    echo "======================================"
else
    echo "❌ 健康检查失败！"
    echo "查看日志："
    docker logs openhands-webhook-server
    exit 1
fi
