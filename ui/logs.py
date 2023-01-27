import flet
from flet import *
def logs(page:Page):
    
    def init_page():
        page.title = "日志"
        page.window_width = 800
        page.window_height = 500
        page.fonts = {
        "SHS_TC": "fonts/SourceHanSansTC-Regular.otf",
        "SHS_SC": "fonts/SourceHanSansSC-Regular.otf"
    }
        page.theme = Theme(font_family="SHS_SC")
        page.update()
        
    def create_controls():
        text_server_logs = Text(value="",italic=True,width=600,height=400)
        page.add(txt_server_logs)
        
        txt_command = TextField(value="在此键入向服务器发送的命令")
        
        
        page.update()
        
    init_page()
    create_controls()
    page.update()
        
flet.app(target=logs,assets_dir="../assets",)