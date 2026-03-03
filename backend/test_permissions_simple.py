#!/usr/bin/env python
"""
权限系统测试脚本

用于快速验证权限功能是否正常工作
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from app import create_app, db
from app.models.user import User
from app.api.deps import (
    get_current_user,
    require_auth,
    require_role,
    require_admin,
    AuthenticationError,
    PermissionError
)
from flask import jsonify


def test_user_model():
    """测试用户模型"""
    print("\n=== 测试用户模型 ===")
    
    # 创建用户
    user = User(username='testuser', email='test@example.com', role='user')
    user.set_password('password123')
    
    assert user.username == 'testuser'
    assert user.check_password('password123')
    assert not user.check_password('wrongpassword')
    print("✓ 用户创建和密码哈希正常")
    
    # 测试角色
    guest = User(username='guest', email='guest@example.com', role='guest')
    admin = User(username='admin', email='admin@example.com', role='admin')
    super_admin = User(username='super', email='super@example.com', role='super_admin')
    
    assert guest.is_guest()
    assert not guest.is_admin()
    assert admin.is_admin()
    assert not admin.is_super_admin()
    assert super_admin.is_super_admin()
    print("✓ 用户角色判断正常")
    
    # 测试权限
    assert not guest.has_permission('admin')
    assert admin.has_permission('user')
    assert super_admin.has_permission('super_admin')
    print("✓ 权限检查正常")
    
    print("用户模型测试通过！\n")


def test_auth_decorators():
    """测试认证装饰器"""
    print("\n=== 测试认证装饰器 ===")
    
    app = create_app('testing')
    
    # 注册测试路由
    @app.route('/api/test/public')
    def public_route():
        return jsonify({'message': 'Public route'})
    
    @app.route('/api/test/protected')
    @require_auth
    def protected_route():
        user = get_current_user()
        return jsonify({'user': user.to_dict()})
    
    @app.route('/api/test/admin-only')
    @require_admin
    def admin_route():
        return jsonify({'message': 'Admin access granted'})
    
    with app.test_client() as client:
        # 测试公开路由
        response = client.get('/api/test/public')
        assert response.status_code == 200
        print("✓ 公开路由可访问")
        
        # 测试受保护路由（无 token）
        response = client.get('/api/test/protected')
        assert response.status_code == 401
        print("✓ 受保护路由需要认证")
        
        # 测试管理员路由（无认证）
        response = client.get('/api/test/admin-only')
        assert response.status_code == 401
        print("✓ 管理员路由需要认证")
    
    print("认证装饰器测试通过！\n")


def test_user_database():
    """测试数据库操作"""
    print("\n=== 测试数据库操作 ===")
    
    app = create_app('testing')
    
    with app.app_context():
        # 创建表
        db.create_all()
        
        # 创建用户
        user = User(username='dbuser', email='dbuser@example.com', role='user')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # 查询用户
        found_user = User.query.filter_by(username='dbuser').first()
        assert found_user is not None
        assert found_user.email == 'dbuser@example.com'
        assert found_user.check_password('password123')
        print("✓ 用户数据库操作正常")
        
        # 清理
        db.session.delete(found_user)
        db.session.commit()
    
    print("数据库操作测试通过！\n")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("权限系统测试")
    print("=" * 60)
    
    try:
        test_user_model()
        test_auth_decorators()
        test_user_database()
        
        print("=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
        return 0
    except Exception as e:
        print("=" * 60)
        print(f"❌ 测试失败：{e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
