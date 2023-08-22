from lib.log import log as log
from Plugins import *
import Plugins.PluginList as PluginList
import flet
import gc
import importlib
from threading import Thread

# 定义运行中保存的字典
on_load_func_dict = {}
on_enable_func_dict = {}
on_disable_func_dict = {}
on_load_classes_dict = {}
on_enable_classes_dict = {}
on_disable_classes_dict = {}

def before_run(name: str, page: flet.Page):
    log(f"在{name}初始化之前调用总入口点")
    log(f"当前Plugin List:{PluginList.Pluginlist}")
    for index in PluginList.Pluginlist:
        if index["Loadtime"] == 'before':
            log(f"已找到注册的插件,信息为{index}")
            if index["Location"] == name:
                # 创建变量方便后期调用
                call_funcs = {}
                call_vars = {}
                use_thread_class = False
                target_func: Callable = index["EntryPoint"]
                target_thread_class: Thread
                need_funcs: List = []
                need_vars: List = []
                need_page = False

                # 此处开始处理插件注册的信息
                # 处理插件需要获取的程序变量和函数
                need_args = index.get("args")
                if need_args is not None:
                    if need_vars := need_args.get('need_vars'):  # 传递变量
                        for var_name in need_vars:
                            if var_name in kwargs["global_vars"].keys():
                                call_vars[need_vars] = kwargs["global_vars"][var_name]

                    if need_funcs := need_args.get('need_funcs'):  # 传递函数
                        for func_name in need_funcs:
                            if func_name in kwargs["funcs"]:
                                call_funcs[func_name] = func_name
                else:
                    log("没有检测到args键,已跳过处理")

                for key in index.keys():
                    match key:
                        case "events":  # 添加事件处理
                            dict_events = index["events"]
                            file_Name = index["File"]
                            m = importlib.import_module("Plugins."+file_Name)
                            for key in dict_events.keys():
                                match key:
                                    case "on_load":  # 处理on_load键传入的参数
                                        if dict_events[key][0] == "func":  # 是函数
                                            on_load_func = getattr(m, dict_events["on_load"])
                                            if on_load_func != None:
                                                global on_load_func_dict
                                                on_load_func_dict["Plugins." + file_Name] = on_load_func
                                                target_func = on_load_func
                                                log("要执行的目标函数已替换为on_load中指定的函数")

                                        elif isinstance(dict_events[key], dict):  # 是字典
                                            target_dict = dict_events[key]
                                            dict_keys = dict_events[key].keys()
                                            if "mode" in dict_keys and "type" in dict_keys and "value" in dict_keys:  # 是合法字典,开始处理
                                                match target_dict["type"]:
                                                    case "class":
                                                        target_load_class = getattr(
                                                            m, target_dict["value"])
                                                        if target_load_class != None:
                                                            global on_load_classes_dict
                                                            on_load_classes_dict["Plugins." +
                                                                                 file_Name] = target_dict["value"]
                                gc.collect()                                        

                # 处理完成,准备调用
                if use_thread_class == False:
                    log("[Before]没有使用thread类,将直接调用函数")
                    if bool(need_funcs) == False:
                        if bool(need_vars) == False:
                            if need_page == False:
                                target_func()
                            else:
                                target_func(page)
                        else:
                            if need_page == False:
                                target_func(need_vars=need_vars)
                            else:
                                target_func(page,need_vars=need_vars)
                    else:
                        log("[Before]检测到使用了thread类")
                        if need_page == False:
                            target_func(page,need_funcs=need_funcs,need_vars=need_vars)
                        else:
                            target_func(page,need_funcs=need_funcs,need_vars=need_vars)
                else:
                    target_thread_class.run(
                        target=target_func, need_vars=need_vars, need_funcs=need_funcs)
                    if bool(need_funcs) == False:
                        if bool(need_vars) == False:
                            if need_page == False:
                                target_thread_class.run(
                            target=target_func)
                            else:
                                target_thread_class.run(
                            target=target_func,page=page)
                        else:
                            if need_page == False:
                                target_thread_class.run(
                            target=target_func, need_vars=need_vars)
                            else:
                                target_thread_class.run(
                            target=target_func, need_vars=need_vars,page=page)
                    else:
                        if need_page == False:
                            target_thread_class.run(
                            target=target_func, need_vars=need_vars, need_funcs=need_funcs)
                        else:
                            target_thread_class.run(
                            target=target_func, need_vars=need_vars, need_funcs=need_funcs,page=page)

def after_run(name: str, page: flet.Page, **kwargs):
    log(f"在{name}初始化之后调用总入口点")
    for index in PluginList.Pluginlist:
        if index["Loadtime"] == 'after':
            log(f"已找到注册的插件,信息为{index}")
            file_Name = index["file"]
            if index["Location"] == name:

                # 创建变量方便后期调用
                call_funcs = {}
                call_vars = {}
                use_thread_class = False
                target_func: Callable = index["EntryPoint"]
                target_thread_class: Thread
                need_funcs: List = []
                need_vars: List = []
                need_page = False

                # 此处开始处理插件注册的信息
                # 处理插件需要获取的程序变量和函数
                need_args = index.get("args")
                if need_args is not None:
                    if need_vars := need_args.get('need_vars'):  # 传递变量
                        for var_name in need_vars:
                            if var_name in kwargs["global_vars"].keys():
                                call_vars[need_vars] = kwargs["global_vars"][var_name]

                    if need_funcs := need_args.get('need_funcs'):  # 传递函数
                        for func_name in need_funcs:
                            if func_name in kwargs["funcs"]:
                                call_funcs[func_name] = func_name
                else:
                    log("没有检测到args键,已跳过处理")

                for key in index.keys():
                    match key:
                        case "unsafe":  # unsafe关键字检测，目前还没有正式实现相关功能
                            unsafe = index["unsafe"]
                            
                        case "need_page":  # need_page关键字检测，如果为True则传入page参数
                            need_page = index["need_page"]

                        case "muti_thread":  # 检测是否使用多线程
                            if "thread_class" in index.keys() and index["thread_class"] != None:
                                m = importlib.import_module(
                                    "Plugins."+file_Name)
                                thread_class = hasattr(
                                    m, index["thread_class"])
                                if thread_class == True:
                                    thread_class = getattr(
                                        m, index["thread_class"])
                                    if hasattr(thread_class, "run"):
                                        target_thread_class = thread_class
                                        use_thread_class = True
                                    else:
                                        log("指定的对象没有run方法", 2)
                            else:
                                log("指定的对象不存在", 2)
                            gc.collect()

                        case "events":  # 添加事件处理
                            dict_events = index["events"]
                            file_Name = index["File"]
                            m = importlib.import_module("Plugins."+file_Name)
                            for key in dict_events.keys():
                                match key:
                                    case "on_load":  # 处理on_load键传入的参数
                                        if dict_events[key][0] == "func":  # 是函数
                                            on_load_func = getattr(m, dict_events["on_load"])
                                            if on_load_func != None:
                                                global on_load_func_dict
                                                on_load_func_dict["Plugins." + file_Name] = on_load_func
                                                target_func = on_load_func
                                                log("要执行的目标函数已替换为on_load中指定的函数")

                                        elif isinstance(dict_events[key], dict):  # 是字典
                                            target_dict = dict_events[key]
                                            dict_keys = dict_events[key].keys()
                                            if "mode" in dict_keys and "type" in dict_keys and "value" in dict_keys:  # 是合法字典,开始处理
                                                match target_dict["type"]:
                                                    case "class":
                                                        target_load_class = getattr(
                                                            m, target_dict["value"])
                                                        if target_load_class != None:
                                                            global on_load_classes_dict
                                                            on_load_classes_dict["Plugins." +
                                                                                 file_Name] = target_dict["value"]

                                    case "on_enable":  # 处理on_enable键传入的参数
                                        if dict_events[key][0] == "func":  # 是函数
                                            on_enable_func = getattr(
                                                m, dict_events["on_enable"])
                                            if on_enable_func != None:
                                                global on_enable_func_dict
                                                on_enable_func_dict["Plugins."+file_Name] = on_enable_func

                                        elif isinstance(dict_events[key], dict):  # 是字典
                                            target_dict = dict_events[key]
                                            dict_keys = target_dict.keys()
                                            if "mode" in dict_keys and "type" in dict_keys and "value" in dict_keys:  # 是合法字典,开始处理
                                                match target_dict["type"]:
                                                    case "class":
                                                        target_enable_class = getattr(
                                                            m, target_dict["value"])
                                                        if target_enable_class != None:
                                                            global on_enable_classes_dict
                                                            on_enable_classes_dict["Plugins."+file_Name] = target_dict["value"]

                                    case "on_disable":  # 处理on_disable键传入的参数
                                        if dict_events[key][0] == "func":  # 是函数
                                            on_disable_func = getattr(
                                                m, dict_events["on_disable"])
                                            if on_disable_func != None:
                                                global on_disable_func_dict
                                                on_disable_func_dict["Plugins."+file_Name] = on_disable_func

                                        elif isinstance(dict_events[key], dict):  # 是字典
                                            target_dict = dict_events[key]
                                            dict_keys = dict_events[key].keys()
                                            if "mode" in dict_keys and "type" in dict_keys and "value" in dict_keys:  # 是合法字典,开始处理
                                                match target_dict["type"]:
                                                    case "class":
                                                        target_disable_class = getattr(
                                                            m, target_dict["value"])
                                                        if target_disable_class != None:
                                                            global on_disable_classes_dict
                                                            on_disable_classes_dict["Plugins."+file_Name] = target_dict["value"]
                                gc.collect()                                        

                # 处理完成,准备调用
                if use_thread_class == False:
                    log("没有使用thread类,将直接调用函数")
                    if bool(need_funcs) == False:
                        if bool(need_vars) == False:
                            if need_page == False:
                                target_func()
                            else:
                                target_func(page)
                        else:
                            if need_page == False:
                                target_func(need_vars=need_vars)
                            else:
                                target_func(page,need_vars=need_vars)
                    else:
                        if need_page == False:
                            target_func(page,need_funcs=need_funcs,need_vars=need_vars)
                        else:
                            target_func(page,need_funcs=need_funcs,need_vars=need_vars)
                else:
                    log("[After]检测到使用了thread类")
                    if bool(need_funcs) == False:
                        if bool(need_vars) == False:
                            if need_page == False:
                                target_thread_class.run(
                            target=target_func)
                            else:
                                target_thread_class.run(
                            target=target_func,page=page)
                        else:
                            if need_page == False:
                                target_thread_class.run(
                            target=target_func, need_vars=need_vars)
                            else:
                                target_thread_class.run(
                            target=target_func, need_vars=need_vars,page=page)
                    else:
                        if need_page == False:
                            target_thread_class.run(
                            target=target_func, need_vars=need_vars, need_funcs=need_funcs)
                        else:
                            target_thread_class.run(
                            target=target_func, need_vars=need_vars, need_funcs=need_funcs,page=page)