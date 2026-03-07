# Webhook Server v2.0 - 基于官方文档修正版

## 📚 文档参考

- [OpenHands CLI Command Reference](https://docs.openhands.dev/openhands/usage/cli/command-reference)
- [OpenHands Headless Mode](https://docs.openhands.dev/openhands/usage/cli/headless)

## ✅ 核心修正

### 重要发现

根据官方文档，**之前版本的命令参数都是编造的** ❌

**错误的命令**（v1.3）：
```bash
openhands --headless -t "task" --repo owner/repo --issue-number 42 --auto-pr
```

**正确的命令**（v2.0）：
```bash
openhands --headless -t "Please fix GitHub issue #42..." --exit-without-confirmation
```

### 关键参数说明

| 参数 | 说明 | 是否必需 |
|------|------|----------|
| `--headless` | 无头模式（无 UI） | ✅ 必需 |
| `-t, --task TEXT` | 初始任务描述 | ✅ Headless 模式必需 |
| `-f, --file PATH` | 从文件读取任务 | 与 -t 二选一 |
| `--exit-without-confirmation` | 退出时不显示确认 | 推荐 |
| `--json` | JSONL 输出 | 可选（用于解析） |
| `--always-approve` | 自动批准 | Headless 模式默认启用 |

### ❌ 不存在的参数

以下参数**不存在**，是我之前编造的：
- `--repo` ❌
- `--issue-number` ❌
- `--auto-pr` ❌

### ✅ 正确的使用方式

GitHub 集成是通过配置文件实现的，不是命令行参数：

1. **配置文件位置**：`~/.openhands/agent_settings.json`
2. **GitHub MCP 配置**：`~/.openhands/mcp.json`
3. **环境变量**（可选）：`LLM_API_KEY`, `LLM_MODEL` 等

## 🚀 部署方法

### 前置要求

1. **安装 OpenHands CLI**
```bash
pip install openhands-ai
# 或
curl -sSL https://install.openhands.dev | bash
```

2. **配置 OpenHands**
```bash
# 运行一次进行初始化配置
openhands

# 或使用环境变量
export LLM_API_KEY="your-api-key"
export LLM_MODEL="openai/qwen3.5-plus"
export LLM_BASE_URL="https://coding.dashscope.aliyuncs.com/v1"
```

3. **配置 GitHub 集成**（可选）
```bash
# 添加 GitHub MCP 服务器
openhands mcp add github --transport stdio node -- -g @openhands/mcp-github
```

### 快速部署

```bash
cd /workspace/project/myResume/scripts
chmod +x deploy-webhook-v2.sh
./deploy-webhook-v2.sh
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
  -v /workspace/project/myResume/scripts/webhook_server_v2.0.py:/app/webhook_server.py:ro \
  -v $HOME/.openhands:/root/.openhands \
  -e WEBHOOK_SECRET="$WEBHOOK_SECRET" \
  python:3.12-slim \
  python /app/webhook_server.py

# 3. 验证
curl http://localhost:5001/health
```

## 📝 命令格式

### 基本用法

```bash
# 运行任务
openhands --headless -t "Please fix GitHub issue #42 in owner/repo"

# 从文件读取任务
openhands --headless -f task.txt

# JSONL 输出（便于解析）
openhands --headless --json -t "Your task"
```

### Webhook Server 调用方式

```python
# 构建任务描述
task = f"Please fix GitHub issue #{issue_number} in repository {repo}\n\n"
task += f"Issue Title: {title}\n\n"
task += f"Issue Description:\n{body}\n\n"
task += "Please analyze the issue, implement the necessary code changes."

# 执行命令
cmd = [
    'openhands',
    '--headless',
    '-t', task,
    '--exit-without-confirmation'
]

# 可选：添加 --json 用于结构化输出
# cmd.append('--json')

result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
```

## 🧪 测试方法

### 1. 创建测试 Issue

```bash
curl -X POST "https://api.github.com/repos/openhandsRoywnOrg/myResume/issues" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -d '{
    "title": "[测试] Webhook v2.0",
    "body": "测试基于官方文档的 headless 模式",
    "labels": ["ai-agent"]
  }'
```

### 2. 查看日志

```bash
# 实时日志
docker logs -f openhands-webhook-server

# 或 HTTP 接口
curl http://localhost:5001/logs
```

### 3. 预期输出

```
✅ 收到事件 - Type: issues, Action: labeled
✅ 触发条件满足 - issues.labeled - Issue #43
✅ 触发 OpenHands Headless - Issue #43
✅ 命令：openhands --headless -t "Please fix GitHub issue #43..."
✅ OpenHands 处理成功 - Issue #43
```

## 📊 Headless 模式特点

### 优势

1. **无 UI**：适合自动化脚本和 CI/CD
2. **自动批准**：headless 模式默认 `--always-approve`
3. **结构化输出**：可使用 `--json` 获取 JSONL 输出

### 限制

1. **必须指定任务**：必须使用 `--task` 或 `--file`
2. **无法使用 LLM 审批**：`--llm-approve` 不可用
3. **总是自动批准**：无法关闭自动批准

## 🔧 故障排查

### 问题 1: `openhands: command not found`

```bash
# 原因：未安装 OpenHands CLI
# 解决：
pip install openhands-ai
```

### 问题 2: 配置缺失

```bash
# 检查配置文件
ls -la ~/.openhands/

# 如果没有配置文件，运行一次 openhands 进行初始化
openhands --headless -t "test"
```

### 问题 3: GitHub 集成未配置

```bash
# 检查 MCP 配置
cat ~/.openhands/mcp.json

# 添加 GitHub MCP（如果需要）
openhands mcp add github --transport stdio node -- -g @openhands/mcp-github
```

### 问题 4: 签名验证失败

```bash
# 检查 GitHub workflow 的 secret
# 确保 OPENHANDS_WEBHOOK_SECRET 与 WEBHOOK_SECRET 一致
```

## 📁 修改的文件

1. **`scripts/webhook_server_v2.0.py`**
   - ✅ 基于官方文档重新编写
   - ✅ 移除编造的参数（--repo, --issue-number 等）
   - ✅ 使用正确的命令格式
   - ✅ 改进任务描述构建

2. **`scripts/deploy-webhook-v2.sh`**
   - ✅ 添加配置检查
   - ✅ 挂载 ~/.openhands 目录
   - ✅ 更新文档链接

3. **`docs/WEBHOOK_SERVER_V2.0.md`**
   - ✅ 完整的 v2.0 文档
   - ✅ 基于官方文档说明

## 🎓 关键理解

### OpenHands CLI 架构

```
┌─────────────────┐
│  Webhook Server │
│   (Flask App)   │
└────────┬────────┘
         │
         │ 调用
         ↓
┌─────────────────┐
│  OpenHands CLI  │
│  (Headless Mode)│
└────────┬────────┘
         │
         │ 读取配置
         ↓
┌─────────────────┐
│ ~/.openhands/   │
│ - agent_settings.json (LLM 配置)
│ - mcp.json (GitHub 集成)
│ - conversations/ (历史记录)
└─────────────────┘
```

### 配置层次

1. **最高优先级**：命令行参数（如 `--override-with-envs`）
2. **中等优先级**：环境变量（`LLM_API_KEY`, `LLM_MODEL`）
3. **最低优先级**：配置文件（`~/.openhands/agent_settings.json`）

### Webhook Server 职责

1. 接收 GitHub webhook
2. 验证签名
3. 判断是否满足触发条件
4. 构建任务描述
5. 调用 `openhands --headless -t "<task>"`
6. 记录日志

## 🔗 相关资源

- [OpenHands CLI 文档](https://docs.openhands.dev/openhands/usage/cli)
- [Headless 模式文档](https://docs.openhands.dev/openhands/usage/cli/headless)
- [命令参考](https://docs.openhands.dev/openhands/usage/cli/command-reference)
- [GitHub 集成](https://docs.openhands.dev/openhands/integrations/github)

---

**版本**: v2.0  
**状态**: ✅ 完成  
**日期**: 2026-03-06  
**基于**: 官方文档
