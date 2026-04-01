# 函数、类、模块与包组织

## 1. 为什么 AI 项目更需要结构化代码？

随着项目从单脚本演进到 Agent、RAG、工具调用、Web API，多数问题不再是“能不能跑”，而是“能不能维护”。

常见目录拆分示例：

```python
app/
├── agents/
├── tools/
├── services/
├── prompts/
├── schemas/
└── config.py
```

## 2. 函数适合什么场景？

函数适合：
- 格式化 Prompt
- 解析模型输出
- 执行单一工具逻辑
- 封装可复用的小步骤

```python
def build_summary_prompt(topic: str, audience: str) -> str:
    return f"请面向{audience}总结 {topic} 的核心概念与实践建议。"
```

## 3. 类适合什么场景？

类适合：
- 封装有状态对象
- 管理服务依赖
- 聚合一组相关方法

```python
class ChatService:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def ask(self, prompt: str) -> str:
        return self.llm_client.invoke(prompt)
```

## 4. 模块拆分原则

- 一个模块只聚焦一类职责
- 不要把 Prompt、HTTP、业务逻辑都堆在一个文件里
- 配置单独抽离
- Schema / 数据结构单独维护

## 5. 面试题

### Q1：AI 项目里什么时候该从函数升级到类？

**答案：**
当逻辑开始依赖共享状态、外部客户端、配置对象，或者多个方法围绕同一个领域对象组织时，就更适合用类。

### Q2：为什么 Prompt 不建议散落在业务代码里？

**答案：**
因为 Prompt 也是项目资产。单独管理可以降低修改成本，便于测试、版本控制和复用。
