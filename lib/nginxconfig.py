from typing import Dict

from .log import logger


class NgConf:
    def __init__(self, conf_path: str):
        self.conf_path = conf_path
        self.conf_data: Dict[str, Dict[str, str]] = {}

    def loadConf(self) -> None:
        try:
            with open(self.conf_path, 'r') as conf_file:
                lines = conf_file.readlines()
                current_block = None

                for line in lines:
                    line = line.strip()
                    if line.startswith('#'):
                        continue
                    if line.endswith('{'):
                        current_block = line[:-1].strip()
                        self.conf_data[current_block] = {}
                    elif line == '}':
                        current_block = None
                    else:
                        if current_block:
                            key_value = line.split(maxsplit=1)
                            if len(key_value) == 2:
                                key, value = key_value
                                self.conf_data[current_block][key] = value

        except FileNotFoundError:
            logger.critical(f"未能找到指定的配置文件:{self.conf_path}")

    def writeConf(self) -> None:
        try:
            with open(self.conf_path, 'w') as conf_file:
                for block, directives in self.conf_data.items():
                    conf_file.write(f"{block} {{\n")
                    for key, value in directives.items():
                        conf_file.write(f"    {key} {value};\n")
                    conf_file.write("}\n")
            print(f"已向{self.conf_path}写入数据")
        except Exception as e:
            print(f"向{self.conf_path}进行数据写入失败:{e}")


'''
# 使用示例
conf_path = "nginx.conf"  # 替换为您的Nginx配置文件路径
ng_conf = NgConf(conf_path)
ng_conf.loadConf()

# 假设现在有一个名为 'http' 的配置块，你可以这样修改它：
ng_conf.conf_data['http']['server_tokens'] = 'off'

# 将修改后的配置写入文件
ng_conf.writeConf()

'''
