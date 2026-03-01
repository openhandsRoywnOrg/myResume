"""
配置管理单元测试

测试配置类的正确性和验证逻辑
"""

import os
import pytest
from datetime import timedelta


class TestBaseConfig:
    """测试基础配置类"""
    
    def test_secret_key_has_default(self):
        """测试 SECRET_KEY 有默认值"""
        from app.config import BaseConfig
        
        # 即使环境变量未设置，也应该有默认值
        config = BaseConfig()
        assert config.SECRET_KEY is not None
        assert len(config.SECRET_KEY) > 0
    
    def test_debug_default_is_false(self):
        """测试 DEBUG 默认是 False"""
        from app.config import BaseConfig
        
        config = BaseConfig()
        assert config.DEBUG is False
    
    def test_testing_default_is_false(self):
        """测试 TESTING 默认是 False"""
        from app.config import BaseConfig
        
        config = BaseConfig()
        assert config.TESTING is False
    
    def test_sqlalchemy_track_modifications_is_false(self):
        """测试 SQLALCHEMY_TRACK_MODIFICATIONS 是 False"""
        from app.config import BaseConfig
        
        config = BaseConfig()
        assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    
    def test_database_url_has_default(self):
        """测试 DATABASE_URL 有默认值"""
        from app.config import BaseConfig
        
        config = BaseConfig()
        assert 'postgresql' in config.SQLALCHEMY_DATABASE_URI
    
    def test_jwt_access_token_expires(self):
        """测试 JWT Access Token 过期时间"""
        from app.config import BaseConfig
        
        config = BaseConfig()
        assert isinstance(config.JWT_ACCESS_TOKEN_EXPIRES, timedelta)
        assert config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds() > 0
    
    def test_llm_temperature_is_float(self):
        """测试 LLM_TEMPERATURE 是浮点数"""
        from app.config import BaseConfig
        
        config = BaseConfig()
        assert isinstance(config.LLM_TEMPERATURE, float)
        assert 0.0 <= config.LLM_TEMPERATURE <= 1.0
    
    def test_pagination_per_page(self):
        """测试分页配置"""
        from app.config import BaseConfig
        
        config = BaseConfig()
        assert config.PAGINATION_PER_PAGE == 20
    
    def test_max_content_length(self):
        """测试文件上传大小限制"""
        from app.config import BaseConfig
        
        config = BaseConfig()
        assert config.MAX_CONTENT_LENGTH == 16777216  # 16MB


class TestDevelopmentConfig:
    """测试开发环境配置"""
    
    def test_debug_is_true(self):
        """测试开发环境 DEBUG 是 True"""
        from app.config import DevelopmentConfig
        
        config = DevelopmentConfig()
        assert config.DEBUG is True
    
    def test_testing_is_false(self):
        """测试开发环境 TESTING 是 False"""
        from app.config import DevelopmentConfig
        
        config = DevelopmentConfig()
        assert config.TESTING is False
    
    def test_log_level_is_debug(self):
        """测试开发环境日志级别是 DEBUG"""
        from app.config import DevelopmentConfig
        
        config = DevelopmentConfig()
        assert config.LOG_LEVEL == 'DEBUG'
    
    def test_cache_type_is_memory(self):
        """测试开发环境使用内存缓存"""
        from app.config import DevelopmentConfig
        
        config = DevelopmentConfig()
        assert config.CACHE_TYPE == 'memory'


class TestTestingConfig:
    """测试测试环境配置"""
    
    def test_debug_is_true(self):
        """测试测试环境 DEBUG 是 True"""
        from app.config import TestingConfig
        
        config = TestingConfig()
        assert config.DEBUG is True
    
    def test_testing_is_true(self):
        """测试测试环境 TESTING 是 True"""
        from app.config import TestingConfig
        
        config = TestingConfig()
        assert config.TESTING is True
    
    def test_csrf_disabled(self):
        """测试测试环境禁用 CSRF"""
        from app.config import TestingConfig
        
        config = TestingConfig()
        assert config.WTF_CSRF_ENABLED is False
    
    def test_jwt_token_longer_expiry(self):
        """测试测试环境 JWT Token 过期时间更长"""
        from app.config import TestingConfig
        
        config = TestingConfig()
        # 测试环境 24 小时过期
        assert config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds() == 24 * 3600


class TestProductionConfig:
    """测试生产环境配置"""
    
    def test_debug_is_false(self):
        """测试生产环境 DEBUG 是 False"""
        from app.config import ProductionConfig
        
        config = ProductionConfig()
        assert config.DEBUG is False
    
    def test_testing_is_false(self):
        """测试生产环境 TESTING 是 False"""
        from app.config import ProductionConfig
        
        config = ProductionConfig()
        assert config.TESTING is False
    
    def test_requires_secret_key(self, monkeypatch):
        """测试生产环境必须设置 SECRET_KEY"""
        from app.config import ProductionConfig
        
        # 清除 SECRET_KEY 环境变量
        monkeypatch.delenv('SECRET_KEY', raising=False)
        
        with pytest.raises(ValueError) as exc_info:
            ProductionConfig()
        
        assert 'SECRET_KEY must be set' in str(exc_info.value)
    
    def test_requires_database_url(self, monkeypatch):
        """测试生产环境必须设置 DATABASE_URL"""
        from app.config import ProductionConfig
        
        # 设置 SECRET_KEY 但不设置 DATABASE_URL
        monkeypatch.setenv('SECRET_KEY', 'test-key')
        monkeypatch.delenv('DATABASE_URL', raising=False)
        
        with pytest.raises(ValueError) as exc_info:
            ProductionConfig()
        
        assert 'DATABASE_URL must be set' in str(exc_info.value)
    
    def test_requires_jwt_secret_key(self, monkeypatch):
        """测试生产环境必须设置 JWT_SECRET_KEY"""
        from app.config import ProductionConfig
        
        # 设置必要的环境变量，但不设置 JWT_SECRET_KEY
        monkeypatch.setenv('SECRET_KEY', 'test-key')
        monkeypatch.setenv('DATABASE_URL', 'postgresql://localhost/db')
        monkeypatch.delenv('JWT_SECRET_KEY', raising=False)
        
        with pytest.raises(ValueError) as exc_info:
            ProductionConfig()
        
        assert 'JWT_SECRET_KEY must be set' in str(exc_info.value)
    
    def test_all_required_vars_set(self, monkeypatch):
        """测试所有必需环境变量都设置时可以正常创建"""
        from app.config import ProductionConfig
        
        # 设置所有必需的环境变量
        monkeypatch.setenv('SECRET_KEY', 'test-key')
        monkeypatch.setenv('DATABASE_URL', 'postgresql://localhost/db')
        monkeypatch.setenv('JWT_SECRET_KEY', 'jwt-key')
        
        # 不应该抛出异常
        config = ProductionConfig()
        assert config.DEBUG is False


class TestConfigDictionary:
    """测试配置字典"""
    
    def test_config_has_all_environments(self):
        """测试配置字典包含所有环境"""
        from app.config import config
        
        assert 'development' in config
        assert 'testing' in config
        assert 'production' in config
        assert 'default' in config
    
    def test_default_is_development(self):
        """测试默认配置是开发环境"""
        from app.config import config
        
        assert config['default'] == config['development']


class TestGetConfig:
    """测试 get_config 函数"""
    
    def test_get_config_default(self, monkeypatch):
        """测试默认获取配置"""
        from app.config import get_config, DevelopmentConfig
        
        monkeypatch.delenv('FLASK_ENV', raising=False)
        
        config_class = get_config()
        assert config_class == DevelopmentConfig
    
    def test_get_config_development(self, monkeypatch):
        """测试获取开发环境配置"""
        from app.config import get_config, DevelopmentConfig
        
        monkeypatch.setenv('FLASK_ENV', 'development')
        
        config_class = get_config()
        assert config_class == DevelopmentConfig
    
    def test_get_config_testing(self, monkeypatch):
        """测试获取测试环境配置"""
        from app.config import get_config, TestingConfig
        
        monkeypatch.setenv('FLASK_ENV', 'testing')
        
        config_class = get_config()
        assert config_class == TestingConfig
    
    def test_get_config_production(self, monkeypatch):
        """测试获取生产环境配置"""
        from app.config import get_config, ProductionConfig
        
        monkeypatch.setenv('FLASK_ENV', 'production')
        
        config_class = get_config()
        assert config_class == ProductionConfig


class TestValidateConfig:
    """测试配置验证函数"""
    
    def test_validate_config_missing_secret_key(self):
        """测试验证缺少 SECRET_KEY"""
        from app import create_app
        from app.config import validate_config
        
        app = create_app('testing')
        app.config['SECRET_KEY'] = None
        
        with pytest.raises(ValueError) as exc_info:
            validate_config(app)
        
        assert 'SECRET_KEY' in str(exc_info.value)
    
    def test_validate_config_missing_database(self):
        """测试验证缺少数据库配置"""
        from app import create_app
        from app.config import validate_config
        
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = None
        
        with pytest.raises(ValueError) as exc_info:
            validate_config(app)
        
        assert 'DATABASE_URL' in str(exc_info.value)
    
    def test_validate_config_valid(self):
        """测试验证有效配置"""
        from app import create_app
        from app.config import validate_config
        
        app = create_app('testing')
        
        # 应该不抛出异常
        result = validate_config(app)
        assert result is True


class TestEnvironmentVariables:
    """测试环境变量加载"""
    
    def test_load_from_env_file(self, monkeypatch, tmp_path):
        """测试从 .env 文件加载配置"""
        # 创建临时 .env 文件
        env_file = tmp_path / ".env"
        env_file.write_text("SECRET_KEY=test-key-from-file\n")
        
        # 设置环境变量
        monkeypatch.setenv('SECRET_KEY', 'test-key')
        
        from app.config import BaseConfig
        config = BaseConfig()
        
        # 环境变量优先于文件
        assert config.SECRET_KEY == 'test-key'
    
    def test_custom_llm_temperature(self, monkeypatch):
        """测试自定义 LLM 温度"""
        monkeypatch.setenv('LLM_TEMPERATURE', '0.9')
        
        # 重新导入以加载新环境变量
        import importlib
        from app import config
        importlib.reload(config)
        
        assert config.BaseConfig.LLM_TEMPERATURE == 0.9
    
    def test_custom_cache_timeout(self, monkeypatch):
        """测试自定义缓存超时时间"""
        monkeypatch.setenv('CACHE_DEFAULT_TIMEOUT', '600')
        
        from app.config import BaseConfig
        config = BaseConfig()
        
        assert config.CACHE_DEFAULT_TIMEOUT == 600
