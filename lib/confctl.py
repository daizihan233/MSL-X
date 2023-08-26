import json
from loguru import logger
logger.add('Logs/{time:YYYY-MM-DD}-ConfCtl.log', format='[{time:HH:mm:ss}][{level}] {message}', encoding='utf-8', backtrace=True, diagnose=True, compression="tar.gz" )

class ConfCtl():
    
    def __init__(self,name="Default"):
        self.name = name
        self.path = f'Config/{name}.json'
        self.xms = 1
        self.xmx = 4
        self.java = "java"
        self.jvm_options = []
        self.server = "server"
        self.server_path = ""
        self.description = ""
        self.name = "Default"
    
    @logger.catch
    def Load_Config(self):
        with open(self.path,'r', encoding='utf-8') as fl:
            conf_dict = json.load(fl)
            try:
                self.xms = conf_dict["xms"]
                self.xmx = conf_dict["xmx"]
                self.java = conf_dict["java"]
                self.server = conf_dict["server"]
                self.server_path = conf_dict["path"]
                self.description = conf_dict["description"]
                self.jvm_options = conf_dict["jvm_options"]
                self.name = conf_dict["name"]
            except KeyError:
                self.Save_Config()
                logger.warning("检测到配置文件损坏,已写入默认设置")
            
    @logger.catch        
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