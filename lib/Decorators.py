from enum import Enum

handlers = {
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


def GetEventHandlers(name: str):
    if name in handlers.keys():
        return handlers.get(name)
