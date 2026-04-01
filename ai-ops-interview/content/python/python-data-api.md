# 文件处理、JSON 与 API 调用

## 1. 这是 AI 应用开发的日常高频工作

很多 AI 项目并不复杂在模型本身，而复杂在“数据进出”。例如：

- 读取 Markdown / PDF / 配置文件
- 解析模型返回 JSON
- 调用外部 API 或内部工具服务
- 保存会话记录和中间结果

## 2. 文件处理

```python
from pathlib import Path

content = Path("prompt.md").read_text(encoding="utf-8")
print(content)
```

## 3. JSON 处理

```python
import json

raw = '{"answer": "LangChain 是 LLM 应用开发框架"}'
data = json.loads(raw)
print(data["answer"])
```

## 4. 调用 HTTP API

```python
import requests

response = requests.get("https://api.github.com/repos/langchain-ai/langchain")
print(response.status_code)
print(response.json().get("stargazers_count"))
```

## 5. 面试题

### Q1：为什么 JSON 在 AI 项目中特别重要？

**答案：**
因为模型接口、工具调用、前后端交互、配置文件、日志事件通常都以 JSON 作为结构化交换格式。

### Q2：读取文件时为什么推荐使用 pathlib？

**答案：**
因为它语义更清晰、跨平台更友好，路径拼接和文件操作可读性更高。
