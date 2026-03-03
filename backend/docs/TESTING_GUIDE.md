# 🧪 测试指南

## 📋 测试目录结构

```
backend/tests/
├── __init__.py
├── conftest.py              # 共享 fixtures
├── unit/                    # 单元测试
│   ├── __init__.py
│   └── test_permissions.py  # 权限系统测试
└── integration/             # 集成测试
    └── __init__.py
```

## 🎯 测试策略

### 单元测试 (Unit Tests)
- **位置**: `tests/unit/`
- **目标**: 测试单个函数、类或模块
- **特点**: 快速、独立、无外部依赖
- **覆盖率目标**: > 90%

### 集成测试 (Integration Tests)
- **位置**: `tests/integration/`
- **目标**: 测试模块间交互和 API 端点
- **特点**: 验证组件协作、数据库交互
- **覆盖率目标**: > 80%

## 🚀 运行测试

### 运行所有测试
```bash
cd backend
python -m pytest tests/ -v
```

### 运行单元测试
```bash
python -m pytest tests/unit/ -v
```

### 运行集成测试
```bash
python -m pytest tests/integration/ -v
```

### 运行特定测试文件
```bash
python -m pytest tests/unit/test_permissions.py -v
```

### 运行特定测试类
```bash
python -m pytest tests/unit/test_permissions.py::TestUserModel -v
```

### 运行特定测试函数
```bash
python -m pytest tests/unit/test_permissions.py::TestUserModel::test_create_user -v
```

### 带覆盖率报告
```bash
python -m pytest tests/ -v --cov=app --cov-report=html
```

查看覆盖率报告：
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## 📝 测试编写规范

### 测试文件命名
- 文件名：`test_<module>.py`
- 类名：`Test<Module>`
- 函数名：`test_<function>_<scenario>_<expected>`

示例：
```python
# test_permissions.py
class TestUserModel:
    def test_create_user_with_valid_data(self):
        """测试使用有效数据创建用户"""
        pass
    
    def test_create_user_with_duplicate_email(self):
        """测试创建重复邮箱的用户"""
        pass
```

### 测试结构 (AAA 模式)
```python
def test_user_creation():
    # Arrange - 准备数据
    user = User(username='test', email='test@example.com')
    user.set_password('password123')
    
    # Act - 执行操作
    db.session.add(user)
    db.session.commit()
    
    # Assert - 验证结果
    assert user.id is not None
    assert user.username == 'test'
```

### 使用 Fixtures
```python
# conftest.py
@pytest.fixture
def sample_user(database):
    user = User(username='test', email='test@example.com')
    user.set_password('password123')
    database.session.add(user)
    database.session.commit()
    return user

# test_file.py
def test_user_permissions(sample_user):
    assert sample_user.has_permission('user')
```

## 🔧 Fixtures 说明

### 内置 Fixtures

#### `app`
创建测试应用实例
```python
@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
```

#### `database`
为每个测试提供干净的数据库
```python
@pytest.fixture(scope='function')
def database(app):
    with app.app_context():
        db.session.begin_nested()
        yield db
        db.session.rollback()
```

#### `client`
Flask 测试客户端
```python
@pytest.fixture
def client(app):
    return app.test_client()
```

### 自定义 Fixtures

#### `auth_client`
已认证的测试客户端
```python
@pytest.fixture
def auth_client(client, database):
    # 创建用户并登录
    user = User(username='testuser', email='test@example.com', role='user')
    user.set_password('password123')
    database.session.add(user)
    database.session.commit()
    
    # 获取 token
    response = client.post('/api/v1/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = response.get_json()['access_token']
    
    # 添加认证头
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    return client
```

#### `admin_client`
管理员认证的客户端
```python
@pytest.fixture
def admin_client(client, database):
    # 创建管理员并登录
    admin = User(username='admin', email='admin@example.com', role='admin')
    admin.set_password('admin123')
    database.session.add(admin)
    database.session.commit()
    
    response = client.post('/api/v1/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    token = response.get_json()['access_token']
    
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    return admin_client
```

## 📊 测试覆盖要求

### 必须测试的内容
1. **Models**
   - 创建对象
   - 验证规则
   - 关系映射
   - 序列化方法

2. **Services**
   - 业务逻辑
   - 错误处理
   - 边界条件

3. **API Routes**
   - 成功场景
   - 错误场景（400, 401, 403, 404）
   - 权限检查

4. **Decorators**
   - 认证成功/失败
   - 权限检查
   - 角色验证

### 测试场景覆盖
- ✅ 正常流程
- ✅ 边界条件
- ✅ 错误处理
- ✅ 异常情况

## 🐛 常见问题

### 1. 数据库未清理
**问题**: 测试间数据污染  
**解决**: 使用 `database` fixture，自动回滚事务

### 2. 中文字符串测试
**问题**: `SyntaxError: bytes can only contain ASCII literal characters`  
**解决**: 避免在 bytes 中使用中文，使用文本断言

```python
# ❌ 错误
assert b'思维导图' in response.data

# ✅ 正确
assert response.status_code == 200
assert '思维导图' in response.get_data(as_text=True)
```

### 3. JWT Token 测试
**问题**: Token 过期或无效  
**解决**: 使用 fixtures 创建测试用户和 token

## 📈 测试报告

### 生成测试报告
```bash
python -m pytest tests/ -v --tb=short --tb=long
```

### 覆盖率报告
```bash
python -m pytest tests/ --cov=app --cov-report=term-missing
```

示例输出：
```
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
app/__init__.py               45      2    96%   23-24
app/models/user.py            38      1    97%   45
app/api/deps.py               67      5    93%   89-93
--------------------------------------------------------
TOTAL                        150      8    95%
```

## 🎯 最佳实践

1. **保持测试独立**: 每个测试应该独立运行，不依赖其他测试
2. **使用 Fixtures**: 复用 setup/teardown 代码
3. **测试命名清晰**: 测试名称应该描述测试场景
4. **AAA 模式**: Arrange-Act-Assert 结构
5. **测试边界**: 不仅测试正常流程，也要测试边界和异常
6. **保持快速**: 测试应该快速执行，避免慢速 I/O
7. **持续集成**: 在 CI/CD 中自动运行测试

## 📚 参考资源

- [pytest 官方文档](https://docs.pytest.org/)
- [Flask 测试文档](https://flask.palletsprojects.com/testing/)
- [SQLAlchemy 测试最佳实践](https://docs.sqlalchemy.org/)

---

**最后更新**: 2025-03-03  
**维护者**: OpenHands Team
