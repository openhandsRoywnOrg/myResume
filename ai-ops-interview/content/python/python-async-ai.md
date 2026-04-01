# Async / asyncio 在 AI 应用中的实践

## 1. 为什么 AI 应用开发经常需要异步？

AI 应用通常会同时处理多种 I/O 操作：

- 请求 LLM API
- 访问向量数据库
- 调用外部工具接口
- 拉取网页或知识库内容
- 与前端保持流式通信

这些任务大多是 **I/O 密集型**，而不是 CPU 密集型，因此使用异步可以更高效地利用等待时间。

## 2. 什么时候适合用 async？

适合：
- 并发调用多个 API
- 同时执行多个检索请求
- Web 服务中的高并发请求处理
- 流式输出和事件驱动任务

不一定适合：
- 纯 CPU 重计算
- 非并发的小脚本
- 团队还无法维护异步复杂度的场景

## 3. 基础示例

```python
import asyncio


async def fetch_model_result(name: str) -> str:
    await asyncio.sleep(1)
    return f"{name} result"


async def main() -> None:
    results = await asyncio.gather(
        fetch_model_result("summary"),
        fetch_model_result("keywords"),
        fetch_model_result("score"),
    )
    print(results)


asyncio.run(main())
```

## 4. AI 场景中的典型收益

- 减少串行等待时间
- 提高 API 聚合效率
- 更适合构建流式聊天和工具链
- 提升 FastAPI 服务并发能力

## 5. 常见误区

- 把所有代码都改成 async
- 忘记 `await`
- 在同步库上强行套异步写法
- 代码结构变复杂后缺少统一封装

## 6. 面试题

### Q1：为什么 AI 应用里 async 经常比多线程更常见？

**答案：**
因为很多 AI 应用的瓶颈在网络请求和外部 I/O，异步更适合处理大量等待型任务，同时开销通常比线程更可控。

### Q2：什么时候不建议引入 asyncio？

**答案：**
如果项目规模小、调用链简单、团队对异步不熟悉，或者核心问题不是 I/O 等待，那么异步带来的复杂度可能大于收益。
