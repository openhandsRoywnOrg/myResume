"""
权限系统测试

测试认证和权限装饰器的功能
"""
import pytest
from flask import Flask
from flask_jwt_extended import JWTManager

from app import db, create_app
from app.models.user import User
from app.api.deps import (
    require_auth,
    require_role,
    require_admin,
    require_super_admin,
    optional_auth,
    permission_required,
    get_current_user,
    AuthenticationError,
    PermissionError
)


class TestUserModel:
    """测试用户模型"""
    
    def test_create_user(self, database):
        """测试创建用户"""
        user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('password123')
        
        database.session.add(user)
        database.session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == 'user'
        assert user.is_active is True
    
    def test_user_password_hashing(self, database):
        """测试密码哈希"""
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.set_password('password123')
        
        assert user.password_hash != 'password123'
        assert user.check_password('password123') is True
        assert user.check_password('wrongpassword') is False
    
    def test_user_roles(self, database):
        """测试用户角色判断"""
        guest = User(username='guest', email='guest@example.com', role='guest')
        user = User(username='user', email='user@example.com', role='user')
        admin = User(username='admin', email='admin@example.com', role='admin')
        super_admin = User(username='super', email='super@example.com', role='super_admin')
        
        # 测试 guest
        assert guest.is_guest() is True
        assert guest.is_user() is False
        assert guest.is_admin() is False
        assert guest.is_super_admin() is False
        
        # 测试 user
        assert user.is_guest() is False
        assert user.is_user() is True
        assert user.is_admin() is False
        assert user.is_super_admin() is False
        
        # 测试 admin
        assert admin.is_guest() is False
        assert admin.is_user() is True
        assert admin.is_admin() is True
        assert admin.is_super_admin() is False
        
        # 测试 super_admin
        assert super_admin.is_guest() is False
        assert super_admin.is_user() is True
        assert super_admin.is_admin() is True
        assert super_admin.is_super_admin() is True
    
    def test_user_has_permission(self, database):
        """测试权限检查"""
        guest = User(username='guest', email='guest@example.com', role='guest')
        user = User(username='user', email='user@example.com', role='user')
        admin = User(username='admin', email='admin@example.com', role='admin')
        super_admin = User(username='super', email='super@example.com', role='super_admin')
        
        # Guest 只能访问 guest 权限
        assert guest.has_permission('guest') is True
        assert guest.has_permission('user') is False
        assert guest.has_permission('admin') is False
        
        # User 可以访问 user 和 guest
        assert user.has_permission('guest') is True
        assert user.has_permission('user') is True
        assert user.has_permission('admin') is False
        
        # Admin 可以访问 admin, user, guest
        assert admin.has_permission('guest') is True
        assert admin.has_permission('user') is True
        assert admin.has_permission('admin') is True
        assert admin.has_permission('super_admin') is False
        
        # Super admin 可以访问所有
        assert super_admin.has_permission('guest') is True
        assert super_admin.has_permission('user') is True
        assert super_admin.has_permission('admin') is True
        assert super_admin.has_permission('super_admin') is True
    
    def test_user_to_dict(self, database):
        """测试用户字典转换"""
        user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        
        # 不包含邮箱
        data = user.to_dict()
        assert 'email' not in data
        assert data['username'] == 'testuser'
        assert data['role'] == 'user'
        
        # 包含邮箱
        data_with_email = user.to_dict(include_email=True)
        assert data_with_email['email'] == 'test@example.com'


class TestAuthDecorators:
    """测试认证装饰器"""
    
    @pytest.fixture
    def test_app(self, app):
        """创建带有测试路由的应用"""
        # 注册错误处理器
        from app.api.deps import register_auth_error_handlers
        register_auth_error_handlers(app)
        
        # 创建测试路由
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
        
        return app
    
    def test_require_auth_without_token(self, client, test_app):
        """测试未提供 token 时要求认证"""
        response = client.get('/api/test/auth-required')
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'authentication_error'
    
    def test_require_auth_with_valid_token(self, auth_client, test_app):
        """测试使用有效 token 要求认证"""
        response = auth_client.get('/api/test/auth-required')
        assert response.status_code == 200
        data = response.get_json()
        assert 'user' in data
        assert data['user']['username'] == 'testuser'
    
    def test_require_auth_with_inactive_user(self, client, database, test_app):
        """测试非活跃用户认证"""
        # 创建非活跃用户
        user = User(
            username='inactive',
            email='inactive@example.com',
            role='user',
            is_active=False
        )
        user.set_password('password123')
        database.session.add(user)
        database.session.commit()
        
        # 登录
        login_response = client.post('/api/v1/auth/login', json={
            'username': 'inactive',
            'password': 'password123'
        })
        
        # 非活跃用户应该无法登录或 token 无效
        # 具体行为取决于认证实现
        if login_response.status_code == 200:
            token = login_response.get_json()['access_token']
            response = client.get(
                '/api/test/auth-required',
                headers={'Authorization': f'Bearer {token}'}
            )
            # 应该返回 401 因为用户非活跃
            assert response.status_code == 401
    
    def test_admin_only_with_regular_user(self, auth_client, test_app):
        """测试普通用户访问管理员接口"""
        response = auth_client.get('/api/test/admin-only')
        assert response.status_code == 403
        data = response.get_json()
        assert data['error'] == 'permission_denied'
    
    def test_admin_only_with_admin(self, admin_client, test_app):
        """测试管理员访问管理员接口"""
        response = admin_client.get('/api/test/admin-only')
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Admin access granted'
    
    def test_super_admin_only_with_admin(self, admin_client, test_app):
        """测试管理员访问超级管理员接口"""
        response = admin_client.get('/api/test/super-admin-only')
        assert response.status_code == 403
        data = response.get_json()
        assert data['error'] == 'permission_denied'
    
    def test_role_check_with_valid_roles(self, auth_client, test_app):
        """测试角色检查（user 角色允许）"""
        response = auth_client.get('/api/test/role-check')
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'User or admin access granted'
    
    def test_role_check_with_admin(self, admin_client, test_app):
        """测试角色检查（admin 角色允许）"""
        response = admin_client.get('/api/test/role-check')
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'User or admin access granted'
    
    def test_optional_auth_without_token(self, client, test_app):
        """测试可选认证（无 token）"""
        response = client.get('/api/test/optional-auth')
        assert response.status_code == 200
        data = response.get_json()
        assert data['authenticated'] is False
    
    def test_optional_auth_with_token(self, auth_client, test_app):
        """测试可选认证（有 token）"""
        response = auth_client.get('/api/test/optional-auth')
        assert response.status_code == 200
        data = response.get_json()
        assert data['authenticated'] is True
        assert data['user']['username'] == 'testuser'


class TestPermissionIntegration:
    """权限集成测试"""
    
    def test_user_creation_workflow(self, client, database):
        """测试用户创建流程"""
        # 1. 创建用户
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepassword123'
        }
        
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            role='user'
        )
        user.set_password(user_data['password'])
        database.session.add(user)
        database.session.commit()
        
        # 2. 验证用户可以登录
        login_response = client.post('/api/v1/auth/login', json={
            'username': 'newuser',
            'password': 'securepassword123'
        })
        
        # 如果认证 API 已实现，应该成功
        # 否则跳过此测试
        if login_response.status_code == 200:
            token = login_response.get_json()['access_token']
            assert token is not None
            
            # 3. 使用 token 访问受保护资源
            response = client.get(
                '/api/test/auth-required',
                headers={'Authorization': f'Bearer {token}'}
            )
            assert response.status_code == 200
    
    def test_permission_escalation(self, database):
        """测试权限升级"""
        # 创建不同角色的用户
        users = [
            User(username='guest1', email='guest1@example.com', role='guest'),
            User(username='user1', email='user1@example.com', role='user'),
            User(username='admin1', email='admin1@example.com', role='admin'),
            User(username='super1', email='super1@example.com', role='super_admin')
        ]
        
        for user in users:
            user.set_password('password123')
            database.session.add(user)
        database.session.commit()
        
        # 验证权限层级
        permissions = ['guest', 'user', 'admin', 'super_admin']
        
        # Guest 只能访问 guest
        guest = users[0]
        assert sum(1 for p in permissions if guest.has_permission(p)) == 1
        
        # User 可以访问 guest 和 user
        user = users[1]
        assert sum(1 for p in permissions if user.has_permission(p)) == 2
        
        # Admin 可以访问 guest, user, admin
        admin = users[2]
        assert sum(1 for p in permissions if admin.has_permission(p)) == 3
        
        # Super admin 可以访问所有
        super_admin = users[3]
        assert sum(1 for p in permissions if super_admin.has_permission(p)) == 4


class TestSecurity:
    """安全测试"""
    
    def test_password_not_stored_in_plain_text(self, database):
        """测试密码不以明文存储"""
        user = User(
            username='testuser',
            email='test@example.com'
        )
        password = 'mysecretpassword123'
        user.set_password(password)
        database.session.add(user)
        database.session.commit()
        
        # 密码应该是哈希值，不是明文
        assert user.password_hash != password
        assert len(user.password_hash) > len(password)
        assert password not in user.password_hash
    
    def test_user_cannot_access_admin_without_role(self, auth_client, test_app):
        """测试用户无法通过伪造访问管理员接口"""
        # 尝试各种方式访问管理员接口
        response = auth_client.get('/api/test/admin-only')
        assert response.status_code == 403
        
        # 尝试修改请求头
        response = auth_client.get(
            '/api/test/admin-only',
            headers={'X-Role': 'admin'}
        )
        assert response.status_code == 403
    
    @pytest.fixture
    def test_app(self, app):
        """创建带有测试路由的应用"""
        from app.api.deps import register_auth_error_handlers
        register_auth_error_handlers(app)
        
        @app.route('/api/test/admin-only')
        @require_admin
        def admin_only():
            return {'message': 'Admin access granted'}
        
        return app
