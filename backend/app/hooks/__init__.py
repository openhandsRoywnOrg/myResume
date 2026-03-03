"""
钩子系统初始化

钩子允许在关键操作前后执行自定义逻辑
"""

from app.hooks.registry import hooks, HookRegistry, init_hooks

__all__ = ['hooks', 'HookRegistry', 'init_hooks']
