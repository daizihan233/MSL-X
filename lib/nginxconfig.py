from pyhocon.tool import HOCONConverter
from pyhocon.config_tree import ConfigTree
import json

def hocon_read(conf_path):
    with open(conf_path, encoding="utf-8") as f:
        data = f.read()
        
    config_data = ConfigFactory.parse_string(data)
    config_data = json.loads(HOCONConverter.to_json(config_data))
    return config_data

def hocon_write(conf_path):
    data = ConfigTree(s) 
    with open(conf_path, "w", encoding="utf-8") as f:
        f.write(HOCONConverter.to_hocon(data))
