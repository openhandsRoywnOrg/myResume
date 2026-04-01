# AI 应用测试：Python 实用做法

## 1. AI 项目为什么更需要测试？

很多人误以为 AI 项目“输出不稳定，所以没法测”。其实真正需要测试的是：

- 业务流程是否正确
- 数据结构是否符合预期
- Prompt 组装逻辑是否正确
- API 接口是否可用
- 错误处理是否稳定

## 2. 应该重点测试什么？

### 可稳定验证的部分
- 数据清洗函数
- Prompt 构造函数
- JSON 解析逻辑
- API schema
- 路由返回结构
- 工具调用编排流程

### 不应过度依赖的部分
- 把 LLM 文本输出逐字断言
- 大量依赖外部 API 的脆弱测试

## 3. pytest 示例

```python
def build_prompt(topic: str) -> str:
    return f"Explain {topic} in simple terms"


def test_build_prompt_contains_topic() -> None:
    prompt = build_prompt("LangGraph")
    assert "LangGraph" in prompt
```

## 4. AI 项目的测试策略

- 优先测试确定性逻辑
- 把 LLM 调用边界封装清楚
- 对输入输出结构做断言
- 对错误场景写测试
- 保持测试快速且稳定

## 5. 面试题

### Q1：AI 项目中哪些部分最值得测试？

**答案：**
最值得测试的是确定性强的代码路径，比如数据处理、接口校验、Prompt 构造、工具编排和异常处理，而不是逐字验证模型自然语言输出。

### Q2：为什么 AI 项目测试不能只靠手工试一下？

**答案：**
因为一旦进入多人协作或持续迭代阶段，没有自动化测试很难发现回归问题，尤其是在工具调用、数据结构和接口层变化时风险很高。
