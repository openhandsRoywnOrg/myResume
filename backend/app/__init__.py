"""
应用包导出

导出核心组件供其他模块使用
"""

from app.main import create_app
from app.extensions import db

__all__ = ['create_app', 'db']
