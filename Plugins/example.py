import os

from .PluginList import AddPluginInfo, PluginInfo

info = PluginInfo(name="ExamplePlugin", author="MojaveHao", description="Nope,Happy coding! =)", version="1.0.0",
                  need_page=False, location=("main", "after"))


@AddPluginInfo(info)
def foo2():
    print("Example Plugin Loaded!(After)")
