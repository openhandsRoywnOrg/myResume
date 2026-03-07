#!/bin/bash
# Webhook Server 部署脚本 - 宿主机模式
# 直接在宿主机运行，无需 Docker

set -e

echo "======================================"
echo "Webhook Server 部署 - 宿主机模式"
echo "======================================"

# 1. 检查 Python
echo "🔍 检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：python3 未安装"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# 2. 安装依赖
echo ""
echo "📦 安装依赖..."
pip3 install flask --quiet
echo "✅ Flask 已安装"

# 3. 检查 openhands
echo ""
echo "🔍 检查 OpenHands CLI..."
if ! command -v openhands &> /dev/null; then
    echo "❌ 错误：openhands 命令未找到"
    echo "   请安装：pip3 install openhands-ai"
    exit 1
fi
echo "✅ OpenHands: $(which openhands)"
openhands --version 2>&1 | head -1

# 4. 检查配置文件
echo ""
echo "📋 检查 OpenHands 配置..."
if [ -f "$HOME/.openhands/agent_settings.json" ]; then
    echo "✅ 配置文件存在"
else
    echo "⚠️  配置文件不存在，请先运行 openhands 进行初始化"
fi

# 5. 停止现有进程
echo ""
echo "🛑 停止现有进程..."
pkill -f "python.*webhook_server" 2>/dev/null || true
sleep 2

# 6. 启动服务
echo ""
echo "🚀 启动 Webhook Server..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WEBHOOK_CODE="$SCRIPT_DIR/webhook_server_v2.0.py"

if [ ! -f "$WEBHOOK_CODE" ]; then
    echo "❌ 错误：找不到 $WEBHOOK_CODE"
    exit 1
fi

# 设置环境变量
export WEBHOOK_SECRET="${WEBHOOK_SECRET:-}"
if [ -z "$WEBHOOK_SECRET" ]; then
    echo "⚠️  警告：WEBHOOK_SECRET 未设置，请确保已设置"
fi

# 后台运行
nohup python3 "$WEBHOOK_CODE" > /tmp/webhook_server.log 2>&1 &
PID=$!

# 7. 等待启动
echo "⏳ 等待服务启动..."
sleep 3

# 8. 健康检查
echo ""
echo "🏥 执行健康检查..."
if curl -f http://127.0.0.1:5001/health > /dev/null 2>&1; then
    echo ""
    echo "✅ Webhook Server 启动成功！"
    echo ""
    echo "======================================"
    echo "服务信息："
    echo "  - PID: $PID"
    echo "  - 端口：5001"
    echo "  - 健康检查：http://127.0.0.1:5001/health"
    echo "  - 日志查看：http://127.0.0.1:5001/logs"
    echo "  - 日志文件：/tmp/webhook_server.log"
    echo "  - 模式：宿主机模式 (Host)"
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
    tail -50 /tmp/webhook_server.log
    exit 1
fi
