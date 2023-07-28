import flet
from flet import *
from .Navbar import nav_side as navbar

def init_page(page):
    page.title = "MSLX | 日志"
    page.window_width = 800
    page.window_height = 600
    page.fonts = {
    "SHS_TC": "fonts/SourceHanSansTC-Regular.otf",
    "SHS_SC": "fonts/SourceHanSansSC-Regular.otf"
}
    page.theme = Theme(font_family="SHS_SC")
    page.update()
    
def create_controls(page):
    text_server_logs = Text(value="Minecraft Server Logs Here...",italic=True,width=600,height=400)
    txt_command = TextField(label="在此键入向服务器发送的命令",on_submit=submit)
    page.add(Row(controls=[navbar,Column(controls=[text_server_logs,txt_command])]))
    page.update()
    
def submit(e):
    pass    
