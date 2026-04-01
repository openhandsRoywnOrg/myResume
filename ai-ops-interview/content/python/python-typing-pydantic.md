# typing 与 Pydantic：让 AI 应用数据结构更清晰

## 1. 为什么 AI 项目特别需要明确的数据结构？

AI 项目通常会在多个层之间传递复杂对象：

- 用户输入
- Prompt 参数
- 模型响应
- 工具调用参数
- API 返回体

如果结构不明确，最容易出现字段缺失、类型错误、联调困难的问题。

## 2. typing 的作用

```python
from typing import Any


def build_payload(model: str, messages: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "model": model,
        "messages": messages,
    }
```

typing 的价值：
- 让函数输入输出更清楚
- 提升 IDE 补全与检查能力
- 降低多人协作理解成本

## 3. Pydantic 的作用

Pydantic 适合做：
- API 请求/响应校验
- 模型输出结构化解析
- 配置对象管理
- 工具调用参数验证

```python
from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.2
```

## 4. AI 场景中的典型使用方式

- 定义聊天接口输入结构
- 约束 Agent 工具参数
- 解析结构化 JSON 输出
- 管理环境配置对象

## 5. 面试题

### Q1：为什么仅靠 dict 不够？

**答案：**
因为 dict 灵活但不受约束，项目规模变大后容易出现结构漂移。typing 和 Pydantic 能让数据结构更稳定、更可维护。

### Q2：Pydantic 在 AI 项目中最有价值的点是什么？

**答案：**
它可以把“隐式约定”变成“显式约束”，特别适合接口层、配置层和结构化输出解析场景。
