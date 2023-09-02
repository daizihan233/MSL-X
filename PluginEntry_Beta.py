from typing import Callable, Dict
import importlib
import threading
import gc
from loguru import logger
from Plugins import *
from Plugins import PluginList

global_var_lock = threading.Lock()

# 日志记录器配置
logger.add('Logs/{time:YYYY-MM-DD}-PluginEntry.log', format='[{time:HH:mm:ss}][{level}] {message}', encoding='utf-8', backtrace=True, diagnose=True, compression="tar.gz")

# 定义运行中保存的字典
on_load_func_dict: Dict[str, Callable] = {}
on_enable_func_dict: Dict[str, Callable] = {}
on_disable_func_dict: Dict[str, Callable] = {}
on_load_classes_dict: Dict[str, str] = {}
on_enable_classes_dict: Dict[str, str] = {}
on_disable_classes_dict: Dict[str, str] = {}

def process_plugin_events(events, file_name):
    """
    处理插件的事件部分，将需要执行的函数或类存储在全局字典中。

    Args:
        events (Dict): 插件定义的事件。
        file_name (str): 插件的文件名。
    """
    m = importlib.import_module("Plugins." + file_name)
    for event_key, event_value in events.items():
        if event_key == "on_load":
            if event_value[0] == "func":
                on_load_func = getattr(m, event_value[1])
                if on_load_func is not None:
                    on_load_func_dict["Plugins." + file_name] = on_load_func
        elif event_key == "on_enable":
            if event_value[0] == "func":
                on_enable_func = getattr(m, event_value[1])
                if on_enable_func is not None:
                    on_enable_func_dict["Plugins." + file_name] = on_enable_func

def process_plugin_args(need_args, kwargs):
    """
    处理插件需要获取的程序变量和函数。

    Args:
        need_args (Dict): 插件定义的需要的参数。
        kwargs (Dict): 包含全局变量和函数的字典。

    Returns:
        Tuple[Dict, Dict]: 包含需要的变量和函数的字典。
    """
    call_vars = {}
    call_funcs = {}
    need_vars = need_args.get('need_vars', [])
    need_funcs = need_args.get('need_funcs', [])

    for var_name in need_vars:
        if var_name in kwargs["global_vars"]:
            call_vars[var_name] = kwargs["global_vars"][var_name]

    for func_name in need_funcs:
        if func_name in kwargs["funcs"]:
            call_funcs[func_name] = kwargs["funcs"][func_name]

    return call_vars, call_funcs

def process_thread_class(thread_class, target_func, page, need_vars, need_funcs):
    """
    处理使用线程类的情况。

    Args:
        thread_class (Thread): 插件定义的线程类。
        target_func (Callable): 目标函数。
        page (Page): 插件的页面对象。
        need_vars (Dict): 需要的变量。
        need_funcs (Dict): 需要的函数。
    """
    if not need_funcs:
        if not need_vars:
            if not page:
                thread_class.run(target=target_func)
            else:
                thread_class.run(target=target_func, page=page)
        else:
            if not page:
                thread_class.run(target=target_func, need_vars=need_vars)
            else:
                thread_class.run(target=target_func, need_vars=need_vars, page=page)

def initialize_plugin(name, page, load_time, **kwargs):
    """
    初始化插件并执行相应操作。

    Args:
        name (str): 插件的名称。
        page (Page): 插件的页面对象。
        load_time (str): 插件的加载时间（before或after）。
        kwargs (Dict): 包含全局变量和函数的字典。
    """

    for plugin in PluginList.Pluginlist:
        if plugin["Loadtime"] == load_time and plugin["Location"] == name:
            use_thread_class = False
            target_func = plugin["EntryPoint"]
            target_thread_class = None
            need_funcs = []
            need_page = False

            # 处理插件需要获取的程序变量和函数
            need_args = plugin.get("args", {})
            call_vars, call_funcs = process_plugin_args(need_args, kwargs)

            for key, value in plugin.items():
                if key == "events":
                    process_plugin_events(value, plugin["File"])
                elif key == "unsafe":
                    unsafe = value
                elif key == "need_page":
                    need_page = value
                elif key == "muti_thread":
                    if "thread_class" in plugin and plugin["thread_class"]:
                        m = importlib.import_module("Plugins." + plugin["File"])
                        if hasattr(m, plugin["thread_class"]):
                            thread_class = getattr(m, plugin["thread_class"])
                            if hasattr(thread_class, "run"):
                                target_thread_class = thread_class
                                use_thread_class = True
                            else:
                                logger.critical("指定的对象没有run方法", 2)
                    else:
                        logger.critical("指定的对象不存在", 2)
                    gc.collect()

            # 处理完成,准备调用
            if use_thread_class is False:
                logger.debug("没有使用thread类,将直接调用函数")
                if not need_funcs:
                    if not need_page:
                        target_func(**call_vars)
                    else:
                        target_func(page, **call_vars)
                else:
                    if not need_page:
                        target_func(page, need_funcs=need_funcs, **call_vars)
                    else:
                        target_func(page, need_funcs=need_funcs, **call_vars)
            else:
                logger.debug("[After]检测到使用了thread类")
                process_thread_class(target_thread_class, target_func, page, call_vars, need_funcs)

def before_run(name, page, **kwargs):
    """
    在插件初始化之前调用总入口点。

    Args:
        name (str): 插件的名称。
        page (Page): 插件的页面对象。
        kwargs (Dict): 包含全局变量和函数的字典。
    """
    initialize_plugin(name, page, 'before', **kwargs)

def after_run(name, page, **kwargs):
    """
    在插件初始化之后调用总入口点。

    Args:
        name (str): 插件的名称。
        page (Page): 插件的页面对象。
        kwargs (Dict): 包含全局变量和函数的字典。
    """
    initialize_plugin(name, page, 'after', **kwargs)

def enable_plugin(name):
    """
    启用插件时调用的函数。

    Args:
        name (str): 插件的名称。
    """
    if name in on_enable_func_dict:
        on_enable_func_dict[name]()
    elif name in on_enable_classes_dict:
        pass
    else:
        logger.error(f"没有找到{name}的开启时方法")
