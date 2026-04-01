# 虚拟环境与依赖管理

## 1. 为什么 AI 项目更容易出现依赖问题？

AI 项目通常会同时依赖：
- Web 框架（FastAPI / Flask）
- LLM SDK（OpenAI / Anthropic）
- Agent 框架（LangChain / LangGraph）
- 数据处理库
- 向量数据库客户端

一旦依赖版本混乱，最容易出现导入错误、接口不兼容和环境漂移。

## 2. 常见做法

### 使用 venv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### requirements.txt

```txt
fastapi
uvicorn
langchain
langgraph
openai
```

## 3. 最佳实践

- 每个项目使用独立虚拟环境
- 依赖集中维护，不要手工记忆
- 明确区分运行依赖和开发依赖
- 在 README 中写清启动方式

## 4. 面试题

### Q1：为什么不能把所有 Python 项目都装在全局环境里？

**答案：**
因为不同项目依赖版本常常冲突。独立虚拟环境能保证项目隔离、可复现和部署一致性。

### Q2：AI 项目为什么更要重视依赖锁定？

**答案：**
因为 AI 框架更新很快，同一个接口在不同版本中可能有明显差异。锁定版本能减少“昨天能跑今天不能跑”的问题。
