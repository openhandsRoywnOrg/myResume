# requests / httpx：AI 应用中的 HTTP 调用基础

## 1. 为什么 AI 应用开发离不开 HTTP 客户端？

AI 应用经常需要通过 HTTP 与外部系统交互，例如：

- 调用模型 API
- 请求 embedding 服务
- 对接搜索、Webhook、GitHub、Notion 等外部服务
- 访问内部微服务或工具网关

因此，熟练掌握 Python 中的 HTTP 客户端是基础能力。

## 2. requests 适合什么场景？

`requests` 适合同步、简单、易读的 HTTP 调用。

```python
import requests

payload = {"question": "What is LangGraph?"}
response = requests.post("https://example.com/chat", json=payload, timeout=30)
print(response.status_code)
print(response.json())
```

## 3. httpx 适合什么场景？

`httpx` 同时支持同步和异步，更适合现代 AI 服务和并发请求场景。

```python
import httpx
import asyncio


async def call_api() -> None:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get("https://example.com/health")
        print(response.status_code)


asyncio.run(call_api())
```

## 4. AI 应用中的最佳实践

- 设置超时
- 检查状态码
- 处理异常
- 区分同步与异步调用方式
- 对认证信息和 base URL 做统一封装

## 5. 面试题

### Q1：为什么 AI 服务调用必须设置 timeout？

**答案：**
因为模型 API 和外部工具服务可能很慢或不可用，如果不设置 timeout，服务端线程或协程可能被长期占用，影响整体稳定性。

### Q2：什么时候更适合用 httpx 而不是 requests？

**答案：**
当项目需要异步调用、并发请求，或者希望统一同步/异步客户端体验时，httpx 更合适。
