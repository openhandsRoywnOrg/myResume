# FastAPI：构建 AI 服务接口的常见做法

## 1. 为什么很多 AI 应用后端喜欢 FastAPI？

因为 FastAPI 同时具备：
- 开发速度快
- 类型提示友好
- 自动生成接口文档
- 原生支持异步
- 和 Pydantic 配合顺畅

这非常适合做：
- Chat API
- RAG 检索接口
- Agent 调用入口
- 模型代理层

## 2. 基础接口示例

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(request: ChatRequest) -> dict[str, str]:
    return {"answer": f"你问的是: {request.question}"}
```

## 3. AI 服务设计建议

- 把模型调用逻辑放到 service 层
- 把 schema 单独维护
- 区分同步接口与流式接口
- 统一错误处理和日志记录
- 给外部调用设置超时和重试策略

## 4. 常见接口类型

- `/chat`：对话问答
- `/rag/query`：知识检索问答
- `/agent/run`：执行 Agent 任务
- `/health`：健康检查
- `/config`：运行配置查看

## 5. 面试题

### Q1：为什么 FastAPI 很适合 AI 后端？

**答案：**
因为它在接口定义、数据校验、异步支持和文档生成方面都很适合快速构建 AI 服务，尤其适合模型代理和工具服务封装。

### Q2：为什么不建议把 LLM 调用直接写在路由函数里？

**答案：**
因为这样会让路由层承担过多职责，不利于测试、复用和维护。更合理的做法是路由只负责接收请求，业务逻辑放到 service 层。
