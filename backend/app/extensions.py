"""
数据库扩展初始化

使用 SQLAlchemy 作为 ORM
"""

from flask_sqlalchemy import SQLAlchemy

# 数据库实例
db = SQLAlchemy()


def init_db(app):
    """
    初始化数据库扩展
    
    Args:
        app: Flask 应用实例
    """
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
