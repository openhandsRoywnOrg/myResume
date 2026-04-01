# 异常处理、日志与类型注解

## 1. AI 应用最常见的问题不是“语法错”，而是“运行时不稳定”

常见异常包括：
- API 超时
- 速率限制
- 返回结构不符合预期
- JSON 解析失败
- 外部工具不可用

## 2. 异常处理

```python
def parse_answer(payload: dict) -> str:
    try:
        return payload["answer"]
    except KeyError:
        return "模型返回中缺少 answer 字段"
```

## 3. 日志记录

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("start request")
logger.error("model response invalid")
```

## 4. 类型注解

```python
from typing import Any


def normalize_result(data: dict[str, Any]) -> str:
    return str(data.get("result", ""))
```

## 5. 为什么这三者很重要？

- 异常处理：保证失败可控
- 日志：帮助排查线上问题
- 类型注解：帮助团队理解接口约定

## 6. 面试题

### Q1：为什么 AI 项目里不能只靠 print 调试？

**答案：**
因为 print 缺乏结构化、级别控制和持续记录能力。日志系统更适合定位问题、观察链路和上线运行。

### Q2：类型注解会不会降低开发速度？

**答案：**
短期会多写一点代码，但长期能显著降低理解成本和联调成本，尤其在多人协作和复杂返回结构下价值更明显。
