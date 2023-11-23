import os
import sys
import inspect
from enum import Enum
from threading import Thread
from typing import Optional

sys.path.append("..")
from lib.log import logger

Pluginlist = []

handlers = {
    "StartServerEvent": [],
    "SelectHomepageEvent": [],
    "SelectFrpcPageEvent": [],
    "SelectAboutPageEvent": [],
}

default_info = {
    "name": "AnonymousPlugin",
    "author": "Anonymous",
    "description": "",
    "version": "1.0.0",
    "need_page": False
}


class PluginInfo(object):  # 新版本的插件信息类
    def __init__(self, name: str = "AnonymousPlugin", author: str = "Anonymous", description: str = "",
                 version: str = "1.0.0", need_page: bool = False, args: dict = {}, unsafe: bool = False,
                 multi_thread: bool = False, thread_class: Optional[Thread] = None, location: tuple = ("main", "after"),
                 file: str = inspect.currentframe().f_back.f_code.co_filename, events: dict = {}):
        self.name = name
        self.author = author
        self.description = description
        self.version = version
        self.need_page = need_page
        self.args = args
        self.unsafe = unsafe
        self.multi_thread = multi_thread
        self.thread_class = thread_class
        self.location = location
        self.file = file
        self.events = events
        # self.need_funcs = []
        self.need_args = []
        self.on_load = None
        self.on_enable = None
        self.on_disable = None
        # if "need_funcs" in args.keys():
        #     self.need_funcs = args["need_funcs"]
        if "need_vars" in args.keys():
            self.need_args = args["need_args"]
        if "on_load" in events.keys():
            self.on_load = events["on_load"]
        if "on_enable" in events.keys():
            self.on_enable = events["on_enable"]
        if "on_disable" in events.keys():
            self.on_disable = events["on_disable"]


default_info_class = PluginInfo()


class AddPluginInfo(object):  # 接受插件信息类的新版修饰器
    def __init__(self, plugin_info: PluginInfo = default_info_class):
        process_location = plugin_info.location[0]
        # load_time = plugin_info.location[1]
        # logger.debug(f"装饰器被init了一次:{process_location},{load_time},{plugin_info.name}")
        self.process_location = process_location
        self.plugin_info = plugin_info
        # self.load_time = load_time

    def __call__(self, func):
        # logger.debug(f"装饰器被{func}Call了一次")
        global Pluginlist
        TargetPlugin = {
            "Name": self.plugin_info.name,
            "Location": self.plugin_info.location[0],
            "EntryPoint": func,
            'version': self.plugin_info.version,
            'author': self.plugin_info.author,
            'need_page': self.plugin_info.need_page,
            'file': self.plugin_info.file,
            'class': self.plugin_info
        }
        if self.plugin_info.args is not None:
            TargetPlugin["args"] = self.plugin_info.args
        Pluginlist.append(TargetPlugin)
        name = TargetPlugin["Name"]
        location = TargetPlugin["Location"]
        # time = TargetPlugin["Loadtime"]
        logger.info(f"已在{location}注册插件{name}")


class RegisterPlugin(object):  # 接受字典的老版本修饰器
    def __init__(self, plugin_info: dict = default_info):
        process_location = plugin_info["location"][0]
        load_time = plugin_info["location"][1]
        logger.debug(f"装饰器被init了一次:{process_location},{load_time},{plugin_info}")
        self.process_location = process_location
        self.plugin_info = plugin_info
        self.load_time = load_time

    def __call__(self, func):
        logger.debug(f"装饰器被{func}Call了一次")
        global Pluginlist
        TargetPlugin = {
            "Name": self.plugin_info["name"],
            "Location": self.plugin_info["location"][0],
            "Loadtime": self.plugin_info["location"][1],
            "EntryPoint": func,
            'need_page': self.plugin_info["need_page"],
            'file': self.plugin_info['file'],
        }
        if args := self.plugin_info.get('args') is not None:
            TargetPlugin["args"] = self.plugin_info['args']
        Pluginlist.append(TargetPlugin)
        name = TargetPlugin["Name"]
        location = TargetPlugin["Location"]
        time = TargetPlugin["Loadtime"]
        logger.info(f"已注册插件{name},位置为{location}")


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
        logger.debug(f"已注册{self.Event.value}的新Handler:{func}")
