import sys
sys.path.append("..") 
from lib.log import log as log

Pluginlist = []

'''
Plugin Info Example

{
    "name":"",
    "author":"",
    "description":"",
    "version":"x.x.x"
}

'''

log("PluginList已被调用")

default_info = {
    "name":"AnonymousPlugin",
    "author":"Anonymous",
    "description":"",
    "version":"1.0.0"
}

class RegisterPlugin(object):
    def __init__(self,process_location,load_time,plugin_info=default_info):
        log(f"修饰器被init了一次:{process_location},{load_time},{plugin_info}")
        self.process_location = process_location
        self.plugin_info = plugin_info
        self.load_time = load_time

    def __call__(self,func):
        log(f"修饰器被{func}Call了一次")
        global Pluginlist
        TargetPlugin = {"Name":self.plugin_info["name"],"Location":self.process_location,"Information":self.plugin_info,"Loadtime":self.load_time.lower(),"EntryPoint":func}
        Pluginlist.append(TargetPlugin)
        name = TargetPlugin["Name"]
        location = TargetPlugin["Location"]
        time = TargetPlugin["Loadtime"]
        log(f"已注册插件{name},位置为{location}[{time}]")