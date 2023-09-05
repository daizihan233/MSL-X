import json
from loguru import logger
from typing import Any
from os import sep
from .info_classes import SingleServerInfo
logger.add('Logs/{time:YYYY-MM-DD}-ConfCtl.log', format='[{time:HH:mm:ss}][{level}] {message}', encoding='utf-8', backtrace=True, diagnose=True, compression="tar.gz" )

class ConfCtl():
    
    def __init__(self,name:str="Default",full_path=""):
        self.name = name
        self.xms = 1
        self.xmx = 4
        self.java = "java"
        self.server = "server"
        self.server_path = ""
        self.description = ""
        self.name = "Default"
        self.jvm_options = \
        [
            "-XX:+UnlockExperimentalVMOptions",
            "-XX:MaxGCPauseMillis=100",
            "-XX:+DisableExplicitGC",
            "-XX:TargetSurvivorRatio=90", 
            "-XX:G1NewSizePercent=50", 
            "-XX:G1MaxNewSizePercent=80",
            "-XX:G1MixedGCLiveThresholdPercent=35", 
            "-XX:+AlwaysPreTouch", 
            "-XX:+ParallelRefProcEnabled", 
            "-Dusing.aikars.flags=mcflags.emc.gs"
        ]
        if full_path == "":
            self.path = f'Config{sep}{name}.json'
        else:
            self.path = full_path
            logger.debug(f"已使用{full_path}替换self.path")
    
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
            conf_dict:Any = \
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
            json.dump(conf_dict,fl)
            
def LoadServerInfoToServer(name:str="Default",full_path=""):
    cfctl = ConfCtl(name=name,full_path=full_path)
    cfctl.Load_Config()
    server = SingleServerInfo\
    (
        xms = cfctl.xms,
        xmx = cfctl.xmx,
        use_java = cfctl.java,
        server_options = cfctl.jvm_options,
        server_file = cfctl.server,
        server_path = cfctl.server_path,
        descr = cfctl.description,
        name = cfctl.name
    )
    return server

def SaveServerInfoToConf(serverclass:Any,name:str="Default",full_path:str=""): # type: ignore
    cfctl = ConfCtl(name=name,full_path=full_path)
    cfctl.xms = serverclass.xms
    cfctl.xmx = serverclass.xmx
    cfctl.java = serverclass.use_java
    cfctl.jvm_options = serverclass.server_options
    cfctl.server = serverclass.server_file
    cfctl.server_path = serverclass.server_path
    cfctl.description = serverclass.descr
    cfctl.name = serverclass.name
    cfctl.Save_Config()