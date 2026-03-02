"""
API Blueprint v1

所有 API v1 版本的路由都注册在这里
"""

from flask import Blueprint

# 创建 Blueprint
api_bp = Blueprint('api_v1', __name__)

# 导入路由（暂时为空，后续 Issue 会添加）
# from . import topics
# from . import questions

# 健康检查端点
@api_bp.route('/health')
def health_check():
    """API 健康检查"""
    return {'status': 'ok', 'version': 'v1'}
