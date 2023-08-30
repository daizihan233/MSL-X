import os

from .PluginList import AddPluginInfo,PluginInfo

info = PluginInfo\
(
    name="ExamplePlugin",
    author= "MojaveHao",
    description= "Nope,Happy coding! =)",
    version= "1.0.0",
    location= ("main", "after"),
    file= os.path.basename(__file__),
    need_page= False
)

@AddPluginInfo(info)
def foo2():
    print("Example Plugin Loaded!(After)")
