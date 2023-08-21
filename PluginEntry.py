from lib.log import log as log
from Plugins import *
import Plugins.PluginList as PluginList
import flet
import gc
import importlib

#定义运行中保存的字典
on_load_func_dict = {}
on_enable_func_dict = {}
on_disable_func_dict = {}
on_load_classes_dict = {}
on_enable_classes_dict = {}
on_disable_classes_dict = {}

def before_run(name:str,page:flet.Page):
    log(f"在{name}初始化之前调用总入口点")
    log(f"当前Plugin List:{PluginList.Pluginlist}")
    for index in PluginList.Pluginlist:
        if index["Loadtime"] == 'before':
            log(f"已找到注册的插件,信息为{index}")
            if index["Location"] == name:
                index["EntryPoint"](page)
    
def after_run(name:str,page:flet.Page,**kwargs):
    log(f"在{name}初始化之后调用总入口点")
    for index in PluginList.Pluginlist:
        if index["Loadtime"] == 'after':
            log(f"已找到注册的插件,信息为{index}")
            file_Name = index["file"]
            if index["Location"] == name:
                
                #创建变量方便后期调用
                call_funcs = {}
                call_vars = {}
                use_thread_class = False
                target_func
                target_thread_class                
                
                # 此处开始处理插件注册的信息     
                # 处理插件需要获取的程序变量和函数           
                need_args = index["args"]
                if "need_vars" in need_args.keys(): # 传递变量
                    need_vars = need_args["need_vars"]
                    for var_name in need_vars:
                        if var_name in kwargs["global_vars"].keys():
                            call_vars.append(need_vars,kwargs["global_vars"][var_name])
                            
                if "need_funcs" in need_args.keys(): # 传递函数
                    need_funcs = need_args["need_funcs"]
                    for func_name in need_funcs:
                        if func_name in kwargs["funcs"]:
                            call_funcs.append(func_name,func_name)  
                                          
                for key in index.keys():                               
                    match key:
                        case "unsafe": # unsafe关键字检测，目前还没有正式实现相关功能
                            unsafe = index["unsafe"]
                            
                        case "muti_thread": # 检测是否使用多线程
                            if "thread_class" in index.keys() and index["thread_class"] != None:
                                m = importlib.import_moudle("Plugins."+file_Name)
                                thread_class = hasattr(m,index["thread_class"])
                                if thread_class == True:
                                    thread_class = getattr(m,index["thread_class"])
                                    if hasattr(thread_class,"run"):
                                        target_thread_class = thread_class
                                        use_thread_class = True
                                    else:
                                        log("指定的对象没有run方法",2)
                            else:
                                log("指定的对象不存在",2)
                            gc.collect()
                            
                        case "events": # 添加事件处理
                            dict_events = index["events"]
                            file_Name = index["File"]
                            m = importlib.import_moudle("Plugins."+file_Name)
                            for key in dict_events.keys():
                                match key:                                
                                    case "on_load": # 处理on_load键传入的参数                                        
                                        if dict_events[key][0] == "func": # 是函数                                                                                    
                                            on_load_func = getattr(m,dict_events["on_load"])          
                                            if on_load_func != None:                          
                                                global on_load_func_dict
                                                on_load_func_dict.append("Plugins."+file_Name,on_load_func)
                                                target_func = on_load_func
                                                
                                        elif isinstance(dict_events[key],dict): # 是字典
                                            target_dict = dict_events[key]
                                            dict_keys = dict_events[key].keys()
                                            if "mode" in dict_keys and "type" in dict_keys and "value" in dict_keys: # 是合法字典,开始处理
                                                match target_dict["type"]:
                                                    case "class":
                                                        target_load_class = getattr(m,target_dict["value"])
                                                        if target_load_class != None:
                                                            global on_load_classes_dict
                                                            on_load_classes_dict.append("Plugins."+file_Name,target_dict["value"])
                                                                                               
                                    case "on_enable": # 处理on_enable键传入的参数
                                        if dict_events[key][0] == "func": # 是函数                                                                                    
                                            on_enable_func = getattr(m,dict_events["on_enable"])          
                                            if on_enable_func != None:                          
                                                global on_enable_func_dict
                                                on_enable_func_dict.append("Plugins."+file_Name,on_enable_func)
                                                
                                        elif isinstance(dict_events[key],dict): # 是字典
                                            target_dict = dict_events[key]
                                            dict_keys = dict_events[key].keys()
                                            if "mode" in dict_keys and "type" in dict_keys and "value" in dict_keys: # 是合法字典,开始处理
                                                match target_dict["type"]:
                                                    case "class":
                                                        target_enable_class = getattr(m,target_dict["value"])
                                                        if target_enable_class != None:
                                                            global on_enable_classes_dict
                                                            on_enable_classes_dict.append("Plugins."+file_Name,target_dict["value"])
                                    
                                    case "on_disable": # 处理on_disable键传入的参数
                                        if dict_events[key][0] == "func": # 是函数                                                                                    
                                            on_disable_func = getattr(m,dict_events["on_disable"])          
                                            if on_disable_func != None:                          
                                                global on_disable_func_dict
                                                on_disable_func_dict.append("Plugins."+file_Name,on_disable_func)
                                                        
                                        elif isinstance(dict_events[key],dict): # 是字典
                                            target_dict = dict_events[key]
                                            dict_keys = dict_events[key].keys()
                                            if "mode" in dict_keys and "type" in dict_keys and "value" in dict_keys: # 是合法字典,开始处理
                                                match target_dict["type"]:
                                                    case "class":
                                                        target_disable_class = getattr(m,target_dict["value"])
                                                        if target_disable_class != None:
                                                            global on_disable_classes_dict
                                                            on_disable_classes_dict.append("Plugins."+file_Name,target_dict["value"])
                                        
                            gc.collect()                    
                                 
                # 处理完成,准备调用                               
                if use_thread_class == false:
                    target_func(need_funcs=need_funcs,need_vars=need_vars)
                else:
                    target_thread_class.run(target=target_func,need_vars=need_vars,need_funcs=need_funcs)