"""
AI DevOps 面试库 - Flask 应用主模块

这个包包含了整个应用的核心功能，按职责分离到不同的子模块：
- models: 数据模型定义
- services: 业务逻辑实现
- api: RESTful API 路由
- hooks: 钩子函数（验证、审计等）
- utils: 工具函数
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.extensions import db


def create_app(config_name=None):
    """
    应用工厂函数 - 创建并配置 Flask 应用
    
    Args:
        config_name: 配置名称 ('development', 'testing', 'production')
        
    Returns:
        Flask: 配置好的应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    if config_name is None:
        from app.config import get_config
        config_class = get_config()
    else:
        from app.config import config
        config_class = config.get(config_name, config['development'])
    
    app.config.from_object(config_class)
    
    # 验证配置
    from app.config import validate_config
    try:
        validate_config(app)
    except ValueError as e:
        if not app.config.get('TESTING'):
            raise
    
    # 初始化扩展
    db.init_app(app)
    jwt = JWTManager()
    jwt.init_app(app)
    CORS(app)  # 允许跨域请求
    
    # 注册错误处理器
    from app.api.deps import register_auth_error_handlers
    register_auth_error_handlers(app)
    
    # 注册 Blueprint
    from app.api.v1 import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # 注册认证 Blueprint
    from app.api.v1.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    # 注册钩子
    from app.hooks import init_hooks
    init_hooks()
    
    # 注册测试路由（仅在测试模式下）
    if app.config.get('TESTING'):
        _register_test_routes(app)

    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app


def _register_test_routes(app):
    """
    注册测试专用路由

    这些路由仅用于测试认证和权限装饰器
    """
    from app.api.deps import (
        require_auth,
        require_role,
        require_admin,
        require_super_admin,
        optional_auth,
        get_current_user
    )

    @app.route('/api/test/auth-required')
    @require_auth
    def auth_required():
        user = get_current_user()
        return {'user': user.to_dict()}

    @app.route('/api/test/admin-only')
    @require_admin
    def admin_only():
        return {'message': 'Admin access granted'}

    @app.route('/api/test/super-admin-only')
    @require_super_admin
    def super_admin_only():
        return {'message': 'Super admin access granted'}

    @app.route('/api/test/role-check')
    @require_role('user', 'admin')
    def role_check():
        return {'message': 'User or admin access granted'}

    @app.route('/api/test/optional-auth')
    @optional_auth
    def optional_auth_route():
        user = get_current_user()
        if user:
            return {'authenticated': True, 'user': user.to_dict()}
        else:
            return {'authenticated': False}
