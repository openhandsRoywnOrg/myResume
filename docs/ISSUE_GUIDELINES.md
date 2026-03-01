# Issue 解决指南

## 📋 解决流程

### 1️⃣ 理解需求 (5-10 分钟)

**阅读 Issue 描述**
- [ ] 问题是什么？
- [ ] 期望的解决方案？
- [ ] 验收标准是什么？
- [ ] 影响范围有多大？

**提问澄清**（如有需要）
- 在 Issue 下评论询问不清楚的地方
- 确认技术选型
- 确认优先级

### 2️⃣ 设计方案 (10-15 分钟)

**简单 Issue**（可以直接编码）
- 影响单个文件
- 不修改数据结构
- 不添加新功能

**中等 Issue**（需要简单设计）
- 影响多个模块
- 需要数据库变更
- 需要 API 设计

**复杂 Issue**（需要详细设计文档）
- 系统级功能
- 重大架构变更
- 性能优化

**设计检查清单**
```markdown
## 设计文档

### 影响模块
- [ ] 列出所有需要修改的文件

### 数据模型
- [ ] 是否需要新的数据库表？
- [ ] 是否需要修改现有表？
- [ ] 是否需要数据迁移？

### API 设计
- [ ] 是否需要新的 API 端点？
- [ ] 是否需要修改现有 API？
- [ ] API 文档是否更新？

### 钩子
- [ ] 是否需要添加新的钩子？
- [ ] 是否需要修改现有钩子？

### 向后兼容
- [ ] 是否破坏现有功能？
- [ ] 是否需要迁移脚本？
- [ ] 是否需要版本控制？
```

### 3️⃣ 实现代码 (30 分钟 - 数小时)

**编码规范**
```python
# ✅ 正确示例
from typing import Optional, List
from app.models.topic import Topic
from app.exceptions import ValidationError

def create_topic(title: str, content: str, category: str) -> Topic:
    """创建知识点
    
    Args:
        title: 知识点标题（至少 3 个字符）
        content: 知识点内容（至少 50 个字符）
        category: 分类标识
        
    Returns:
        Topic: 创建的知识点对象
        
    Raises:
        ValidationError: 当验证失败时
    """
    # 触发前置钩子
    hooks.trigger('before_topic_save', title=title, content=content)
    
    # 业务逻辑
    topic = Topic(title=title, content=content, category=category)
    db.session.add(topic)
    db.session.commit()
    
    # 触发后置钩子
    hooks.trigger('after_topic_create', topic=topic)
    
    return topic
```

**编码检查清单**
- [ ] 遵循项目结构
- [ ] 添加类型注解
- [ ] 编写 docstring
- [ ] 添加错误处理
- [ ] 注册必要的钩子
- [ ] 添加日志记录
- [ ] 考虑向后兼容
- [ ] 无硬编码值
- [ ] 无调试代码

### 4️⃣ 编写测试 (20-30 分钟)

**测试金字塔**
```
        /\
       /  \
      / E2E \      端到端测试 (10%)
     /______\
    /        \
   /Integration\   集成测试 (20%)
  /______________\
 /                \
/    Unit Tests    \  单元测试 (70%)
--------------------
```

**单元测试示例**
```python
class TestTopicCreation:
    """测试知识点创建"""
    
    def test_create_valid_topic(self, database):
        """测试正常场景"""
        topic = create_topic(
            title="Valid Title",
            content="Valid content with sufficient length...",
            category="test"
        )
        assert topic.id is not None
    
    def test_create_topic_with_short_title(self, database):
        """测试异常场景"""
        with pytest.raises(ValidationError):
            create_topic(
                title="AB",  # 太短
                content="Valid content...",
                category="test"
            )
```

**集成测试示例**
```python
class TestTopicAPI:
    """测试知识点 API"""
    
    def test_create_topic_api(self, auth_client):
        """测试创建知识点 API"""
        response = auth_client.post(
            '/api/v1/topics',
            json={
                'title': 'Test Topic',
                'content': 'Valid content...',
                'category': 'test'
            }
        )
        assert response.status_code == 201
        assert 'id' in response.json()
```

**测试检查清单**
- [ ] 单元测试覆盖新逻辑
- [ ] 集成测试验证 API
- [ ] 回归测试确保不破坏现有功能
- [ ] 边界条件测试
- [ ] 错误场景测试
- [ ] 测试覆盖率 > 80%

### 5️⃣ 验证 (15-20 分钟)

**本地验证**
```bash
# 运行所有测试
pytest

# 检查代码规范
flake8 backend/app

# 类型检查
mypy backend/app

# 运行特定测试
pytest tests/unit/test_topic_service.py -v

# 查看测试覆盖率
pytest --cov=app --cov-report=html
```

**验证检查清单**
- [ ] 所有测试通过
- [ ] 代码规范检查通过
- [ ] 类型检查通过
- [ ] 手动测试功能正常
- [ ] 性能无明显下降
- [ ] 文档已更新

### 6️⃣ 提交代码 (5-10 分钟)

**Commit 规范**
```bash
# 格式
<type>(<scope>): <subject>

# 示例
feat(topic): add mindmap visualization feature
fix(api): resolve 404 error in topic endpoint
docs(readme): update installation instructions
test(auth): add unit tests for JWT validation
refactor(service): extract validation logic to hooks
```

**Commit 类型**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具

**提交检查清单**
- [ ] Commit 信息清晰
- [ ] 关联 Issue 编号：`Fixes #123`
- [ ] 代码已格式化
- [ ] 无调试代码
- [ ] 无 TODO（或明确说明）

### 7️⃣ 创建 PR (10 分钟)

**PR 模板**
```markdown
## 描述
简要描述这个 PR 做了什么

## 相关 Issue
Fixes #123

## 变更类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 重构
- [ ] 文档更新
- [ ] 测试添加

## 测试
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动测试通过

## 截图（如适用）
添加功能截图

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 测试覆盖率 > 80%
- [ ] 文档已更新
- [ ] 无破坏性变更
```

## 🚨 常见陷阱

### 陷阱 1: 跳过测试
```python
# ❌ 错误：无测试
def new_feature():
    pass

# ✅ 正确：先写测试
def test_new_feature():
    assert new_feature() == expected_result
```

### 陷阱 2: 忽略钩子
```python
# ❌ 错误：直接操作数据库
topic = Topic(title=title)
db.session.add(topic)
db.session.commit()

# ✅ 正确：使用钩子
hooks.trigger('before_topic_save', title=title)
topic = Topic(title=title)
db.session.add(topic)
db.session.commit()
hooks.trigger('after_topic_create', topic=topic)
```

### 陷阱 3: 大 Commit
```bash
# ❌ 错误：一次性提交所有变更
git commit -m "Update everything"

# ✅ 正确：小步提交
git commit -m "feat: add topic model"
git commit -m "feat: add topic service"
git commit -m "test: add topic tests"
```

### 陷阱 4: 无文档
```python
# ❌ 错误：无文档
def calc(a, b, c):
    return a * b + c

# ✅ 正确：有文档
def calculate_total_score(base: float, multiplier: float, bonus: float) -> float:
    """计算总分
    
    Args:
        base: 基础分
        multiplier: 倍数
        bonus: 奖励分
        
    Returns:
        计算后的总分
    """
    return base * multiplier + bonus
```

## 📚 参考资源

- [AGENTS.md](./AGENTS.md) - AI Agent 开发指南
- [ARCHITECTURE_PLAN.md](./ARCHITECTURE_PLAN.md) - 架构设计文档
- [pytest 文档](https://docs.pytest.org/)
- [Flask 最佳实践](https://flask.palletsprojects.com/patterns/)
