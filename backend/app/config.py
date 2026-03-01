"""
配置管理模块

支持三种环境：
- development: 开发环境，开启 debug 模式
- testing: 测试环境，使用测试数据库
- production: 生产环境，优化性能
"""

import os
from datetime import timedelta


class BaseConfig:
    """基础配置类"""
    
    # 密钥
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # 数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://localhost:5432/ai_interview_dev'
    )
    
    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # AI 配置
    LLM_API_KEY = os.environ.get('LLM_API_KEY', '')
    LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://api.openai.com/v1')
    LLM_MODEL = os.environ.get('LLM_MODEL', 'gpt-3.5-turbo')
    LLM_TEMPERATURE = float(os.environ.get('LLM_TEMPERATURE', '0.7'))


class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    """测试环境配置"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL',
        'postgresql://localhost:5432/ai_interview_test'
    )


class ProductionConfig(BaseConfig):
    """生产环境配置"""
    DEBUG = False
    TESTING = False
    
    # 生产环境必须设置这些环境变量
    def __init__(self):
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY must be set in production")
        if not os.environ.get('DATABASE_URL'):
            raise ValueError("DATABASE_URL must be set in production")


# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
