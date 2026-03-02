"""
钩子系统 - Hook Registry

钩子允许在关键操作前后执行自定义逻辑，例如：
- 数据验证
- 审计日志
- 级联操作
- 缓存更新

使用示例：
    from app.hooks import hooks
    
    # 注册钩子
    @hooks.register('before_topic_save')
    def validate_topic(data, **kwargs):
        if not data.get('title'):
            raise ValidationError("Title is required")
    
    # 触发钩子
    hooks.trigger('before_topic_save', data=topic_data)
"""

from typing import Any, Callable, Dict, List, Optional


class HookRegistry:
    """钩子注册表"""
    
    def __init__(self):
        self._hooks: Dict[str, List[Callable]] = {}
    
    def register(self, event: str) -> Callable:
        """
        注册钩子函数
        
        Args:
            event: 事件名称，如 'before_topic_save'
            
        Returns:
            装饰器函数
            
        示例:
            @hooks.register('before_topic_save')
            def validate_topic(data, **kwargs):
                pass
        """
        def decorator(func: Callable) -> Callable:
            if event not in self._hooks:
                self._hooks[event] = []
            self._hooks[event].append(func)
            return func
        return decorator
    
    def trigger(self, event: str, *args: Any, **kwargs: Any) -> List[Any]:
        """
        触发事件的所有钩子
        
        Args:
            event: 事件名称
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            所有钩子函数的返回值列表
            
        Raises:
            钩子函数抛出的任何异常
        """
        results = []
        for hook in self._hooks.get(event, []):
            result = hook(*args, **kwargs)
            results.append(result)
        return results
    
    def clear(self, event: Optional[str] = None):
        """
        清除钩子
        
        Args:
            event: 要清除的事件名称，如果为 None 则清除所有
        """
        if event:
            self._hooks.pop(event, None)
        else:
            self._hooks.clear()
    
    def get_hooks(self, event: str) -> List[Callable]:
        """
        获取事件的所有钩子函数
        
        Args:
            event: 事件名称
            
        Returns:
            钩子函数列表
        """
        return self._hooks.get(event, []).copy()


# 全局钩子注册表实例
hooks = HookRegistry()


def init_hooks():
    """初始化钩子系统"""
    # 这里可以注册默认的钩子
    pass


__all__ = ['hooks', 'HookRegistry', 'init_hooks']
