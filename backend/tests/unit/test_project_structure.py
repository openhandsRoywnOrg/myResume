"""
测试项目结构是否正确

验证所有模块都能正常导入
"""


def test_import_app():
    """测试能否导入 app 模块"""
    from app import create_app
    assert create_app is not None


def test_import_config():
    """测试能否导入 config 模块"""
    from app.config import config
    assert config is not None
    assert 'development' in config
    assert 'testing' in config
    assert 'production' in config


def test_import_extensions():
    """测试能否导入 extensions 模块"""
    from app.extensions import db
    assert db is not None


def test_import_hooks():
    """测试能否导入 hooks 模块"""
    from app.hooks import hooks, HookRegistry
    assert hooks is not None
    assert HookRegistry is not None


def test_import_exceptions():
    """测试能否导入 exceptions 模块"""
    from app.utils.exceptions import (
        AppException,
        ValidationError,
        NotFoundError,
        AuthenticationError,
        PermissionError,
        DatabaseError
    )
    assert AppException is not None
    assert ValidationError is not None


def test_create_app():
    """测试能否创建应用实例"""
    from app import create_app
    
    app = create_app('testing')
    assert app is not None
    assert app.config['TESTING'] is True


def test_health_endpoint():
    """测试健康检查端点"""
    from app import create_app
    
    app = create_app('testing')
    client = app.test_client()
    
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['version'] == 'v1'
