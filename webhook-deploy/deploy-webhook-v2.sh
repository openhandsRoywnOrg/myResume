#!/bin/bash
# Webhook 服务器部署脚本 - v2.0 (Headless 模式)
# 基于官方文档修正版本

set -e

echo "======================================"
echo "Webhook 服务器部署 - v2.0"
echo "Headless 模式 (基于官方文档)"
echo "======================================"

# 1. 检查 openhands 命令是否存在
echo "🔍 检查 OpenHands CLI 安装..."
if ! command -v openhands &> /dev/null; then
    echo "❌ 错误：openhands 命令未找到！"
    echo ""
    echo "请先安装 OpenHands CLI："
    echo "   pip install openhands-ai"
    echo "或者："
    echo "   curl -sSL https://install.openhands.dev | bash"
    exit 1
fi

echo "✅ OpenHands CLI 已安装：$(which openhands)"
openhands --version 2>&1 | head -1 || true

# 2. 检查配置文件
echo ""
echo "📋 检查 OpenHands 配置..."
if [ -f "$HOME/.openhands/agent_settings.json" ]; then
    echo "✅ 配置文件存在：$HOME/.openhands/agent_settings.json"
else
    echo "⚠️  配置文件不存在：$HOME/.openhands/agent_settings.json"
    echo "   请先运行 openhands 进行初始化配置"
fi

# 3. 停止现有容器
echo ""
echo "📦 停止现有容器..."
docker stop openhands-webhook-server 2>/dev/null || true
docker rm openhands-webhook-server 2>/dev/null || true

# 4. 复制新版本的 webhook 服务器代码
echo "📝 复制 webhook 服务器代码..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WEBHOOK_CODE="$SCRIPT_DIR/webhook_server_v2.0.py"

if [ ! -f "$WEBHOOK_CODE" ]; then
    echo "❌ 错误：找不到 webhook 服务器代码 $WEBHOOK_CODE"
    exit 1
fi

# 5. 创建日志目录
echo "📁 创建日志目录..."
sudo mkdir -p /app/logs
sudo chmod 777 /app/logs

# 6. 启动新容器
echo "🚀 启动新的 webhook 服务器..."
docker run -d \
    --name openhands-webhook-server \
    --restart unless-stopped \
    -p 5001:5001 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /app/logs:/app/logs \
    -v "$WEBHOOK_CODE:/app/webhook_server.py:ro" \
    -v "$HOME/.openhands:/root/.openhands" \
    -e WEBHOOK_SECRET="$WEBHOOK_SECRET" \
    python:3.12-slim \
    bash -c "pip install flask openhands-ai && python /app/webhook_server.py"

# 7. 等待启动
echo "⏳ 等待服务启动..."
sleep 5

# 8. 健康检查
echo "🏥 执行健康检查..."
if curl -f http://localhost:5001/health; then
    echo ""
    echo "✅ Webhook 服务器启动成功！"
    echo ""
    echo "======================================"
    echo "服务信息："
    echo "  - 端口：5001"
    echo "  - 健康检查：http://localhost:5001/health"
    echo "  - 日志查看：http://localhost:5001/logs"
    echo "  - 模式：Headless (无 UI)"
    echo "  - 版本：v2.0"
    echo "======================================"
    echo ""
    echo "📚 参考文档:"
    echo "  - https://docs.openhands.dev/openhands/usage/cli/command-reference"
    echo "  - https://docs.openhands.dev/openhands/usage/cli/headless"
    echo "======================================"
else
    echo "❌ 健康检查失败！"
    echo ""
    echo "查看日志："
    docker logs openhands-webhook-server
    exit 1
fi
