# Backend 目录结构说明

## 目录结构

```
backend/
├── app/                      # 应用主目录
│   ├── __init__.py          # 包初始化
│   ├── main.py              # Flask 应用工厂
│   ├── config.py            # 配置管理
│   ├── extensions.py        # 扩展初始化 (SQLAlchemy 等)
│   │
│   ├── models/              # 数据模型层
│   │   ├── __init__.py
│   │   ├── user.py          # 用户模型
│   │   ├── topic.py         # 知识点模型
│   │   └── question.py      # 面试题模型
│   │
│   ├── services/            # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── topic_service.py # 知识点业务逻辑
│   │   └── question_service.py # 面试题业务逻辑
│   │
│   ├── api/                 # API 路由层
│   │   ├── __init__.py
│   │   └── v1/              # API v1 版本
│   │       ├── __init__.py
│   │       ├── routes.py    # 路由定义
│   │       ├── topics.py    # 知识点 API
│   │       └── questions.py # 面试题 API
│   │
│   ├── hooks/               # 钩子系统
│   │   ├── __init__.py
│   │   ├── registry.py      # 钩子注册表
│   │   └── validators.py    # 验证钩子
│   │
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── exceptions.py    # 自定义异常
│       └── validators.py    # 验证工具
│
├── tests/                   # 测试代码
│   ├── __init__.py
│   ├── conftest.py          # pytest fixtures
│   ├── unit/                # 单元测试
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   └── test_services.py
│   └── integration/         # 集成测试
│       ├── __init__.py
│       └── test_api.py
│
├── requirements.txt         # Python 依赖
└── pytest.ini              # pytest 配置
```

## 分层架构

### 1. Models 层 (数据模型)
- 定义数据结构
- 使用 SQLAlchemy ORM
- 不包含业务逻辑

### 2. Services 层 (业务逻辑)
- 实现核心业务逻辑
- 调用 Models 层
- 触发 Hooks 进行验证

### 3. API 层 (路由)
- 处理 HTTP 请求
- 调用 Services 层
- 返回 JSON 响应

### 4. Hooks 层 (钩子)
- 数据验证
- 审计日志
- 级联操作

## 使用示例

### 创建知识点

```python
# API 层 (api/v1/topics.py)
@api_bp.route('/topics', methods=['POST'])
def create_topic():
    data = request.get_json()
    topic = create_topic_service(**data)
    return jsonify(topic.to_dict()), 201

# Service 层 (services/topic_service.py)
def create_topic_service(title: str, content: str, category: str):
    # 触发验证钩子
    hooks.trigger('before_topic_save', title=title, content=content)
    
    # 创建模型
    topic = Topic(title=title, content=content, category=category)
    db.session.add(topic)
    db.session.commit()
    
    return topic

# Model 层 (models/topic.py)
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
```

### 运行测试

```bash
cd backend

# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/test_project_structure.py -v

# 查看测试覆盖率
pytest --cov=app --cov-report=html
```

### 启动应用

```bash
cd backend

# 开发模式
export FLASK_APP=app.main
export FLASK_ENV=development
flask run

# 或者使用 Python
python -m app.main
```

## 添加新功能的流程

1. **在 Models 层创建数据模型**
   ```bash
   touch backend/app/models/new_feature.py
   ```

2. **在 Services 层实现业务逻辑**
   ```bash
   touch backend/app/services/new_feature_service.py
   ```

3. **在 API 层添加路由**
   ```bash
   touch backend/app/api/v1/new_feature_api.py
   ```

4. **编写测试**
   ```bash
   touch backend/tests/unit/test_new_feature.py
   ```

5. **运行测试验证**
   ```bash
   pytest tests/unit/test_new_feature.py
   ```

## 注意事项

1. **不要跨层调用**
   - API 层 → Service 层 → Model 层
   - 不要：API 层直接调用 Model 层

2. **使用钩子进行验证**
   - 不要在每个函数中重复验证逻辑
   - 使用钩子统一处理

3. **编写测试**
   - 每个新功能必须有测试
   - 测试覆盖率 > 80%

4. **遵循命名规范**
   - 文件：小写，下划线分隔 (user_model.py)
   - 类：大驼峰 (UserProfile)
   - 函数：小写，下划线分隔 (get_user_by_id)
