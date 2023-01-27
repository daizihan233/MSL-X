import flet
from flet import *
import subprocess as sp
import random
import requests
import platform

sys.path.append('..')
from lib.download import download

def frpconfig(page:Page):
    
    node = ''
    port = 25565
    user = ''
    protocol = "tcp"
    remote_port = random.randint(20000,60000)
    page.fonts = {
        "SHS_TC": "fonts/SourceHanSansTC-Regular.otf",
        "SHS_SC": "fonts/SourceHanSansSC-Regular.otf"
    }
    page.theme = Theme(font_family="SHS_SC")
    
    def init_page():
        page.title = "Frpc设置"
        page.window_width = 700
        page.window_height = 400
        page.update()
        
    def create_controls():
        dd_node = Dropdown(
            label = "节点选择",
            options=[
            dropdown.Option("上海1"),
            dropdown.Option("香港"),
            dropdown.Option("北京[付费]"),
            dropdown.Option("广州[付费]"),
            dropdown.Option("上海2[付费]"),
            ],
            width=500
        )
        txt_port = TextField(
        label="服务器端口",
        value=25565
        )
        txt_user = TextField(
        label="在此输入您的QQ号(请勿乱输)",
        width=160
        )
        dd_protocol = Dropdown(
        label = "协议选择",
        width = 170,
        options = [
            dropdown.Option("TCP(Java)"),
            dropdown.Option("UDP(Bedrock)"),
            dropdown.Option("TCP+UDP(互通服用)"),
            dropdown.Option("KCP(仅付费节点可用)"),
            dropdown.Option("QUIC(仅付费节点可用)")
        ]
        )
        btn_start_frpc = ElevatedButton("启动映射",on_click=start_frpc)
        btn_download_frpc = ElevatedButton("下载最新版frpc",on_click=download_frpc)
        ctrls_bottom = Row(controls=[btn_start_frpc,btn_download_frpc])
        
        page.add(
            dd_node,
            txt_port,
            txt_user,
            dd_protocol,
            ctrls_bottom
        )
        page.update()
        
    def start_frpc(e):
        
        node_list = ["sh1","hk","bj","gz","sh2"]
        if dd_node.value == "上海1":
            node = node_list[0]
        if dd_node.value == "香港":
            node = node_list[1]
        if dd_node.value == "北京[付费]":
            node = node_list[2]
        if dd_node.value == "广州[付费]":
            node = node_list[3]
        if dd_node.value == "上海2[付费]":
            node = node_list[4]
            
        protocol_list = ["tcp","udp","tcp+udp","kcp","quic"]
        
        frpc_config = f'\
        [common]\n\
        server_port=7000\n\
        server_addr={node}.qwq.one \n\
        user={user}\n\
        meta_token=20021120\n\
        protocol={protocol}\n\
\
        {user}TCP\n\
        type=tcp\n\
        local_ip=127.0.0.1\n\
        local_port={port}\n\
        remote_port={remote_port}\n\
\
        {user}UDP\n\
        type=udp\n\
        local_ip=127.0.0.1\n\
        local_port={port}\n\
        remote_port={remote_port}\n\
'

    def download_frpc(e):
        
        sys_type = platform.system()
        
        url = 'https://api.github.com/repos/fatedier/frp/releases/latest'
        response_data = requests.get(url)
        response_dict = response_data.json()
        assets_list = response_dict["assets"]
        resource_list = []
        
        for items in assets_list:
            name = items["name"]
            browser_download_url = items["browser_download_url"]
            tmp_dict = {"name":name,"url":browser_download_url}
            resource_list.append(tmp_dict)
        
        for current_dict in resource_list:
                if sys_type.lower() in current_dict["name"] and "amd64" in current_dict["name"]:
                    download_url = current_dict["url"]
                    download_name = current_dict["name"]
                    
        print(f"Donwload file name:{download_name}\nDownload file URL:{download_url}")
        download(down_url=download_url, down_name=download_name)
    
    init_page()
    create_controls()
    page.update()
