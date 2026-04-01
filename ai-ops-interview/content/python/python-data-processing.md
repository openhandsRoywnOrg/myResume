# 数据处理与 Chunking：AI 应用开发中的 Python 基础

## 1. 为什么 AI 应用开发特别依赖数据处理？

很多 AI 应用在模型调用之前，真正的工作是：

- 清洗文本
- 拆分文档
- 提取字段
- 规范化输入
- 构建 chunks
- 组织检索结果

这一步做不好，后面的 Prompt、RAG、Agent 都会受到影响。

## 2. 常见处理任务

- 去掉空白和噪声
- 分段处理长文本
- 从 JSON 中提取关键信息
- 组装检索上下文
- 控制 chunk 大小和 overlap

## 3. Python 示例

```python
def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
```

## 4. AI 场景中的意义

- 提升检索命中率
- 控制上下文长度
- 改善模型回答质量
- 让文档处理流程更稳定

## 5. 面试题

### Q1：为什么 RAG 中不能直接把整篇长文都送进模型？

**答案：**
因为上下文长度有限，而且整篇输入会增加噪声。合理的 chunking 可以提高相关性和可控性。

### Q2：chunk overlap 有什么作用？

**答案：**
它能减少切分边界导致的语义断裂，让相邻 chunk 之间保留一定上下文连续性。
