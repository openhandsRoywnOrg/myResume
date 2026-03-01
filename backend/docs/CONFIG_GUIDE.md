# 配置管理指南

## 📋 配置项清单

### 基础配置

| 配置项 | 环境变量 | 默认值 | 说明 | 必需 |
|--------|---------|--------|------|------|
| `SECRET_KEY` | `SECRET_KEY` | `dev-secret-key...` | Flask 密钥 | ✅ 生产环境 |
| `FLASK_ENV` | `FLASK_ENV` | `development` | 运行环境 | ❌ |
| `DEBUG` | - | `False` | Debug 模式 | ❌ |
| `TESTING` | - | `False` | 测试模式 | ❌ |

### 数据库配置

| 配置项 | 环境变量 | 默认值 | 说明 | 必需 |
|--------|---------|--------|------|------|
| `SQLALCHEMY_DATABASE_URI` | `DATABASE_URL` | `postgresql://...` | 数据库连接 | ✅ |
| `DEV_DATABASE_URL` | `DEV_DATABASE_URL` | `postgresql://...` | 开发数据库 | ❌ |
| `TEST_DATABASE_URL` | `TEST_DATABASE_URL` | `postgresql://...` | 测试数据库 | ❌ |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | - | `False` | 跟踪修改 | ❌ |

### JWT 认证配置

| 配置项 | 环境变量 | 默认值 | 说明 | 必需 |
|--------|---------|--------|------|------|
| `JWT_SECRET_KEY` | `JWT_SECRET_KEY` | `jwt-secret-key` | JWT 密钥 | ✅ 生产环境 |
| `JWT_ACCESS_TOKEN_EXPIRES` | `JWT_ACCESS_TOKEN_HOURS` | 1 小时 | Access Token 过期 | ❌ |
| `JWT_REFRESH_TOKEN_EXPIRES` | `JWT_REFRESH_TOKEN_DAYS` | 30 天 | Refresh Token 过期 | ❌ |

### AI/LLM 配置

| 配置项 | 环境变量 | 默认值 | 说明 | 必需 |
|--------|---------|--------|------|------|
| `LLM_API_KEY` | `LLM_API_KEY` | - | LLM API 密钥 | ❌ |
| `LLM_BASE_URL` | `LLM_BASE_URL` | OpenAI URL | LLM API 地址 | ❌ |
| `LLM_MODEL` | `LLM_MODEL` | `gpt-3.5-turbo` | LLM 模型 | ❌ |
| `LLM_TEMPERATURE` | `LLM_TEMPERATURE` | `0.7` | 温度（创造性） | ❌ |
| `LLM_MAX_TOKENS` | `LLM_MAX_TOKENS` | `1024` | 最大 token 数 | ❌ |

### 缓存配置

| 配置项 | 环境变量 | 默认值 | 说明 | 必需 |
|--------|---------|--------|------|------|
| `CACHE_TYPE` | `CACHE_TYPE` | `memory` | 缓存类型 | ❌ |
| `CACHE_REDIS_URL` | `CACHE_REDIS_URL` | - | Redis 连接 | ❌ |
| `CACHE_DEFAULT_TIMEOUT` | `CACHE_DEFAULT_TIMEOUT` | 300 秒 | 缓存超时 | ❌ |

### 日志配置

| 配置项 | 环境变量 | 默认值 | 说明 | 必需 |
|--------|---------|--------|------|------|
| `LOG_LEVEL` | `LOG_LEVEL` | `INFO` | 日志级别 | ❌ |
| `LOG_FILE` | `LOG_FILE` | - | 日志文件路径 | ❌ |

### 应用配置

| 配置项 | 环境变量 | 默认值 | 说明 | 必需 |
|--------|---------|--------|------|------|
| `APP_NAME` | - | `AI DevOps 面试库` | 应用名称 | ❌ |
| `APP_VERSION` | - | `0.1.0` | 应用版本 | ❌ |
| `PAGINATION_PER_PAGE` | - | `20` | 每页数量 | ❌ |
| `MAX_CONTENT_LENGTH` | `MAX_CONTENT_LENGTH` | 16MB | 上传大小限制 | ❌ |
| `UPLOAD_FOLDER` | `UPLOAD_FOLDER` | `/tmp/uploads` | 上传文件夹 | ❌ |

---

## 🔧 使用方法

### 1. 创建 .env 文件

```bash
cd backend
cp .env.example .env
```

### 2. 编辑 .env 文件

```bash
# 开发环境配置
SECRET_KEY=your-dev-secret-key
FLASK_ENV=development

# 数据库
DEV_DATABASE_URL=postgresql://localhost:5432/ai_interview_dev

# JWT
JWT_SECRET_KEY=your-jwt-secret-key

# LLM（可选）
LLM_API_KEY=sk-your-api-key
LLM_MODEL=gpt-3.5-turbo
```

### 3. 启动应用

```bash
# 开发环境
export FLASK_ENV=development
flask run

# 测试环境
export FLASK_ENV=testing
pytest

# 生产环境
export FLASK_ENV=production
export SECRET_KEY=prod-secret-key
export DATABASE_URL=postgresql://prod/db
gunicorn app.main:app
```

---

## 📝 环境配置示例

### 开发环境 (.env.development)

```bash
# 基础配置
SECRET_KEY=dev-secret-key-123456
FLASK_ENV=development
DEBUG=True

# 数据库
DEV_DATABASE_URL=postgresql://localhost:5432/ai_interview_dev

# JWT
JWT_SECRET_KEY=dev-jwt-key
JWT_ACCESS_TOKEN_HOURS=24  # 开发环境长一点

# LLM
LLM_API_KEY=sk-test-key
LLM_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.7

# 缓存
CACHE_TYPE=memory

# 日志
LOG_LEVEL=DEBUG
```

### 测试环境 (.env.testing)

```bash
# 基础配置
FLASK_ENV=testing
TESTING=True

# 数据库（测试数据库，每次测试前清空）
TEST_DATABASE_URL=postgresql://localhost:5432/ai_interview_test

# JWT（测试环境不过期）
JWT_SECRET_KEY=test-jwt-key
JWT_ACCESS_TOKEN_HOURS=24

# 禁用 CSRF（方便测试）
WTF_CSRF_ENABLED=False

# 缓存
CACHE_TYPE=memory

# 日志
LOG_LEVEL=DEBUG
```

### 生产环境 (.env.production)

```bash
# 基础配置（必须使用强随机密钥）
SECRET_KEY=<从密钥管理系统获取>
FLASK_ENV=production
DEBUG=False

# 数据库（必须设置）
DATABASE_URL=postgresql://user:password@host:port/database

# JWT（必须设置）
JWT_SECRET_KEY=<从密钥管理系统获取>
JWT_ACCESS_TOKEN_HOURS=1

# LLM（必须设置）
LLM_API_KEY=<从密钥管理系统获取>
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4

# 缓存（使用 Redis）
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://redis-host:6379/0
CACHE_DEFAULT_TIMEOUT=600

# 日志
LOG_LEVEL=INFO
LOG_FILE=/var/log/ai_interview/app.log
```

---

## 🔐 安全最佳实践

### 1. 密钥管理

**❌ 错误做法**：
```bash
# 硬编码密钥
SECRET_KEY=my-secret-key
LLM_API_KEY=sk-1234567890
```

**✅ 正确做法**：
```bash
# 从环境变量读取
SECRET_KEY=${SECRET_KEY_FROM_VAULT}
LLM_API_KEY=${LLM_API_KEY_FROM_VAULT}

# 或使用密钥管理服务
# AWS Secrets Manager
# HashiCorp Vault
# Azure Key Vault
```

### 2. 生成强密钥

```bash
# Python
python -c "import secrets; print(secrets.token_hex(32))"

# OpenSSL
openssl rand -hex 32

# Linux
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1
```

### 3. 不要提交 .env 文件

```bash
# .gitignore 已经包含
.env
.env.local
.env.*.local

# 提交前检查
git status
git add .
# 确保没有 .env 文件
```

### 4. 生产环境验证

```python
# ProductionConfig 会自动验证
from app.config import ProductionConfig

try:
    config = ProductionConfig()
except ValueError as e:
    print(f"配置错误：{e}")
    exit(1)
```

---

## 🧪 测试配置

### 运行配置测试

```bash
cd backend
pytest tests/unit/test_config.py -v
```

### 测试不同环境

```python
# test_environments.py
from app.config import (
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig
)

def test_development():
    config = DevelopmentConfig()
    assert config.DEBUG is True

def test_testing():
    config = TestingConfig()
    assert config.TESTING is True

def test_production():
    # 需要设置环境变量
    import os
    os.environ['SECRET_KEY'] = 'test'
    os.environ['DATABASE_URL'] = 'postgresql://...'
    os.environ['JWT_SECRET_KEY'] = 'test'
    
    config = ProductionConfig()
    assert config.DEBUG is False
```

---

## 🚨 常见问题

### Q1: 配置不生效怎么办？

**检查清单**：
1. ✅ `.env` 文件是否存在
2. ✅ 环境变量名是否正确
3. ✅ 是否重启了应用
4. ✅ 是否有拼写错误

**调试方法**：
```python
import os
from dotenv import load_dotenv

load_dotenv()  # 重新加载
print(os.environ.get('SECRET_KEY'))  # 检查值
```

### Q2: 如何在不同环境切换？

**方法 1：环境变量**
```bash
export FLASK_ENV=development
flask run

export FLASK_ENV=production
gunicorn app.main:app
```

**方法 2：不同 .env 文件**
```bash
# 开发
cp .env.development .env
flask run

# 测试
cp .env.testing .env
pytest

# 生产
cp .env.production .env
gunicorn app.main:app
```

### Q3: 如何在 Docker 中使用配置？

**Dockerfile**：
```dockerfile
FROM python:3.12

WORKDIR /app

# 不复制 .env，通过环境变量传入
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

# 使用环境变量启动
CMD ["gunicorn", "app.main:app"]
```

**docker-compose.yml**：
```yaml
version: '3'
services:
  app:
    build: .
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://db:5432/app
      - LLM_API_KEY=${LLM_API_KEY}
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
```

### Q4: 如何在 Vercel 中配置？

**Vercel 控制台**：
1. 进入项目 Settings
2. 选择 Environment Variables
3. 添加变量：
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `LLM_API_KEY`
   - 等等

**或使用 vercel.json**：
```json
{
  "env": {
    "FLASK_ENV": "production"
  }
}
```

---

## 📚 参考资源

- [Flask 配置文档](https://flask.palletsprojects.com/en/2.3.x/config/)
- [python-dotenv 文档](https://pypi.org/project/python-dotenv/)
- [12-Factor App 配置](https://12factor.net/config)
- [SQLAlchemy 配置](https://docs.sqlalchemy.org/en/20/core/engines.html)

---

## ✅ 配置检查清单

在部署前检查：

- [ ] `.env` 文件未提交到 Git
- [ ] 生产环境使用强随机密钥
- [ ] 所有必需的环境变量都已设置
- [ ] 数据库连接测试通过
- [ ] LLM API 密钥有效
- [ ] 日志级别设置正确
- [ ] 缓存配置正确
- [ ] 配置测试通过

---

**最后更新**: 2026-03-01
**版本**: 0.1.0
