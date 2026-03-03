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
    
    # 注册钩子
    from app.hooks import init_hooks
    init_hooks()
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app
