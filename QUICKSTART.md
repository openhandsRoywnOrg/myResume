# 🚀 快速开始指南

## 立即可以做的事情

### 1. 将文档添加到项目

将以下文件复制到你的项目根目录：

```bash
# 核心文档
ARCHITECTURE_PLAN.md      # 架构设计
AGENTS.md                 # AI Agent 指南
README_REFACTORING.md     # 重构总结

# GitHub 配置
.github/
├── ISSUE_TEMPLATE/
│   ├── feature_request.md
│   ├── bug_report.md
│   └── ai_task.md
└── workflows/
    └── ci.yml

# 测试配置
backend/
├── pytest.ini
└── tests/
    ├── conftest.py
    └── unit/
        └── test_topic_service.py

# 开发文档
docs/
└── ISSUE_GUIDELINES.md
```

### 2. 立即生效的改进

#### ✅ 使用 Issue 模板
创建新 Issue 时，选择对应的模板：
- 功能请求 → `feature_request.md`
- Bug 报告 → `bug_report.md`
- AI 任务 → `ai_task.md`

#### ✅ 遵循 Issue 解决流程
解决任何 Issue 时，按照这个流程：

```markdown
1. 理解需求 (5-10 分钟)
   - 阅读 Issue 描述
   - 确认验收标准

2. 设计方案 (10-15 分钟)
   - 确定影响范围
   - 列出需要修改的文件

3. 实现代码 (30 分钟 - 数小时)
   - 遵循 AGENTS.md 规范
   - 添加类型注解
   - 编写 docstring

4. 编写测试 (20-30 分钟)
   - 单元测试
   - 集成测试
   - 回归测试

5. 验证 (15-20 分钟)
   - 运行 pytest
   - 检查 flake8
   - 手动测试

6. 提交代码 (5-10 分钟)
   - 清晰的 commit 信息
   - 关联 Issue 编号
```

#### ✅ 使用钩子机制
在添加新功能时，考虑添加钩子：

```python
from app.hooks import hooks

# 注册验证钩子
@hooks.register('before_topic_save')
def validate_topic(topic_data):
    if len(topic_data['title']) < 3:
        raise ValidationError("Title too short")
    return True

# 使用钩子
hooks.trigger('before_topic_save', title=title, content=content)
```

#### ✅ 编写测试
为每个新功能编写测试：

```python
def test_new_feature():
    """测试新功能的正常场景"""
    result = new_feature(input_data)
    assert result == expected_output

def test_new_feature_with_invalid_input():
    """测试新功能的异常场景"""
    with pytest.raises(ValidationError):
        new_feature(invalid_input)
```

### 3. 配置 CI/CD

#### 步骤 1: 添加 Secrets
在 GitHub 仓库设置中添加：
```
Settings → Secrets and variables → Actions

- DOCKER_USERNAME: 你的 Docker Hub 用户名
- DOCKER_PASSWORD: Docker Hub token
- VERCEL_TOKEN: Vercel API token
- VERCEL_ORG_ID: Vercel 组织 ID
- VERCEL_PROJECT_ID: Vercel 项目 ID
```

#### 步骤 2: 启用 GitHub Actions
```bash
# 推送代码后，CI/CD 会自动运行
git push origin main

# 查看运行状态
https://github.com/your-org/myResume/actions
```

### 4. 运行测试

#### 本地测试
```bash
cd backend

# 安装依赖
pip install -r requirements.txt
pip install pytest pytest-cov flake8 mypy

# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/test_topic_service.py -v

# 查看覆盖率
pytest --cov=app --cov-report=html

# 检查代码规范
flake8 app

# 类型检查
mypy app
```

### 5. 代码规范检查清单

在提交代码前，检查：

```markdown
## 代码质量
- [ ] 有类型注解
- [ ] 有 docstring
- [ ] 遵循 PEP 8
- [ ] 函数单一职责
- [ ] 无重复代码

## 测试
- [ ] 单元测试通过
- [ ] 测试覆盖率 > 80%
- [ ] 边界条件测试
- [ ] 错误场景测试

## 安全
- [ ] 输入验证
- [ ] SQL 注入防护
- [ ] 权限检查
- [ ] 敏感数据处理

## 文档
- [ ] 函数文档
- [ ] API 文档
- [ ] CHANGELOG 更新
```

---

## 📋 常用命令

### 开发命令
```bash
# 运行应用
cd backend
python app/main.py

# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html

# 代码规范检查
flake8 app --max-line-length=127

# 类型检查
mypy app --ignore-missing-imports

# 格式化代码
black app

# 排序 imports
isort app
```

### Git 命令
```bash
# 创建功能分支
git checkout -b feature/new-feature

# 提交代码
git add .
git commit -m "feat: add new feature"

# 推送分支
git push origin feature/new-feature

# 查看提交历史
git log --oneline --graph
```

---

## 🎯 第一个任务

### 任务：重构 app.py

#### 目标
将当前的 `app.py` 拆分为模块化结构

#### 步骤

1. **创建目录结构**
```bash
mkdir -p backend/app/{models,api,services,hooks,utils}
touch backend/app/__init__.py
touch backend/app/{models,api,services,hooks,utils}/__init__.py
```

2. **移动模型**
```python
# backend/app/models/topic.py
from app import db
from datetime import datetime

class Topic(db.Model):
    __tablename__ = 'topics'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

3. **移动服务**
```python
# backend/app/services/topic_service.py
from app.models.topic import Topic
from app.hooks import hooks

def create_topic(title: str, content: str, category: str) -> Topic:
    hooks.trigger('before_topic_save', title=title, content=content)
    
    topic = Topic(title=title, content=content, category=category)
    db.session.add(topic)
    db.session.commit()
    
    hooks.trigger('after_topic_create', topic=topic)
    return topic
```

4. **移动 API 路由**
```python
# backend/app/api/v1/topics.py
from flask import Blueprint, request, jsonify
from app.services.topic_service import create_topic

api = Blueprint('topics', __name__)

@api.route('/topics', methods=['POST'])
def create_topic_api():
    data = request.get_json()
    topic = create_topic(**data)
    return jsonify(topic.to_dict()), 201
```

5. **更新主应用**
```python
# backend/app/main.py
from flask import Flask
from app.api.v1.topics import api as topics_api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(topics_api, url_prefix='/api/v1')
    return app
```

6. **编写测试**
```python
# tests/unit/test_topic_service.py
def test_create_topic():
    topic = create_topic(
        title="Test",
        content="Valid content...",
        category="test"
    )
    assert topic.id is not None
```

---

## 🆘 需要帮助？

### 常见问题

**Q: 如何开始重构？**
A: 从最小的模块开始，比如先重构 models，再重构 services，最后重构 API。

**Q: 如何保证不破坏现有功能？**
A: 编写充分的回归测试，确保每个功能都有测试覆盖。

**Q: AI 生成的代码不符合规范怎么办？**
A: 使用 AGENTS.md 指导 AI，并人工 Review 和优化代码。

**Q: 如何添加新的钩子？**
A: 在 `backend/app/hooks/` 目录下创建新的钩子文件，使用 `@hooks.register()` 装饰器。

### 资源链接

- [Flask 文档](https://flask.palletsprojects.com/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [pytest 文档](https://docs.pytest.org/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

---

## ✅ 检查清单

在开始重构前，确保：

- [ ] 已阅读 AGENTS.md
- [ ] 已阅读 ARCHITECTURE_PLAN.md
- [ ] 已了解 Issue 解决流程
- [ ] 已配置本地开发环境
- [ ] 已安装所有依赖
- [ ] 已运行现有测试
- [ ] 已备份当前代码

祝重构顺利！🚀
