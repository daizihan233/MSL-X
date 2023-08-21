import sys
import os
sys.path.append("..") 
from lib.log import log as log

Pluginlist = []

log("PluginList已被调用")

default_info = \
{
    "name":"AnonymousPlugin",
    "author":"Anonymous",
    "description":"",
    "version":"1.0.0"
}

class RegisterPlugin(object):
    def __init__(self,plugin_info=default_info):
        log(f"修饰器被init了一次:{process_location},{load_time},{plugin_info}")
        self.process_location = process_location
        self.plugin_info = plugin_info
        self.load_time = load_time

    def __call__(self,func):
        log(f"修饰器被{func}Call了一次")
        global Pluginlist
        TargetPlugin = \
        {
            "Name":self.plugin_info["name"],
            "Location":self.plugin_info["location"][0],
            "Loadtime":self.plugin_info["location"][1],
            "EntryPoint":func,
        }
        Pluginlist.append(TargetPlugin)
        name = TargetPlugin["Name"]
        location = TargetPlugin["Location"]
        time = TargetPlugin["Loadtime"]
        log(f"已注册插件{name},位置为{location}[{time}]")