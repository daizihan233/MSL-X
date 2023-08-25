import json

class ConfCtl():
    
    def __init__(self,name="Default"):
        self.name = name
        self.path = f'/Config/{name}.json'
        self.xms = 1
        self.xmx = 4
        self.java = "java"
        self.jvm_options = []
        self.server = "server"
        self.server_path = ""
        self.description = ""
        self.name = "Default"
    
    def Load_Config(self):
        with open(self.path,'r', encoding='utf-8') as fl:
            conf_dict = json.load(fl)
            self.xms = conf_dict["xms"]
            self.xmx = conf_dict["xmx"]
            self.java = conf_dict["java"]
            self.server = conf_dict["server"]
            self.server_path = conf_dict["path"]
            self.description = conf_dict["description"]
            self.jvm_options = conf_dict["jvm_options"]
            self.name = conf_dict["name"]
            
    def Save_Config(self):
        with open(self.path,'w', encoding='utf-8') as fl:
            conf_dict = \
                {
                    "xms":self.xms,
                    "xmx":self.xmx,
                    "java":self.java,
                    "server":self.server,
                    "path":self.server_path,
                    "description":self.description,
                    "jvm_options":self.jvm_options,
                    "name":self.name                                    
                }
            conf_json = json.dump(conf_dict,fl)