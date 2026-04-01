# LangChain / LangGraph 项目的 Python 代码组织

## 1. 为什么这类项目特别容易写乱？

因为 AI 应用通常会同时包含：

- Prompt 模板
- LLM 调用逻辑
- Tool 定义
- Agent 编排
- 状态对象
- API 路由
- 配置和日志

如果全部堆在一个文件里，后续会非常难维护。

## 2. 推荐目录结构

```python
app/
├── api/
├── agents/
├── graphs/
├── prompts/
├── tools/
├── services/
├── schemas/
├── config.py
└── main.py
```

## 3. 组织原则

- Prompt 单独放目录
- Tool 单独维护
- Agent / Graph 只负责编排
- 具体模型调用下沉到 service 层
- API 路由不要直接堆业务逻辑

## 4. 一个简单示例

```python
# services/llm_service.py
def summarize(text: str) -> str:
    return f"summary: {text}"

# agents/summary_agent.py
from services.llm_service import summarize


def run_summary_agent(text: str) -> str:
    return summarize(text)
```

## 5. 面试题

### Q1：为什么 LangChain 项目更需要模块化拆分？

**答案：**
因为这类项目天然包含多个职责层：Prompt、Tool、Agent、Service、API。如果不拆分，复杂度会迅速失控。

### Q2：为什么 Agent 不应该直接承担所有业务逻辑？

**答案：**
Agent 更适合做流程编排和决策，不适合承载全部实现细节。底层逻辑应该放到更稳定、可测试的 service 和 tool 中。
