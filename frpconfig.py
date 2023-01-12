import flet
from flet import *
import subprocess as sp
import random
def frpconfig(page:Page):
    
    node = ''
    port = 25565
    user = ''
    protocol = "tcp"
    remote_port = random.randint(20000,60000)
    
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
            dropdown.Option("广州腾讯云[不支持SRV]"),
            dropdown.Option("香港"),
            dropdown.Option("北京[付费]"),
            dropdown.Option("广州[付费]"),
            dropdown.Option("上海2[付费]"),
            dropdown.Option("宿迁[应急]"),
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
        ]
        )
        btn_start_frpc = ElevatedButton("启动映射",on_click=start_frpc)
        page.add(
            dd_node,
            txt_port,
            txt_user,
            dd_protocol,
            btn_start_frpc
        )
        page.update()
        
    def start_frpc(e):
        pass

    init_page()
    create_controls()
    page.update()

flet.app(target=frpconfig,port=10242)