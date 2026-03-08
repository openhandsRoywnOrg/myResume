"""
Authentication API routes

Provides login, register, and token management endpoints
"""
from flask import request, jsonify, Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from datetime import timedelta

from app import db
from app.models.user import User
from app.api.deps import require_auth, AuthenticationError

# Create blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录接口

    Request JSON:
        {
            "username": "string",
            "password": "string"
        }

    Response JSON:
        {
            "access_token": "string",
            "refresh_token": "string",
            "user": {
                "id": "int",
                "username": "string",
                "role": "string"
            }
        }
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing request body'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Find user
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    # Check password
    if not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Check if user is active
    if not user.is_active:
        return jsonify({'error': 'User account is inactive'}), 401

    # Create tokens
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(hours=1)
    )
    refresh_token = create_refresh_token(
        identity=user.id,
        expires_delta=timedelta(days=30)
    )

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    用户注册接口

    Request JSON:
        {
            "username": "string",
            "email": "string",
            "password": "string"
        }

    Response JSON:
        {
            "message": "User registered successfully",
            "user": {
                "id": "int",
                "username": "string",
                "email": "string",
                "role": "string"
            }
        }
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing request body'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400

    # Validate username
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400

    # Validate email
    if '@' not in email or '.' not in email:
        return jsonify({'error': 'Invalid email format'}), 400

    # Validate password
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 409

    # Create new user
    user = User(
        username=username,
        email=email,
        role='user'  # Default role
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    刷新 access token

    使用 refresh token 获取新的 access token

    Response JSON:
        {
            "access_token": "string"
        }
    """
    current_user_id = get_jwt_identity()

    # Verify user still exists and is active
    user = User.query.get(current_user_id)
    if not user or not user.is_active:
        return jsonify({'error': 'User not found or inactive'}), 401

    # Create new access token
    access_token = create_access_token(
        identity=current_user_id,
        expires_delta=timedelta(hours=1)
    )

    return jsonify({'access_token': access_token}), 200


@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user_info():
    """
    获取当前用户信息

    Response JSON:
        {
            "user": {
                "id": "int",
                "username": "string",
                "email": "string",
                "role": "string"
            }
        }
    """
    from app.api.deps import get_current_user
    user = get_current_user()

    return jsonify({
        'user': user.to_dict(include_email=True)
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """
    用户登出

    将当前 token 加入黑名单（需要配置 JWT 黑名单）

    Response JSON:
        {
            "message": "Successfully logged out"
        }
    """
    # Get the JWT ID (jti) for the current token
    jti = get_jwt()['jti']

    # Note: This requires a token blacklist implementation
    # For now, we just return success
    # In production, you would add jti to a blacklist

    return jsonify({'message': 'Successfully logged out'}), 200

