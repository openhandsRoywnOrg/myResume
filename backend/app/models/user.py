"""
用户模型

定义用户数据结构和基本方法
"""
from datetime import datetime
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class User(db.Model):
    """
    用户模型
    
    角色说明：
    - guest: 访客（未认证用户）
    - user: 普通用户
    - admin: 管理员
    - super_admin: 超级管理员
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # 关系
    # topics = db.relationship('Topic', backref='creator', lazy='dynamic')
    # interviews = db.relationship('Interview', backref='user', lazy='dynamic')
    
    def set_password(self, password: str) -> None:
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def is_guest(self) -> bool:
        """是否为访客"""
        return self.role == 'guest'
    
    def is_user(self) -> bool:
        """是否为普通用户"""
        return self.role in ['user', 'admin', 'super_admin']
    
    def is_admin(self) -> bool:
        """是否为管理员"""
        return self.role in ['admin', 'super_admin']
    
    def is_super_admin(self) -> bool:
        """是否为超级管理员"""
        return self.role == 'super_admin'
    
    def has_permission(self, permission: str) -> bool:
        """
        检查用户是否有指定权限
        
        Args:
            permission: 权限名称
            
        Returns:
            bool: 是否有权限
        """
        # 权限层级：super_admin > admin > user > guest
        permission_hierarchy = {
            'super_admin': ['super_admin', 'admin', 'user', 'guest'],
            'admin': ['admin', 'user', 'guest'],
            'user': ['user', 'guest'],
            'guest': ['guest']
        }
        
        user_level = permission_hierarchy.get(self.role, ['guest'])
        return permission in user_level or self.role == permission
    
    def to_dict(self, include_email: bool = False) -> dict:
        """
        转换为字典
        
        Args:
            include_email: 是否包含邮箱（默认不包含，保护隐私）
            
        Returns:
            dict: 用户信息字典
        """
        data = {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_email:
            data['email'] = self.email
        return data
    
    def __repr__(self) -> str:
        return f'<User {self.username} ({self.role})>'
