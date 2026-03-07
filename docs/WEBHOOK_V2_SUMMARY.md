# Webhook Server v2.0 - 学习官方文档后重写

## 🎯 关键学习

### 之前版本的错误 ❌

在 v1.3 及更早版本中，我**编造了不存在的命令参数**：

```bash
# ❌ 错误的命令（我编造的）
openhands --headless -t "task" --repo owner/repo --issue-number 42 --auto-pr
```

这些参数**都不存在**：
- `--repo` ❌
- `--issue-number` ❌  
- `--auto-pr` ❌

### 正确的用法 ✅

学习官方文档后，正确的命令格式是：

```bash
# ✅ 正确的命令
openhands --headless -t "Please fix GitHub issue #42 in repository owner/repo\n\nIssue Title: ...\n\nDescription: ..." --exit-without-confirmation
```

## 📚 官方文档要点

### 1. Headless 模式

**文档**: https://docs.openhands.dev/openhands/usage/cli/headless

关键要点：
- 无 UI，适合自动化
- **必须**指定 `--task` 或 `--file`
- 默认运行在 `--always-approve` 模式
- 无法使用 `--llm-approve`

### 2. 命令参考

**文档**: https://docs.openhands.dev/openhands/usage/cli/command-reference

**必需参数**：
- `--headless`: 无头模式
- `-t, --task TEXT`: 初始任务（headless 模式必需）

**可选参数**：
- `-f, --file PATH`: 从文件读取任务
- `--json`: JSONL 输出
- `--exit-without-confirmation`: 退出时不显示确认
- `--override-with-envs`: 使用环境变量覆盖

**不存在的参数**：
- `--repo` ❌
- `--issue-number` ❌
- `--auto-pr` ❌

### 3. 配置管理

**GitHub 集成**不是通过命令行参数，而是通过：

1. **配置文件**: `~/.openhands/agent_settings.json`
2. **MCP 配置**: `~/.openhands/mcp.json`
3. **环境变量**: `LLM_API_KEY`, `LLM_MODEL`, `LLM_BASE_URL`

## 🔧 v2.0 核心改进

### 1. 正确的命令调用

```python
# ✅ v2.0 正确的实现
cmd = [
    'openhands',
    '--headless',
    '-t', task_description,  # 完整的任务描述
    '--exit-without-confirmation'
]

# 可选：添加 --json 用于结构化输出
# cmd.append('--json')
```

### 2. 改进的任务描述

```python
def build_task_description(issue_number, repo, title, body):
    """构建符合官方文档的任务描述"""
    task = f"Please fix GitHub issue #{issue_number} in repository {repo}\n\n"
    task += f"Issue Title: {title}\n\n"
    
    if body:
        body_preview = body[:1000] if len(body) > 1000 else body
        task += f"Issue Description:\n{body_preview}\n\n"
    
    task += "Please analyze the issue, implement the necessary code changes, and create a pull request if needed."
    
    return task
```

### 3. 配置共享

```bash
# 挂载 ~/.openhands 目录，共享配置
docker run -v $HOME/.openhands:/root/.openhands ...
```

## 🚀 部署步骤

### 前置要求

1. **安装 OpenHands CLI**
```bash
pip install openhands-ai
```

2. **配置 LLM**
```bash
export LLM_API_KEY="your-api-key"
export LLM_MODEL="openai/qwen3.5-plus"
export LLM_BASE_URL="https://coding.dashscope.aliyuncs.com/v1"
```

3. **配置 GitHub 集成**（可选）
```bash
openhands mcp add github --transport stdio node -- -g @openhands/mcp-github
```

### 快速部署

```bash
cd /workspace/project/myResume/scripts
./deploy-webhook-v2.sh
```

## 🧪 测试

### 创建测试 Issue

```bash
curl -X POST "https://api.github.com/repos/openhandsRoywnOrg/myResume/issues" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -d '{
    "title": "[测试] v2.0",
    "body": "测试基于官方文档的正确实现",
    "labels": ["ai-agent"]
  }'
```

### 查看日志

```bash
docker logs -f openhands-webhook-server
```

### 预期输出

```
✅ 收到事件 - Type: issues, Action: labeled
✅ 触发条件满足 - issues.labeled - Issue #XX
✅ 触发 OpenHands Headless - Issue #XX
✅ 命令：openhands --headless -t "Please fix GitHub issue #XX..."
✅ OpenHands 处理成功 - Issue #XX
```

## 📊 版本对比

| 项目 | v1.3 (错误版本) | v2.0 (正确版本) |
|------|----------------|-----------------|
| **命令参数** | 编造的参数 ❌ | 官方文档 ✅ |
| **--repo** | ❌ 不存在 | ✅ 移除 |
| **--issue-number** | ❌ 不存在 | ✅ 移除 |
| **--auto-pr** | ❌ 不存在 | ✅ 移除 |
| **任务描述** | 简单 | 完整详细 ✅ |
| **配置方式** | 环境变量 | ~/.openhands ✅ |
| **文档参考** | 无 | 官方文档 ✅ |

## 🎓 学习总结

### 关键教训

1. **不要编造参数**：必须查阅官方文档
2. **理解配置层次**：环境变量 > 配置文件
3. **GitHub 集成方式**：通过 MCP，不是命令行参数
4. **任务描述要完整**：包含所有必要信息

### 正确的开发流程

1. ✅ 先阅读官方文档
2. ✅ 理解命令和参数
3. ✅ 实现代码
4. ✅ 测试验证
5. ✅ 更新文档

## 🔗 重要链接

- [CLI Command Reference](https://docs.openhands.dev/openhands/usage/cli/command-reference)
- [Headless Mode](https://docs.openhands.dev/openhands/usage/cli/headless)
- [GitHub Integration](https://docs.openhands.dev/openhands/integrations/github)
- [MCP Servers](https://docs.openhands.dev/openhands/usage/mcp)

---

**版本**: v2.0  
**状态**: ✅ 基于官方文档  
**日期**: 2026-03-06  
**教训**: 不要编造参数，先读文档！
