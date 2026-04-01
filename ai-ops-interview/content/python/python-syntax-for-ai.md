# Python 语法与数据结构（面向 AI 开发）

## 1. 为什么语法基础对 AI 应用重要？

AI 应用开发并不只是“调一个模型 API”。大量日常工作其实是：

- 组织请求参数
- 遍历消息列表
- 拼接 Prompt
- 清洗模型输出
- 转换字典 / JSON / 列表结构

因此，真正高频使用的是 Python 的基础语法与内置数据结构。

## 2. AI 开发中最常用的数据结构

### 列表（list）
适合存储消息、文档片段、候选结果。

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain LangGraph."}
]

for message in messages:
    print(message["role"], message["content"])
```

### 字典（dict）
适合表示结构化配置、模型返回结果、工具参数。

```python
payload = {
    "model": "gpt-4o-mini",
    "temperature": 0.2,
    "stream": False,
}
```

### 集合（set）
适合去重标签、去重文档 ID。

```python
unique_tags = {"rag", "agent", "rag", "langchain"}
print(unique_tags)
```

## 3. 常见语法模式

### 条件判断

```python
def choose_model(is_fast: bool) -> str:
    if is_fast:
        return "gpt-4o-mini"
    return "gpt-4.1"
```

### 列表推导式

```python
questions = ["什么是 RAG？", "什么是 Agent？"]
normalized = [q.strip() for q in questions if q.strip()]
```

### 字典安全读取

```python
result = {"answer": "LangGraph 用于状态化工作流"}
answer = result.get("answer", "")
```

## 4. AI 项目中的典型场景

- 消息列表处理
- Prompt 参数映射
- 模型返回 JSON 清洗
- 批量文档切分后遍历处理
- 对多个工具结果进行聚合

## 5. 面试题

### Q1：为什么 dict 在 AI 应用开发里使用特别多？

**答案：**
因为 API 请求体、模型响应、工具参数、配置对象几乎都是结构化键值对，dict 是最自然的数据表达方式。

### Q2：列表推导式适合用在哪些 AI 开发场景？

**答案：**
适合做文档过滤、消息提取、结果标准化等轻量数据转换场景。但如果逻辑变复杂，应改写成普通循环以提高可读性。
