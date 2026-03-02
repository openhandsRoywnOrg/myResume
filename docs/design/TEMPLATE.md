# 设计文档：{设计主题}

**状态**: 草案 | 评审中 | 已批准 | 已完成  
**创建日期**: YYYY-MM-DD  
**最后更新**: YYYY-MM-DD  
**作者**: @username  
**Reviewers**: @reviewer1, @reviewer2  
**关联需求**: [需求文档链接](../requirements/feature_XXX.md)

---

## 1. 概述

### 1.1 目标

这个设计要解决什么问题？

**示例**：
> 设计一个用户认证系统，支持用户名密码登录、JWT Token 认证、Token 自动刷新。

### 1.2 范围

**包含**：
- 用户登录功能
- Token 生成和验证
- Token 刷新机制

**不包含**：
- 用户注册功能（另见设计文档 XXX）
- 密码找回功能（另见设计文档 XXX）

### 1.3 设计原则

- 安全性优先
- 简单易用
- 可扩展
- 遵循 RESTful 规范

---

## 2. 架构设计

### 2.1 系统架构图

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │ ───→ │   API Gateway│ ───→ │ Auth Service│
│  (Browser)  │ ←─── │  (Flask App) │ ←─── │  (JWT Lib)  │
└─────────────┘      └──────────────┘      └─────────────┘
                              │
                              ↓
                     ┌──────────────┐
                     │   Database   │
                     │  (PostgreSQL)│
                     └──────────────┘
```

### 2.2 组件说明

| 组件 | 职责 | 技术选型 |
|------|------|----------|
| Client | 用户界面，发送认证请求 | React/Vue |
| API Gateway | 路由分发，请求验证 | Flask |
| Auth Service | 认证逻辑，Token 管理 | Flask-JWT-Extended |
| Database | 存储用户数据 | PostgreSQL |

### 2.3 数据流

```
1. 用户提交登录表单
   ↓
2. Client 发送 POST /api/v1/auth/login
   ↓
3. API Gateway 验证请求格式
   ↓
4. Auth Service 验证用户名密码
   ↓
5. 生成 JWT Token
   ↓
6. 返回 Token 给 Client
   ↓
7. Client 存储 Token（localStorage）
   ↓
8. 后续请求携带 Token（Authorization header）
```

---

## 3. 详细设计

### 3.1 数据模型

#### User 表

```python
class User(db.Model):
    """用户模型"""
    
    __tablename__ = 'users'
    
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(255), nullable=False)
    is_active: bool = db.Column(db.Boolean, default=True)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at: datetime = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def set_password(self, password: str):
        """设置密码（加密存储）"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """验证密码"""
        return check_password_hash(self.password_hash, password)
```

#### Token 表（可选，用于 Token 黑名单）

```python
class TokenBlacklist(db.Model):
    """Token 黑名单"""
    
    __tablename__ = 'token_blacklist'
    
    id: int = db.Column(db.Integer, primary_key=True)
    token: str = db.Column(db.String(500), unique=True, nullable=False)
    revoked_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
```

### 3.2 接口设计

#### POST /api/v1/auth/login

**请求**：
```json
{
  "username": "string",
  "password": "string"
}
```

**响应**：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600
}
```

**错误响应**：
```json
{
  "error": "Invalid credentials",
  "code": "AUTH_FAILED"
}
```

#### POST /api/v1/auth/refresh

**请求**：
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**响应**：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600
}
```

#### POST /api/v1/auth/logout

**请求头**：
```
Authorization: Bearer <access_token>
```

**响应**：
```json
{
  "message": "Successfully logged out"
}
```

### 3.3 流程设计

#### 登录流程

```
┌────────┐         ┌────────┐         ┌────────┐         ┌────────┐
│ Client │         │  API   │         │ Auth   │         │  DB    │
│        │         │Gateway │         │Service │         │        │
└───┬────┘         └───┬────┘         └───┬────┘         └───┬────┘
    │                  │                  │                  │
    │ 1. POST /login   │                  │                  │
    │─────────────────>│                  │                  │
    │                  │ 2. 验证请求格式   │                  │
    │                  │─────────────────>│                  │
    │                  │                  │ 3. 查询用户      │
    │                  │                  │─────────────────>│
    │                  │                  │<─────────────────│
    │                  │                  │ 4. 验证密码      │
    │                  │                  │                  │
    │                  │                  │ 5. 生成 Token     │
    │                  │<─────────────────│                  │
    │<─────────────────│                  │                  │
    │ 6. 返回 Token     │                  │                  │
    │                  │                  │                  │
```

#### Token 刷新流程

```
Client → POST /auth/refresh → 验证 refresh_token → 生成新 access_token → 返回
```

### 3.4 安全设计

#### 密码存储

```python
# 使用 bcrypt 加密
from werkzeug.security import generate_password_hash, check_password_hash

# 设置密码
user.set_password('plain_password')  # 自动哈希

# 验证密码
user.check_password('plain_password')  # 自动验证
```

#### Token 安全

```python
# JWT 配置
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_ALGORITHM = 'HS256'
```

#### 防止暴力破解

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/v1/auth/login', methods=['POST'])
@limiter.limit("5 per minute")  # 每分钟最多 5 次
def login():
    pass
```

---

## 4. 实现计划

### 4.1 任务分解

#### 阶段 1: 基础功能（P0）

- [ ] **Task-001**: 创建 User 数据模型
  - 预计：2 小时
  - 依赖：无
  
- [ ] **Task-002**: 实现登录 API
  - 预计：4 小时
  - 依赖：Task-001
  
- [ ] **Task-003**: 实现 Token 刷新 API
  - 预计：2 小时
  - 依赖：Task-002

#### 阶段 2: 安全增强（P1）

- [ ] **Task-004**: 实现 Token 黑名单
  - 预计：3 小时
  - 依赖：Task-003
  
- [ ] **Task-005**: 添加速率限制
  - 预计：2 小时
  - 依赖：Task-002

#### 阶段 3: 测试与文档（P2）

- [ ] **Task-006**: 编写单元测试
  - 预计：4 小时
  - 依赖：Task-001 ~ Task-005
  
- [ ] **Task-007**: 编写 API 文档
  - 预计：2 小时
  - 依赖：Task-002, Task-003

### 4.2 时间估算

| 阶段 | 任务数 | 预计时间 | 负责人 |
|------|--------|----------|--------|
| 阶段 1 | 3 | 8 小时 | @dev1 |
| 阶段 2 | 2 | 5 小时 | @dev1 |
| 阶段 3 | 2 | 6 小时 | @dev1 |
| **总计** | **7** | **19 小时** | |

### 4.3 里程碑

- **M1**: 基础功能完成（阶段 1）
- **M2**: 安全增强完成（阶段 2）
- **M3**: 测试文档完成（阶段 3）

---

## 5. 测试策略

### 5.1 单元测试

```python
def test_login_success():
    """测试登录成功"""
    response = client.post('/api/v1/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_invalid_credentials():
    """测试登录失败"""
    response = client.post('/api/v1/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.json['code'] == 'AUTH_FAILED'
```

### 5.2 集成测试

```python
def test_full_auth_flow():
    """测试完整认证流程"""
    # 1. 登录
    login_resp = client.post('/api/v1/auth/login', ...)
    access_token = login_resp.json['access_token']
    
    # 2. 访问受保护资源
    protected_resp = client.get('/api/v1/user/profile',
                                headers={'Authorization': f'Bearer {access_token}'})
    assert protected_resp.status_code == 200
    
    # 3. 登出
    logout_resp = client.post('/api/v1/auth/logout',
                              headers={'Authorization': f'Bearer {access_token}'})
    assert logout_resp.status_code == 200
    
    # 4. 使用已登出的 Token 访问
    protected_resp2 = client.get('/api/v1/user/profile',
                                 headers={'Authorization': f'Bearer {access_token}'})
    assert protected_resp2.status_code == 401
```

### 5.3 性能测试

```bash
# 使用 locust 进行压力测试
locust -f tests/performance/auth_perf.py --host=http://localhost:5000
```

---

## 6. 风险与缓解

### 6.1 技术风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| JWT 库有安全漏洞 | 低 | 高 | 使用最新稳定版本，定期更新 |
| 数据库性能瓶颈 | 中 | 中 | 添加索引，优化查询 |
| Token 泄露 | 中 | 高 | HTTPS 传输，Token 加密存储 |

### 6.2 实施风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 开发时间不足 | 中 | 中 | 优先实现 P0 功能 |
| 人员变动 | 低 | 中 | 详细文档，代码 Review |

---

## 7. 参考资料

### 7.1 相关文档

- [需求文档](../requirements/feature_001_user_auth.md)
- [架构设计文档](architecture.md)
- [API 设计规范](api_design.md)

### 7.2 技术文档

- [JWT RFC 7519](https://tools.ietf.org/html/rfc7519)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [bcrypt 密码加密](https://github.com/pyca/bcrypt/)

### 7.3 最佳实践

- [OWASP 认证指南](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [RESTful API 设计最佳实践](https://restfulapi.net/)

---

## 8. 变更历史

| 版本 | 日期 | 作者 | 变更描述 |
|------|------|------|----------|
| v0.1 | YYYY-MM-DD | @author | 初始版本 |
| v0.2 | YYYY-MM-DD | @author | 添加安全设计章节 |

---

## ✅ 审批

- [ ] 架构师审批：@architect - [ ] 批准 / [ ] 需要修改
- [ ] 技术负责人审批：@tech_lead - [ ] 批准 / [ ] 需要修改
- [ ] 安全负责人审批：@security_lead - [ ] 批准 / [ ] 需要修改

---

**备注**：
- 此文档必须在代码实现前完成并审批
- 任何设计变更必须更新此文档
- 代码必须严格按照设计文档实现
