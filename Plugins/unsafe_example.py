from .PluginList import RegisterPlugin
import flet

info = {
    "name":"UnsafeExamplePlugin",
    "author":"MojaveHao",
    "description":"Nope,Happy coding! :)",
    "version":"1.0.0",
    "args":
    {
        "need_funcs":[],
        "need_vars":[],
    },
    "unsafe":True,
    "muti_thread":True,
    "thread_class":"Start_Plugin_Thread",
    "location":("main","after"),
    "events":
    {
        "on_load":("func","name"),
        "on_enable":("func","name"),
        "on_disable":("func","name"),
    }
}
'''
@RegisterPlugin("main","after",info)
def unsafe_foo(page:flet.Page):
    print("Example Plugin Loaded!(After)")
'''