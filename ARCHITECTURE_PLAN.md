# AI DevOps 面试库 - 项目架构重构方案

## 📊 当前项目分析

### 现状
- **代码结构**: 单一 Flask 应用 (84 行 app.py)
- **功能**: 知识点展示、搜索、思维导图
- **问题**: 
  - 所有逻辑在单个文件
  - 无测试覆盖
  - 无代码规范约束
  - 无数据库 (文件系统)
  - 无权限系统
  - 难以扩展

### 风险
1. **技术债务累积**: AI 生成的代码没有规范，容易跑偏
2. **重构困难**: 没有测试，不敢大改
3. **扩展性差**: 单体架构，添加新功能困难
4. **质量问题**: 无代码审查标准

---

## 🏗️ 目标架构设计

### 项目愿景
做一个专业的 **AI DevOps 面试库网站**，包含：
- ✅ 知识点管理系统
- ✅ 面试题库
- ✅ AI 模拟面试
- ✅ 智能评分系统
- ✅ 用户权限管理
- ✅ 学习进度追踪

### 架构原则
1. **模块化**: 功能解耦，独立开发
2. **可测试**: 单元测试覆盖率 > 80%
3. **可扩展**: 插件化设计，易于添加新功能
4. **可维护**: 代码规范、文档齐全
5. **安全性**: 权限控制、数据验证

---

## 📁 推荐项目结构

```
myResume/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # CI/CD 流程
│   │   ├── tests.yml           # 测试自动化
│   │   └── openhands-resolver.yml
│   └── ISSUE_TEMPLATE/
│       └── feature_request.md  # Issue 模板
│
├── backend/                     # 后端服务
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # Flask 应用入口
│   │   ├── config.py           # 配置管理
│   │   ├── extensions.py       # 扩展初始化
│   │   │
│   │   ├── models/             # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py         # 用户模型
│   │   │   ├── topic.py        # 知识点模型
│   │   │   ├── question.py     # 面试题模型
│   │   │   ├── interview.py    # 模拟面试模型
│   │   │   └── score.py        # 评分模型
│   │   │
│   │   ├── api/                # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── topics.py
│   │   │   │   ├── questions.py
│   │   │   │   ├── interviews.py
│   │   │   │   └── users.py
│   │   │   └── deps.py         # 依赖注入
│   │   │
│   │   ├── services/           # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── topic_service.py
│   │   │   ├── question_service.py
│   │   │   ├── interview_service.py
│   │   │   ├── scoring_service.py
│   │   │   └── ai_service.py   # AI 集成
│   │   │
│   │   ├── hooks/              # 钩子系统
│   │   │   ├── __init__.py
│   │   │   ├── pre_save.py     # 保存前钩子
│   │   │   ├── post_update.py  # 更新后钩子
│   │   │   └── validators.py   # 数据验证
│   │   │
│   │   └── utils/              # 工具函数
│   │       ├── __init__.py
│   │       ├── auth.py         # 认证工具
│   │       └── validators.py   # 验证工具
│   │
│   ├── tests/                  # 测试目录
│   │   ├── __init__.py
│   │   ├── conftest.py         # pytest 配置
│   │   ├── unit/
│   │   │   ├── test_models.py
│   │   │   ├── test_services.py
│   │   │   └── test_hooks.py
│   │   ├── integration/
│   │   │   ├── test_api.py
│   │   │   └── test_auth.py
│   │   └── e2e/
│   │       └── test_workflows.py
│   │
│   ├── requirements.txt
│   ├── pytest.ini
│   └── Dockerfile
│
├── frontend/                    # 前端 (可选 React/Vue)
│   ├── src/
│   ├── public/
│   └── package.json
│
├── scripts/                     # 自动化脚本
│   ├── setup_db.py
│   ├── seed_data.py
│   └── run_tests.sh
│
├── docs/                        # 文档
│   ├── architecture.md
│   ├── api.md
│   ├── development.md
│   └── issue-guidelines.md
│
├── .env.example                 # 环境变量示例
├── .gitignore
├── docker-compose.yml
├── Makefile                     # 常用命令
└── README.md
```

---

## 🔧 核心机制设计

### 1. 钩子系统 (Hooks)

**目的**: 在关键操作前后执行逻辑，确保数据一致性和业务规则

```python
# backend/app/hooks/pre_save.py
from functools import wraps

class HookRegistry:
    def __init__(self):
        self.hooks = {}
    
    def register(self, event, callback):
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(callback)
    
    def trigger(self, event, *args, **kwargs):
        results = []
        for callback in self.hooks.get(event, []):
            results.append(callback(*args, **kwargs))
        return results

# 全局钩子注册表
hooks = HookRegistry()

# 使用示例
@hooks.register('before_topic_save')
def validate_topic_content(topic):
    """验证知识点内容完整性"""
    if not topic.title:
        raise ValueError("Topic title is required")
    if len(topic.content) < 50:
        raise ValueError("Topic content too short")
    return True

@hooks.register('before_question_save')
def link_question_to_topic(question):
    """自动关联问题到知识点"""
    if not question.topic_id:
        question.topic_id = auto_detect_topic(question.content)
    return True
```

### 2. 回归测试系统

**目的**: 确保新功能不破坏现有功能

```python
# backend/app/tests/regression/test_topic_workflow.py
import pytest

class TestTopicWorkflow:
    """知识点工作流回归测试"""
    
    def test_create_topic_with_valid_content(self, client, auth_token):
        """测试创建有效知识点"""
        response = client.post(
            '/api/v1/topics',
            json={
                'title': 'ML Basics',
                'content': 'Machine learning is...',
                'category': 'ai-ml'
            },
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert response.status_code == 201
        assert 'id' in response.json()
    
    def test_create_topic_with_invalid_content(self, client, auth_token):
        """测试创建无效知识点（回归测试）"""
        response = client.post(
            '/api/v1/topics',
            json={'title': 'A'},  # 标题太短
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert response.status_code == 400
        assert 'validation_error' in response.json()
    
    def test_update_topic_preserves_history(self, client, auth_token, topic_id):
        """测试更新知识点保留历史（回归测试）"""
        # 先获取原始内容
        original = client.get(f'/api/v1/topics/{topic_id}')
        
        # 更新
        response = client.patch(
            f'/api/v1/topics/{topic_id}',
            json={'content': 'Updated content...'},
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert response.status_code == 200
        
        # 验证历史存在
        history = client.get(f'/api/v1/topics/{topic_id}/history')
        assert len(history.json()) >= 2
```

### 3. Issue 解决规范

**目的**: 确保 AI 生成的代码符合项目标准

```markdown
## Issue 解决流程

### 1. 理解需求
- [ ] 阅读 Issue 描述
- [ ] 确认验收标准 (Acceptance Criteria)
- [ ] 识别影响范围

### 2. 设计解决方案
- [ ] 选择正确的模块 (models/services/api)
- [ ] 考虑是否需要数据库迁移
- [ ] 考虑是否需要 API 变更
- [ ] 考虑向后兼容性

### 3. 实现代码
- [ ] 遵循代码规范 (PEP 8, 类型注解)
- [ ] 添加必要的钩子
- [ ] 添加错误处理
- [ ] 添加日志记录

### 4. 编写测试
- [ ] 单元测试 (覆盖新逻辑)
- [ ] 集成测试 (API 测试)
- [ ] 回归测试 (确保不破坏现有功能)
- [ ] 测试覆盖率 > 80%

### 5. 验证
- [ ] 本地运行所有测试
- [ ] 检查代码规范 (flake8, mypy)
- [ ] 手动测试功能
- [ ] 更新文档

### 6. 提交
- [ ] Commit 信息清晰
- [ ] 关联 Issue 编号
- [ ] 创建 PR 描述
- [ ] 请求 Code Review
```

### 4. 代码审查清单

```markdown
## Code Review Checklist

### 代码质量
- [ ] 遵循 PEP 8 规范
- [ ] 有类型注解
- [ ] 函数单一职责
- [ ] 无重复代码 (DRY)
- [ ] 适当的错误处理

### 测试
- [ ] 单元测试覆盖新功能
- [ ] 回归测试通过
- [ ] 测试覆盖率未下降
- [ ] 边界条件测试

### 安全
- [ ] 输入验证
- [ ] SQL 注入防护
- [ ] XSS 防护
- [ ] 权限检查
- [ ] 敏感数据加密

### 性能
- [ ] 无 N+1 查询
- [ ] 适当的索引
- [ ] 缓存策略
- [ ] 资源释放

### 文档
- [ ] 函数 docstring
- [ ] API 文档更新
- [ ] CHANGELOG 更新
```

---

## 📋 分阶段实施计划

### 第一阶段：基础架构 (1-2 周)
1. **重构项目结构**
   - 拆分 app.py 为模块化结构
   - 添加配置管理
   - 设置数据库 (PostgreSQL)

2. **建立测试基础设施**
   - 配置 pytest
   - 添加 CI/CD 流程
   - 编写基础测试

3. **制定规范文档**
   - 代码规范
   - Issue 解决流程
   - Code Review 清单

### 第二阶段：核心功能 (2-3 周)
1. **实现钩子系统**
   - 数据验证钩子
   - 业务逻辑钩子
   - 审计日志钩子

2. **完善测试覆盖**
   - 单元测试 > 80%
   - 集成测试
   - 回归测试套件

3. **添加权限系统**
   - 用户认证 (JWT)
   - 角色管理
   - 资源权限

### 第三阶段：高级功能 (3-4 周)
1. **AI 模拟面试**
   - 集成 LLM API
   - 面试流程管理
   - 实时反馈

2. **评分系统**
   - 评分模型
   - 多维度评估
   - 进度追踪

3. **性能优化**
   - 缓存策略
   - 数据库优化
   - 前端优化

---

## 🛠️ 立即行动项

### 1. 创建 AGENTS.md 文件
让 AI 了解项目规范和架构

### 2. 添加 Issue 模板
确保 Issue 描述清晰

### 3. 配置 GitHub Actions
自动化测试和部署

### 4. 创建初始测试
建立测试基准

### 5. 文档化当前功能
为后续重构做准备

---

## 📚 参考资源

- [Flask 最佳实践](https://flask.palletsprojects.com/en/2.3.x/patterns/)
- [pytest 文档](https://docs.pytest.org/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [12-Factor App](https://12factor.net/)
