# 程序会在页面初始化前加载before_run(),在页面初始化后加载after_run()

from lib.log import log as log
from Plugins import *
import Plugins.PluginList as PluginList

def before_run(name,page):
    log(f"在{name}初始化之前调用总入口点")
    log(f"当前Plugin List:{PluginList.Pluginlist}")
    for index in PluginList.Pluginlist:
        if index["Loadtime"] == 'before':
            log(f"已找到注册的插件,信息为{index}")
            if index["Location"] == name:
                index["EntryPoint"](page)
    
def after_run(name,page):
    log(f"在{name}初始化之后调用总入口点")
    for index in PluginList.Pluginlist:
        if index["Loadtime"] == 'after':
            log(f"已找到注册的插件,信息为{index}")
            if index["Location"] == name:
                index["EntryPoint"](page)