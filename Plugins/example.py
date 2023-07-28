from .PluginList import RegisterPlugin

info = {
    "name":"ExamplePlugin",
    "author":"MojaveHao",
    "description":"Nope,Happy coding! :)",
    "version":"1.0.0"
}

@RegisterPlugin("main","before",info)
def foo(page):
    print("Example Plugin Loaded!(Before)")
    
@RegisterPlugin("main","after",info)
def foo2(page):
    print("Example Plugin Loaded!(After)")