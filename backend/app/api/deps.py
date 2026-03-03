"""
认证和权限依赖装饰器

提供 API 路由的权限检查功能
"""
from functools import wraps
from typing import Optional, List, Union
from flask import request, jsonify, g, current_app
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity,
    get_jwt,
    jwt_required
)

from app.models.user import User
from app import db


class PermissionError(Exception):
    """权限错误"""
    def __init__(self, message: str = "Permission denied", status_code: int = 403):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(Exception):
    """认证错误"""
    def __init__(self, message: str = "Authentication required", status_code: int = 401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def get_current_user() -> Optional[User]:
    """
    获取当前登录用户
    
    Returns:
        User: 当前用户对象，如果未登录则返回 None
    """
    if hasattr(g, 'current_user'):
        return g.current_user
    
    # 尝试从 JWT token 中获取
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user and user.is_active:
            g.current_user = user
            return user
    except Exception:
        pass
    
    return None


def require_auth(f):
    """
    要求用户已认证（任何角色均可）
    
    使用示例：
        @api.route('/protected')
        @require_auth
        def protected_route():
            user = get_current_user()
            return jsonify({'user': user.to_dict()})
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        
        g.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function


def require_role(*roles: str):
    """
    要求用户具有指定角色之一
    
    Args:
        roles: 允许的角色列表
        
    使用示例：
        @api.route('/admin-only')
        @require_role('admin', 'super_admin')
        def admin_route():
            return jsonify({'message': 'Admin access granted'})
    """
    def decorator(f):
        @wraps(f)
        @require_auth
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            
            if not user:
                raise AuthenticationError("Authentication required")
            
            if user.role not in roles:
                raise PermissionError(
                    f"Required role: {', '.join(roles)}. Your role: {user.role}"
                )
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def require_admin(f):
    """
    要求用户是管理员（admin 或 super_admin）
    
    使用示例：
        @api.route('/topics', methods=['DELETE'])
        @require_admin
        def delete_topic():
            # 只有管理员可以删除
            pass
    """
    @wraps(f)
    @require_role('admin', 'super_admin')
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    
    return decorated_function


def require_super_admin(f):
    """
    要求用户是超级管理员
    
    使用示例：
        @api.route('/system/config', methods=['PUT'])
        @require_super_admin
        def update_system_config():
            # 只有超级管理员可以修改系统配置
            pass
    """
    @wraps(f)
    @require_role('super_admin')
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    
    return decorated_function


def optional_auth(f):
    """
    可选认证：如果用户已认证则获取用户信息，否则允许匿名访问
    
    使用示例：
        @api.route('/topics')
        @optional_auth
        def list_topics():
            user = get_current_user()
            if user:
                # 返回个性化内容
                pass
            else:
                # 返回公开内容
                pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 尝试获取用户，但不强制要求
        get_current_user()
        return f(*args, **kwargs)
    
    return decorated_function


def permission_required(permission: str):
    """
    基于权限的检查（更细粒度的权限控制）
    
    Args:
        permission: 权限名称
        
    使用示例：
        @api.route('/topics/<int:id>/edit')
        @permission_required('edit_topic')
        def edit_topic(id):
            # 检查用户是否有编辑知识点的权限
            pass
    """
    def decorator(f):
        @wraps(f)
        @require_auth
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            
            if not user:
                raise AuthenticationError("Authentication required")
            
            if not user.has_permission(permission):
                raise PermissionError(f"Permission '{permission}' required")
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


# ========== 错误处理器 ==========

def register_auth_error_handlers(app):
    """
    注册认证和权限错误处理器
    
    Args:
        app: Flask 应用实例
    """
    @app.errorhandler(AuthenticationError)
    def handle_auth_error(error):
        return jsonify({
            'error': 'authentication_error',
            'message': error.message
        }), error.status_code
    
    @app.errorhandler(PermissionError)
    def handle_permission_error(error):
        return jsonify({
            'error': 'permission_denied',
            'message': error.message
        }), error.status_code
