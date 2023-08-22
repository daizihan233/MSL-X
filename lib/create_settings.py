import json
import sys
sys.path.append("..") 
from Config import *


def create_conf(name, server_name, server_path, java_path, describe):
    dict_setting = {
        "name": name,
        "server": server_name,
        "path": server_path,
        "java": java_path,
        "describe": describe
    }
    with open(f'Config/{name}.json', 'w') as f:
        set_json = json.dump(dict_setting, f)


def conf_load(name):
    with open(f'Config/{name}.json', 'r') as f:
        dict_conf = json.load(f)
        print(f"load:{dict_conf}")
    return dict_conf
