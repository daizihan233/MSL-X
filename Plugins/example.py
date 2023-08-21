from .PluginList import RegisterPlugin

info = {
    "name":"ExamplePlugin",
    "author":"MojaveHao",
    "description":"Nope,Happy coding! :)",
    "version":"1.0.0",
    "location":("main","after"),
    "File":os.path.basename(__file__)

}

@RegisterPlugin(info)
def foo(page):
    print("Example Plugin Loaded!(Before)")
    
@RegisterPlugin(info)
def foo2(page):
    print("Example Plugin Loaded!(After)")