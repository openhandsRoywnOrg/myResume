# AI Agent 开发指南 - AI DevOps 面试库

## 🎯 项目目标

构建一个专业的 **AI DevOps 面试库网站**，包含：
- 📚 知识点管理系统
- ❓ 面试题库
- 🤖 AI 模拟面试
- 📊 智能评分系统
- 🔐 用户权限管理
- 📈 学习进度追踪

## 📊 项目状态

**当前阶段**: Phase 2 - 功能扩展与优化 (80% 完成)  
**最新进展**: 2025-03-03

### 已完成功能 ✅
- ✅ 知识点展示系统（Markdown 存储）
- ✅ 统一导航栏（4 个主菜单，宽版下拉）
- ✅ 知识地图（思维导图、技术路线、全景图）
- ✅ AI 应用开发菜单（LangChain, LangGraph, MCP, Agent）
- ✅ AI 软件工程菜单（DDD, TDD, 需求驱动）
- ✅ 权限系统（RBAC 模型，JWT 认证）
- ✅ 响应式设计（桌面端 + 移动端）

### 进行中功能 🚧
- 🚧 后端服务集成
- 🚧 数据库实现
- 🚧 用户系统

详细进展查看：[项目进展报告](docs/PROJECT_PROGRESS.md)

## 🧠 Repository Memory

- `/topic/<category>/<topic>` 页面由 `ai-ops-interview/templates/topic.html` 渲染，不是 `content_page.html`。
- Topic 页正文来自 Markdown，并启用了 `markdown` 的 `extra`、`codehilite`、`toc` 扩展，因此样式必须覆盖表格、目录、代码块、列表、blockquote 等结构。
- Topic 页已统一到新版四大导航风格，并使用 `.topic-*` 作用域样式；如果后续继续优化内容页，优先复用 `style.css` 中的共享导航与 `.topic-markdown` 版式规则。
- Topic 页的思维导图是辅助模块，默认收起，位于侧栏 `#topic-mindmap-panel`，不要再恢复为正文前置的大块首屏模块。
- 首页 `templates/index.html` 现在包含独立的 Python 学习专区 `.python-focus-section`，它不是单一卡片，而是一个带说明、CTA 和多入口卡片的独立模块。
- Python 学习内容落在 `ai-ops-interview/content/python/` 下，依赖现有 `get_categories()` 自动进入 topic 分类体系，因此新增 Python 主题时优先往该目录补 Markdown。
- Python 子主题目前已扩展到异步编程、typing/Pydantic、FastAPI 服务开发、AI 应用测试；若继续扩展首页专区，优先保持“AI 应用开发所需 Python 能力”这个边界，不要泛化成完整 Python 教程站。
- Python 专区当前已扩展到 13 个主题，新增方向包括 HTTP 客户端、配置管理、LangChain/LangGraph 项目组织、数据处理与 chunking；后续若继续补充，优先围绕 AI 应用“交付链路”扩展，而不是通用语法堆叠。





## 🏗️ 项目架构

### 目录结构
```
myResume/
├── ai-ops-interview/          # 前端应用（Flask）
│   ├── app.py                 # 主应用（270 行）
│   ├── templates/             # HTML 模板（11 个文件）
│   │   ├── index.html        # 首页
│   │   ├── mindmap.html      # 思维导图
│   │   ├── langchain.html    # LangChain 页面
│   │   ├── doc_driven.html   # 文档驱动开发
│   │   ├── tech_roadmap.html # 技术路线
│   │   ├── ai_devops_landscape.html  # AI DevOps 全景图
│   │   └── content_page.html # 通用内容页
│   ├── static/css/
│   │   └── style.css         # 样式（1276 行）
│   └── content/              # Markdown 内容
│       ├── linux/
│       ├── docker/
│       ├── k8s/
│       └── ...
│
├── backend/                   # 后端服务（开发中）
│   ├── app/
│   │   ├── models/           # 数据模型
│   │   │   └── user.py       # 用户模型（4 角色）
│   │   ├── api/              # API 路由
│   │   │   ├── v1/
│   │   │   └── deps.py       # 认证依赖
│   │   ├── hooks/            # 钩子系统
│   │   ├── services/         # 业务逻辑
│   │   ├── config.py
│   │   ├── main.py
│   │   └── extensions.py
│   └── tests/                # 测试代码
│       ├── unit/
│       │   └── test_permissions.py
│       └── conftest.py
│
├── docs/                      # 项目文档
│   ├── PROJECT_PROGRESS.md   # 项目进展 ⭐
│   ├── ARCHITECTURE_PLAN.md  # 架构设计
│   ├── PERMISSION_TEST_REPORT.md  # 权限测试
│   ├── ISSUE_GUIDELINES.md   # Issue 指南
│   ├── DDD_SPEC.md           # DDD 规范
│   ├── design/               # 设计模板
│   └── requirements/         # 需求模板
│
└── .github/                   # GitHub 配置
    ├── workflows/
    │   └── ci.yml            # CI/CD
    └── ISSUE_TEMPLATE/
        ├── feature_request.md
        ├── bug_report.md
        └── ai_task.md
```

### 在修改代码前必须遵守的规则

#### 1. 文件组织规则
```
✅ 正确：
- 新模型放在 backend/app/models/
- 新 API 放在 backend/app/api/v1/
- 业务逻辑放在 backend/app/services/
- 钩子函数放在 backend/app/hooks/

❌ 错误：
- 所有代码堆在 app.py
- 模型定义在 API 路由文件中
- 业务逻辑在路由处理器中
```

#### 2. 函数编写规则
```python
# ✅ 正确：单一职责，有类型注解
from typing import Optional, List
from app.models.topic import Topic

def get_topic_by_id(topic_id: int) -> Optional[Topic]:
    """根据 ID 获取知识点
    
    Args:
        topic_id: 知识点 ID
        
    Returns:
        Topic 对象或 None
    """
    return Topic.query.get(topic_id)

# ❌ 错误：无类型注解，职责不清
def get_topic(id):
    topic = Topic.query.get(id)
    # 一堆混合逻辑...
    return topic
```

#### 3. 错误处理规则
```python
# ✅ 正确：明确的错误处理
from app.exceptions import TopicNotFoundError, ValidationError

def create_topic(title: str, content: str) -> Topic:
    if not title or len(title) < 3:
        raise ValidationError("Title must be at least 3 characters")
    
    if not content or len(content) < 50:
        raise ValidationError("Content must be at least 50 characters")
    
    topic = Topic(title=title, content=content)
    db.session.add(topic)
    db.session.commit()
    return topic

# ❌ 错误：无错误处理
def create_topic(title, content):
    topic = Topic(title=title, content=content)
    db.session.add(topic)
    db.session.commit()
    return topic
```

#### 4. 钩子使用规则
```python
# ✅ 正确：使用钩子确保数据一致性
from app.hooks import hooks

@hooks.register('before_topic_save')
def validate_topic(topic):
    """验证知识点数据"""
    if not topic.title:
        raise ValueError("Title is required")
    if len(topic.content) < 50:
        raise ValueError("Content too short")
    return True

# 在保存时自动触发
topic.save()  # 会自动调用 validate_topic

# ❌ 错误：在每个地方重复验证
def create_topic(title, content):
    if not title:
        raise ValueError("Title is required")
    # ... 重复的验证逻辑
```

#### 5. 测试编写规则
```python
# ✅ 正确：完整的测试覆盖
import pytest
from app.services.topic_service import create_topic

class TestTopicCreation:
    """测试知识点创建"""
    
    def test_create_valid_topic(self, db):
        """测试创建有效的知识点"""
        topic = create_topic(
            title="Machine Learning",
            content="Machine learning is a subset of AI..."
        )
        assert topic.id is not None
        assert topic.title == "Machine Learning"
    
    def test_create_topic_with_short_title(self, db):
        """测试标题太短时的验证"""
        with pytest.raises(ValidationError):
            create_topic(title="ML", content="Some content...")
    
    def test_create_topic_with_empty_content(self, db):
        """测试内容为空时的验证"""
        with pytest.raises(ValidationError):
            create_topic(title="Valid Title", content="")

# ❌ 错误：无测试或测试不完整
def test_topic():
    # 测试什么？不知道
    pass
```

---

## 📋 Issue 解决流程

### 步骤 1: 理解需求
```markdown
在开始编码前，确认：
- [ ] Issue 要解决什么问题？
- [ ] 验收标准是什么？
- [ ] 影响哪些模块？
- [ ] 需要数据库变更吗？
- [ ] 需要 API 变更吗？
- [ ] 会影响现有功能吗？
```

### 步骤 2: 设计解决方案
```markdown
设计文档（简单 Issue 可以省略）：
1. 需要添加/修改哪些文件？
2. 数据模型如何设计？
3. API 接口如何设计？
4. 需要哪些钩子？
5. 测试策略是什么？
```

### 步骤 3: 实现代码
```markdown
编码检查清单：
- [ ] 遵循项目结构
- [ ] 添加类型注解
- [ ] 编写 docstring
- [ ] 添加错误处理
- [ ] 注册必要的钩子
- [ ] 添加日志记录
- [ ] 考虑向后兼容
```

### 步骤 4: 编写测试
```markdown
测试检查清单：
- [ ] 单元测试覆盖新逻辑
- [ ] 集成测试验证 API
- [ ] 回归测试确保不破坏现有功能
- [ ] 边界条件测试
- [ ] 错误场景测试
- [ ] 测试覆盖率 > 80%
```

### 步骤 5: 验证
```markdown
验证检查清单：
- [ ] 运行所有测试：`pytest`
- [ ] 检查代码规范：`flake8 backend/app`
- [ ] 类型检查：`mypy backend/app`
- [ ] 手动测试功能
- [ ] 检查性能影响
- [ ] 更新文档
```

### 步骤 6: 提交
```markdown
提交检查清单：
- [ ] Commit 信息清晰（使用动词开头）
- [ ] 关联 Issue 编号：`Fixes #123`
- [ ] 代码格式化
- [ ] 无调试代码
- [ ] 无 TODO 注释（或明确说明）
```

---

## 🏗️ 项目架构

### 目录结构
```
backend/
├── app/
│   ├── models/          # 数据模型
│   ├── api/             # API 路由
│   ├── services/        # 业务逻辑
│   ├── hooks/           # 钩子系统
│   └── utils/           # 工具函数
├── tests/               # 测试代码
└── requirements.txt     # 依赖
```

### 模块职责

#### Models (数据模型)
- 只负责数据结构定义
- 不包含业务逻辑
- 使用 SQLAlchemy ORM

```python
# app/models/topic.py
from app import db
from datetime import datetime

class Topic(db.Model):
    __tablename__ = 'topics'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # 关系
    questions = db.relationship('Question', backref='topic', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'created_at': self.created_at.isoformat()
        }
```

#### Services (业务逻辑)
- 实现核心业务逻辑
- 调用钩子进行验证
- 处理事务

```python
# app/services/topic_service.py
from app.models.topic import Topic
from app.hooks import hooks
from app.exceptions import ValidationError

def create_topic(title: str, content: str, category: str) -> Topic:
    """创建知识点
    
    Args:
        title: 标题
        content: 内容
        category: 分类
        
    Returns:
        Topic: 创建的知识点对象
        
    Raises:
        ValidationError: 验证失败时
    """
    # 触发前置钩子
    hooks.trigger('before_topic_save', title=title, content=content)
    
    # 创建对象
    topic = Topic(title=title, content=content, category=category)
    db.session.add(topic)
    db.session.commit()
    
    # 触发后置钩子
    hooks.trigger('after_topic_create', topic=topic)
    
    return topic
```

#### API (路由层)
- 处理 HTTP 请求
- 参数验证
- 调用 Service 层
- 返回 JSON 响应

```python
# app/api/v1/topics.py
from flask import Blueprint, request, jsonify
from app.services.topic_service import create_topic
from app.api.deps import require_auth
from app.exceptions import ValidationError

api = Blueprint('topics', __name__)

@api.route('/topics', methods=['POST'])
@require_auth
def create_topic_api():
    """创建知识点 API"""
    data = request.get_json()
    
    try:
        topic = create_topic(
            title=data.get('title'),
            content=data.get('content'),
            category=data.get('category')
        )
        return jsonify(topic.to_dict()), 201
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
```

#### Hooks (钩子层)
- 数据验证
- 业务规则检查
- 审计日志
- 级联操作

```python
# app/hooks/validators.py
from app.hooks import hooks

@hooks.register('before_topic_save')
def validate_topic_length(title: str, content: str):
    """验证知识点长度"""
    if len(title) < 3:
        raise ValidationError("Title must be at least 3 characters")
    if len(content) < 50:
        raise ValidationError("Content must be at least 50 characters")
    return True

@hooks.register('before_topic_save')
def sanitize_topic_content(title: str, content: str):
    """清理内容（去除 HTML 标签等）"""
    # 清理逻辑
    return True
```

---

## 🔐 权限规则

### 角色定义
- **Guest**: 未认证用户，只能查看公开内容
- **User**: 认证用户，可以创建笔记、参与模拟面试
- **Admin**: 管理员，可以管理知识点、用户
- **Super Admin**: 超级管理员，所有权限

### 权限检查示例
```python
from app.api.deps import require_role

@api.route('/topics/<int:topic_id>', methods=['DELETE'])
@require_role('admin')
def delete_topic(topic_id: int):
    """删除知识点（仅管理员）"""
    topic = Topic.query.get_or_404(topic_id)
    db.session.delete(topic)
    db.session.commit()
    return jsonify({'message': 'Topic deleted'})
```

---

## 📊 数据库设计

### 核心表

#### users (用户表)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### topics (知识点表)
```sql
CREATE TABLE topics (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### questions (面试题表)
```sql
CREATE TABLE questions (
    id INTEGER PRIMARY KEY,
    topic_id INTEGER REFERENCES topics(id),
    question_text TEXT NOT NULL,
    answer_hint TEXT,
    difficulty VARCHAR(20) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### interviews (模拟面试表)
```sql
CREATE TABLE interviews (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    score DECIMAL(5,2),
    feedback TEXT
);
```

---

## 🧪 测试规范

### 测试文件组织
```
tests/
├── unit/              # 单元测试
│   ├── test_models.py
│   ├── test_services.py
│   └── test_hooks.py
├── integration/       # 集成测试
│   ├── test_api.py
│   └── test_auth.py
└── e2e/              # 端到端测试
    └── test_workflows.py
```

### 测试命名规范
```python
def test_<功能>_<场景>_<预期结果>():
    # 示例
    def test_create_topic_with_valid_data_returns_topic():
    def test_create_topic_with_short_title_raises_error():
    def test_delete_topic_as_admin_succeeds():
    def test_delete_topic_as_user_fails():
```

### Fixture 使用
```python
# conftest.py
import pytest
from app import create_app, db

@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.fixture
def auth_token(client):
    """创建认证 token"""
    response = client.post('/api/v1/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    return response.json['access_token']
```

---

## 🚨 常见错误

### ❌ 错误 1: 所有逻辑写在 app.py
```python
# 错误示例
@app.route('/topics', methods=['POST'])
def create_topic():
    data = request.json
    # 100 行混合了验证、业务逻辑、数据库操作的代码
    # ...
    return jsonify(topic)
```

### ✅ 正确做法：分层架构
```python
# app.py - 只负责路由
@app.route('/topics', methods=['POST'])
@require_auth
def create_topic_api():
    data = request.get_json()
    topic = create_topic_service(**data)
    return jsonify(topic.to_dict()), 201

# services/topic_service.py - 业务逻辑
def create_topic_service(title, content, category):
    # 验证、钩子、数据库操作
    pass
```

### ❌ 错误 2: 无测试
```python
# 没有测试文件
# 或者
def test_something():
    assert True  # 无意义测试
```

### ✅ 正确做法：完整测试
```python
class TestTopicService:
    def test_create_valid_topic(self):
        # 测试正常场景
        pass
    
    def test_create_topic_with_invalid_data(self):
        # 测试错误场景
        pass
    
    def test_create_topic_triggers_hooks(self):
        # 测试钩子触发
        pass
```

### ❌ 错误 3: 硬编码配置
```python
# 错误
DATABASE_URL = "postgresql://localhost/mydb"
SECRET_KEY = "my-secret-key"
```

### ✅ 正确做法：使用配置管理
```python
# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
```

---

## 📚 参考资源

- [Flask 官方文档](https://flask.palletsprojects.com/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [pytest 文档](https://docs.pytest.org/)
- [Python 类型注解](https://docs.python.org/3/library/typing.html)

---

## 💡 提示

当你（AI Agent）在解决 Issue 时：

1. **先读这个文档**，了解项目规范
2. **查看现有代码**，保持一致的风格
3. **编写测试**，确保质量
4. **使用钩子**，不要重复代码
5. **考虑扩展性**，不要硬编码
6. **添加文档**，帮助后来者

记住：**代码质量 > 代码数量**
