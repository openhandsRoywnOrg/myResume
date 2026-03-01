"""
配置管理模块

支持三种环境：
- development: 开发环境，开启 debug 模式
- testing: 测试环境，使用测试数据库
- production: 生产环境，优化性能

使用示例：
    from app.config import config
    app.config.from_object(config['development'])
    
    # 或从环境变量
    export FLASK_ENV=production
"""

import os
from datetime import timedelta
from typing import Optional

from dotenv import load_dotenv

# 加载 .env 文件（如果存在）
load_dotenv()


class BaseConfig:
    """
    基础配置类
    
    所有环境共享的配置项
    """
    
    # ========== 基础配置 ==========
    
    # Flask 密钥（用于 session、CSRF 等）
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # 调试模式
    DEBUG: bool = False
    TESTING: bool = False
    
    # ========== 数据库配置 ==========
    
    # 数据库连接 URL
    # 格式：postgresql://user:password@host:port/database
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        'DATABASE_URL',
        'postgresql://localhost:5432/ai_interview_dev'
    )
    
    # 跟踪对象修改（设为 False 节省内存）
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    
    # 池配置
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,  # 自动检测失效连接
    }
    
    # ========== JWT 认证配置 ==========
    
    # JWT 密钥
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # Access Token 过期时间（1 小时）
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(
        hours=int(os.environ.get('JWT_ACCESS_TOKEN_HOURS', '1'))
    )
    
    # Refresh Token 过期时间（30 天）
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(
        days=int(os.environ.get('JWT_REFRESH_TOKEN_DAYS', '30'))
    )
    
    # ========== AI/LLM 配置 ==========
    
    # LLM API 密钥
    LLM_API_KEY: Optional[str] = os.environ.get('LLM_API_KEY')
    
    # LLM API 基础 URL
    LLM_BASE_URL: str = os.environ.get(
        'LLM_BASE_URL',
        'https://api.openai.com/v1'
    )
    
    # LLM 模型名称
    LLM_MODEL: str = os.environ.get('LLM_MODEL', 'gpt-3.5-turbo')
    
    # LLM 温度（创造性，0-1 之间）
    LLM_TEMPERATURE: float = float(os.environ.get('LLM_TEMPERATURE', '0.7'))
    
    # LLM 最大 token 数
    LLM_MAX_TOKENS: int = int(os.environ.get('LLM_MAX_TOKENS', '1024'))
    
    # ========== 缓存配置 ==========
    
    # 缓存类型（redis/memory/none）
    CACHE_TYPE: str = os.environ.get('CACHE_TYPE', 'memory')
    
    # Redis 连接（如果使用 Redis 缓存）
    CACHE_REDIS_URL: Optional[str] = os.environ.get('CACHE_REDIS_URL')
    
    # 缓存默认过期时间（秒）
    CACHE_DEFAULT_TIMEOUT: int = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', '300'))
    
    # ========== 日志配置 ==========
    
    # 日志级别
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')
    
    # 日志文件路径
    LOG_FILE: Optional[str] = os.environ.get('LOG_FILE')
    
    # ========== 应用配置 ==========
    
    # 应用名称
    APP_NAME: str = 'AI DevOps 面试库'
    
    # 应用版本
    APP_VERSION: str = '0.1.0'
    
    # 每页默认显示数量
    PAGINATION_PER_PAGE: int = 20
    
    # 文件上传配置
    MAX_CONTENT_LENGTH: int = int(os.environ.get('MAX_CONTENT_LENGTH', '16777216'))  # 16MB
    UPLOAD_FOLDER: str = os.environ.get('UPLOAD_FOLDER', '/tmp/uploads')


class DevelopmentConfig(BaseConfig):
    """
    开发环境配置
    
    特点：
    - 开启 Debug 模式
    - 使用本地数据库
    - 详细的错误信息
    """
    
    DEBUG: bool = True
    TESTING: bool = False
    
    # 开发环境使用 SQLite（方便）
    # 也可以配置为本地 PostgreSQL
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        'DEV_DATABASE_URL',
        'postgresql://localhost:5432/ai_interview_dev'
    )
    
    # 开发环境日志级别
    LOG_LEVEL: str = 'DEBUG'
    
    # 开发环境使用内存缓存
    CACHE_TYPE: str = 'memory'


class TestingConfig(BaseConfig):
    """
    测试环境配置
    
    特点：
    - 开启 Testing 模式
    - 使用测试数据库
    - 禁用 CSRF 保护
    """
    
    DEBUG: bool = True
    TESTING: bool = True
    
    # 测试数据库（每次测试前清空）
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        'TEST_DATABASE_URL',
        'postgresql://localhost:5432/ai_interview_test'
    )
    
    # 测试环境使用内存缓存
    CACHE_TYPE: str = 'memory'
    
    # 测试环境 JWT 不过期（方便测试）
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=24)
    
    # 禁用 CSRF 保护（方便测试）
    WTF_CSRF_ENABLED: bool = False


class ProductionConfig(BaseConfig):
    """
    生产环境配置
    
    特点：
    - 关闭 Debug 模式
    - 使用环境变量配置
    - 严格的安全检查
    """
    
    DEBUG: bool = False
    TESTING: bool = False
    
    # 生产环境必须从环境变量读取配置
    def __init__(self):
        """验证生产环境配置"""
        if not os.environ.get('SECRET_KEY'):
            raise ValueError(
                "SECRET_KEY must be set in production environment. "
                "Example: export SECRET_KEY='your-secret-key'"
            )
        
        if not os.environ.get('DATABASE_URL'):
            raise ValueError(
                "DATABASE_URL must be set in production environment. "
                "Example: export DATABASE_URL='postgresql://user:pass@host/db'"
            )
        
        if not os.environ.get('JWT_SECRET_KEY'):
            raise ValueError(
                "JWT_SECRET_KEY must be set in production environment."
            )
        
        # 生产环境不应该使用默认的 LLM 配置
        if not os.environ.get('LLM_API_KEY'):
            print("⚠️  Warning: LLM_API_KEY not set. AI features will not work.")


# 配置字典
# 通过 config['development'] 访问对应的配置类
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config() -> type:
    """
    根据环境变量获取配置类
    
    Returns:
        配置类
        
    使用示例：
        config_class = get_config()
        app.config.from_object(config_class)
    """
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])


def validate_config(app) -> bool:
    """
    验证应用配置是否完整
    
    Args:
        app: Flask 应用实例
        
    Returns:
        bool: 配置是否有效
        
    Raises:
        ValueError: 配置无效时
    """
    required_keys = ['SECRET_KEY']
    
    for key in required_keys:
        if not app.config.get(key):
            raise ValueError(f"Required config '{key}' is not set")
    
    # 验证数据库配置
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if not db_uri:
        raise ValueError("DATABASE_URL is not configured")
    
    # 验证 JWT 配置（如果需要认证功能）
    if not app.config.get('JWT_SECRET_KEY'):
        print("⚠️  Warning: JWT_SECRET_KEY not set. Authentication will not work.")
    
    return True
