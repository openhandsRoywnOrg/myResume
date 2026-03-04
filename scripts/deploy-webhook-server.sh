#!/bin/bash
set -e

# OpenHands Webhook 服务器部署脚本（Docker 版本）
# 用法：bash deploy-webhook-server.sh

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }

print_info "=========================================="
print_info "🚀 OpenHands Webhook 服务器部署"
print_info "=========================================="
print_info ""
print_info "⚠️  重要提示："
print_info "部署后请编辑 .env 文件，替换占位符为实际值"
print_info ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker 未安装"
    exit 1
fi

print_info "检查 Docker..."
print_success "Docker 已安装"

# 创建目录
mkdir -p ~/webhook-docker
mkdir -p ~/webhook-docker/logs
cd ~/webhook-docker

print_info "创建目录..."
print_success "目录已创建：~/webhook-docker"

# 创建 Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask==3.0.0 requests==2.31.0
COPY webhook_server.py /app/
RUN mkdir -p /app/logs
EXPOSE 5001
CMD ["python", "webhook_server.py"]
EOF

print_info "创建 Dockerfile..."

# 创建 webhook_server.py
cat > webhook_server.py << 'PYEOF'
from flask import Flask, request, jsonify
import subprocess, os, hmac, hashlib, logging, threading, json
from datetime import datetime

app = Flask(__name__)
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', 'CHANGE_THIS_SECRET')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
LLM_API_KEY = os.environ.get('LLM_API_KEY')
LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://coding.dashscope.aliyuncs.com/v1')
LLM_MODEL = os.environ.get('LLM_MODEL', 'openai/qwen3.5-plus')

log_file = '/app/logs/webhook.log'
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()])
logger = logging.getLogger(__name__)

def verify_signature(payload, signature):
    if not signature: return False
    expected = 'sha256=' + hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

def trigger_openhands(event_type, data):
    try:
        issue_number = data.get('issue', {}).get('number') or data.get('pull_request', {}).get('number')
        if not issue_number: return False, "No issue number"
        cmd = ['docker', 'run', '--rm', '-v', '/var/run/docker.sock:/var/run/docker.sock',
            '-e', f'GITHUB_TOKEN={GITHUB_TOKEN}', '-e', f'LLM_API_KEY={LLM_API_KEY}',
            '-e', f'LLM_BASE_URL={LLM_BASE_URL}', '-e', f'LLM_MODEL={LLM_MODEL}',
            'ghcr.io/openhands/openhands:1.4', 'openhands-agent',
            '--issue-number', str(issue_number), '--auto-pr', '--workspace', '/workspace']
        logger.info(f"触发 OpenHands - Issue #{issue_number}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        return result.returncode == 0, result.stdout[:500] if result.returncode == 0 else result.stderr[:500]
    except Exception as e:
        return False, str(e)

def should_trigger(event, data):
    if event == 'issues' and data.get('action') == 'labeled':
        labels = [l['name'] for l in data.get('issue', {}).get('labels', [])]
        return 'ai-agent' in labels or 'fix-me' in labels
    elif event == 'pull_request' and data.get('action') == 'labeled':
        labels = [l['name'] for l in data.get('pull_request', {}).get('labels', [])]
        return 'ai-agent' in labels
    elif event in ['issue_comment', 'pull_request_review', 'pull_request_review_comment']:
        comment = data.get('comment', {}).get('body', '') or data.get('review', {}).get('body', '')
        return '@openhands-agent' in comment
    return False

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.utcnow().isoformat()}), 200

@app.route('/webhook/github', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    payload = request.get_data()
    if not verify_signature(payload, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    event = request.headers.get('X-GitHub-Event')
    data = request.json
    logger.info(f"收到事件：{event}")
    
    if should_trigger(event, data):
        issue_number = data.get('issue', {}).get('number') or data.get('pull_request', {}).get('number')
        threading.Thread(target=lambda: trigger_openhands(event, data), daemon=True).start()
        return jsonify({'status': 'accepted', 'issue': issue_number}), 202
    return jsonify({'status': 'ignored'}), 200

if __name__ == '__main__':
    logger.info("OpenHands Webhook 服务器启动 - 端口 5001")
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
PYEOF

print_info "创建 webhook_server.py..."

# 创建 docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  webhook-server:
    build: .
    container_name: openhands-webhook
    restart: unless-stopped
    ports:
      - "5001:5001"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./logs:/app/logs
      - /workspace:/workspace
    environment:
      - WEBHOOK_SECRET=${WEBHOOK_SECRET:-CHANGE_THIS_SECRET}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - LLM_API_KEY=${LLM_API_KEY}
      - LLM_BASE_URL=${LLM_BASE_URL:-https://coding.dashscope.aliyuncs.com/v1}
      - LLM_MODEL=${LLM_MODEL:-openai/qwen3.5-plus}
EOF

print_info "创建 docker-compose.yml..."

# 创建 .env 文件（使用占位符）
cat > .env << 'EOF'
# ===========================================
# OpenHands Webhook 服务器配置
# ===========================================
# 重要：请替换以下占位符为实际值！
# ===========================================

# Webhook 密钥（用于验证 GitHub 请求）
# 建议：使用 openssl rand -hex 32 生成随机密钥
WEBHOOK_SECRET=CHANGE_THIS_SECRET

# GitHub Personal Access Token
# 需要 repo 权限
GITHUB_TOKEN=ghp_YOUR_GITHUB_TOKEN_HERE

# LLM API 配置（阿里云 DashScope）
LLM_API_KEY=sk-YOUR_LLM_API_KEY_HERE
LLM_BASE_URL=https://coding.dashscope.aliyuncs.com/v1
LLM_MODEL=openai/qwen3.5-plus

# ===========================================
EOF

print_info "创建 .env 文件（占位符）..."
print_warning "请编辑 ~/webhook-docker/.env 文件，替换占位符为实际值"

# 构建并启动
print_info ""
print_info "构建 Docker 镜像..."
docker-compose build

print_info "启动容器..."
docker-compose up -d

sleep 5

# 验证
if docker ps | grep -q openhands-webhook; then
    print_success "部署完成！"
    print_info ""
    print_info "=========================================="
    print_info "📊 服务信息:"
    print_info "=========================================="
    SERVER_IP=$(hostname -I | awk '{print $1}')
    echo "   - Webhook 地址：http://$SERVER_IP:5001/webhook/github"
    echo "   - 健康检查：http://$SERVER_IP:5001/health"
    echo ""
    print_info "=========================================="
    print_info "📋 下一步:"
    print_info "=========================================="
    echo "   1. 编辑配置文件：nano ~/webhook-docker/.env"
    echo "   2. 替换占位符为实际值"
    echo "   3. 重启容器：docker-compose restart"
    echo "   4. 测试：curl http://$SERVER_IP:5001/health"
    echo ""
    print_info "=========================================="
    print_info "🔧 管理命令:"
    print_info "=========================================="
    echo "   - 查看状态：docker ps | grep webhook"
    echo "   - 查看日志：docker logs -f openhands-webhook"
    echo "   - 重启：docker-compose restart"
    echo "   - 停止：docker-compose down"
    echo ""
else
    print_error "启动失败"
    print_info "查看日志：docker logs openhands-webhook"
    exit 1
fi
