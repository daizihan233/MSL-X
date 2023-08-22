import sys
sys.path.append("..") 
from lib.log import log

Pluginlist = []

log("PluginList已被调用")

default_info = {
    "name": "AnonymousPlugin",
    "author": "Anonymous",
    "description": "",
    "version": "1.0.0"
}


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
            'file': self.plugin_info['file'],
        }
        if args := self.plugin_info.get('args') is not None:
            TargetPlugin["args"] = self.plugin_info['args']
        Pluginlist.append(TargetPlugin)
        name = TargetPlugin["Name"]
        location = TargetPlugin["Location"]
        time = TargetPlugin["Loadtime"]
        log(f"已注册插件{name},位置为{location}[{time}]")
