# 配置管理：env / settings 在 AI 项目中的实践

## 1. 为什么 AI 项目更要重视配置管理？

AI 项目里通常有很多可变配置：

- 模型名称
- API Key
- Base URL
- 温度参数
- 数据库地址
- 向量库索引名
- 日志级别

如果把这些内容硬编码在代码里，后续切环境、换模型、排查问题都会很痛苦。

## 2. 基本原则

- 配置与业务逻辑分离
- 敏感信息放环境变量
- 默认值清晰可见
- 配置入口尽量统一

## 3. 示例

```python
import os

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
API_BASE = os.getenv("API_BASE", "https://api.openai.com/v1")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

## 4. 更推荐的方式：Settings 对象

```python
from pydantic import BaseModel
import os


class AppSettings(BaseModel):
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    api_base: str = os.getenv("API_BASE", "https://api.openai.com/v1")


settings = AppSettings()
```

## 5. 面试题

### Q1：为什么 AI 项目里不应该把 API Key 写进代码？

**答案：**
因为这会造成安全风险，也不利于环境切换和团队协作。更好的方式是使用环境变量或安全配置管理系统。

### Q2：为什么建议统一管理配置入口？

**答案：**
因为配置分散会导致维护困难，统一管理可以降低修改成本，也便于测试和部署。
