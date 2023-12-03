from .InfoClasses import handlers, UniversalInfo
from .Exceptions import WrongInfoTypeError
from typing import Optional, Callable
from functools import wraps

# todo
# 在这里实现关于插件注册的事件相关的代码


class EventHandler:

    def __init__(self, info: UniversalInfo):
        if info.type == "EventHandler":
            self.Event = info.on
        else:
            raise WrongInfoTypeError(info.name, info.type, "EventHandler")

    def __call__(self, func):
        handlers.get(self.Event.value, None).insert(0, func)


class CustomEvent:

    def __init__(self, info: UniversalInfo):
        if info.type == "EventHandler":
            self.Event = info.on
        else:
            raise WrongInfoTypeError(info.name, info.type, "EventHandler")
        self.HandlerList = []

    def AddHandler(self, name: str, func: Optional[Callable] = None):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.HandlerList.append(func)
            result = func(*args, **kwargs)
            return result

        return wrapper
