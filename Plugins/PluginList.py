import sys,os
sys.path.append("..") 
from lib.log import log

Pluginlist = []

log("PluginList已被调用")

default_info = {
    "name": "AnonymousPlugin",
    "author": "Anonymous",
    "description": "",
    "version": "1.0.0",
    "need_page": False
}

class PluginInfo(object):
    def __init__(self, name="AnonymosPlugin", author="Anonymous", description="", version="1.0.0", need_page=False,args={}, unsafe=False, muti_thread=False, thread_class=None, location=("main","after"), file=os.path.basename(__file__),events={} ):
        self.name = name
        self.author = author
        self.description = description
        self.version = version
        self.need_page = need_page
        self.args = args
        self.unsafe = unsafe
        self.muti_thread = muti_thread
        self.thread_class = thread_class
        self.location = location
        self.file = file
        self.events = events
        self.need_funcs = []
        self.need_args = []
        self.on_load = None
        self.on_enable = None
        self.on_disable = None
        if "need_funcs" in args.keys():
            self.need_funcs = args["need_funcs"]
        if "need_vars" in args.keys():
            self.need_args  = args["need_args"]
        if "on_load" in events.keys():
            self.on_load = events["on_load"]
        if "on_enable" in events.keys():
            self.on_enable = events["on_enable"]
        if "on_disable" in events.keys():
            self.on_disable = events["on_disable"]

default_info_class = PluginInfo()

class AddPluginInfo(object):
    def __init__(self, plugin_info: PluginInfo = default_info_class):
        process_location = plugin_info.location[0]
        load_time = plugin_info.location[1]
        log(f"装饰器被init了一次:{process_location},{load_time},{plugin_info.name}")
        self.process_location = process_location
        self.plugin_info = plugin_info
        self.load_time = load_time

    def __call__(self, func):
        log(f"装饰器被{func}Call了一次")
        global Pluginlist
        TargetPlugin = {
            "Name": self.plugin_info.name,
            "Location": self.plugin_info.location[0],
            "Loadtime": self.plugin_info.location[1],
            "EntryPoint": func,
            'need_page': self.plugin_info.need_page,
            'file': self.plugin_info.file,
        }
        if args := self.plugin_info.args is not None:
            TargetPlugin["args"] = self.plugin_info.args
        Pluginlist.append(TargetPlugin)
        name = TargetPlugin["Name"]
        location = TargetPlugin["Location"]
        time = TargetPlugin["Loadtime"]
        log(f"已注册插件{name},位置为{location}[{time}]")



class RegisterPlugin(object):
    def __init__(self, plugin_info: dict = default_info):
        process_location = plugin_info["location"][0]
        load_time = plugin_info["location"][1]
        log(f"装饰器被init了一次:{process_location},{load_time},{plugin_info}")
        self.process_location = process_location
        self.plugin_info = plugin_info
        self.load_time = load_time

    def __call__(self, func):
        log(f"装饰器被{func}Call了一次")
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
        log(f"已注册插件{name},位置为{location}[{time}]")
