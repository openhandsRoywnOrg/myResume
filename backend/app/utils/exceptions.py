"""
自定义异常类

用于应用程序中的错误处理
"""


class AppException(Exception):
    """应用基础异常"""
    def __init__(self, message: str, code: str = 'APP_ERROR', status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(AppException):
    """数据验证错误"""
    def __init__(self, message: str, field: str = None):
        super().__init__(message=message, code='VALIDATION_ERROR', status_code=400)
        self.field = field


class NotFoundError(AppException):
    """资源未找到错误"""
    def __init__(self, message: str = 'Resource not found', resource: str = None):
        super().__init__(message=message, code='NOT_FOUND', status_code=404)
        self.resource = resource


class AuthenticationError(AppException):
    """认证错误"""
    def __init__(self, message: str = 'Authentication failed'):
        super().__init__(message=message, code='AUTH_ERROR', status_code=401)


class PermissionError(AppException):
    """权限错误"""
    def __init__(self, message: str = 'Permission denied'):
        super().__init__(message=message, code='PERMISSION_DENIED', status_code=403)


class DatabaseError(AppException):
    """数据库错误"""
    def __init__(self, message: str = 'Database error'):
        super().__init__(message=message, code='DATABASE_ERROR', status_code=500)
