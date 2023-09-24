import importlib
from typing import Callable
from enum import Enum

handlers = \
    {
        "StartServerEvent": [],
        "SelectHomepageEvent": [],
        "SelectFrpcPageEvent": [],
        "SelectAboutPageEvent": [],
    }
"""
Handlers示例
{
    "StartServerEvent":
    [
        func1(default,latest),
        func2(backup1),
        func3(backup2),
        ...
    ],
    ...
}

"""


class MSLXEvents(Enum):
    # 切换页面的事件
    SelectHomepageEvent = "SelectHomepageEvent"
    SelectFrpcPageEvent = "SelectFrpcPageEvent"
    SelectAboutPageEvent = "SelectAboutPageEvent"

    # 一些函数的事件
    StartServerEvent = "StartServerEvent"
    CloseWindowEvent = "CloseWindowEvent"


class EventHandler:

    def __init__(self, Event: MSLXEvents):
        self.Event = Event

    def __call__(self, func):
        handlers[self.Event.value].insert(0, func)


class export:

    def __init__(self) -> object:
        pass

    def __call__(func: Callable):
        m = importlib.import_moudle("Emptiness")
        setattr(m, func.__name__, func)


def ProcessEvent(name: str):
    if name in handlers.keys():
        return handlers.get(name)
