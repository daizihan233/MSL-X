from flet import \
(
    Theme,
    TextField,
    ElevatedButton,
    Row,
    Column,
    AlertDialog,
    Text,
    TextButton,
    
)
from .Navbar import nav_side as navbar

import subprocess as sp
import pyperclip as clip
import sys,os
sys.path.append(os.getcwd())
from lib import nginxconfig as ngf
    
def init_page(page):
    page.title = "MSLX | Nginx配置"
    page.window_height = 600
    page.window_width = 910
    page.fonts = {
    "SHS_TC": "fonts/SourceHanSansTC-Regular.otf",
    "SHS_SC": "fonts/SourceHanSansSC-Regular.otf"
}
    page.theme = Theme(font_family="SHS_SC")
    page.update()
    
def create_controls(page):
    
    global txt_pathto
    txt_pathto = TextField(label="Nginx路径",height=400,multiline=True)
    
    btn_login = ElevatedButton("确认",on_click=ident_path)
    btn_auto_detect = ElevatedButton("检测",on_click=detect_nginx)
    row_top = Row(controls=[btn_login,btn_auto_detect])
    page.add(Row(controls=[navbar,Column(controls=[txt_pathto,row_top])]))
    page.update()
    
def detect_nginx(e):
    def close(e):
        warn_type_choose.open = False
        page.update()
        
    def detect_ng_linux(e):
        def close(e):
            warn_result.open = False
            warn_type_choose.open = False
            page.update()
            
        def copy(e):
            clip.copy(f"Path:{wri}\nNginx -V Info:{ngv}")
        
        wri = sp.run("whereis nginx",shell=True).stdout
        ngv = sp.run("nginx -V",shell=True).stdout    
        txt_pathto.content = wri
        warn_result = AlertDialog(
        modal = False,
        title = Text("检测结果"),
        content = Text(f"Path:{wri}\nNginx -V Info:{ngv}"),
        actions=[
            TextButton("确定", on_click=close),
            TextButton("复制", on_click=copy),
        ],
        open=True
    )
        page.add(warn_result)
        page.update()
        
    def detect_ng_winpath(e):
        
        nonlocal close
        close()
        
    warn_type_choose = AlertDialog(
        modal = False,
        title = Text("选择检测方法"),
        actions=[
            TextButton("自动检测Path(Linux)", on_click=detect_ng_linux),
            TextButton("调用EverythingSDK(Windows)", on_click=close),
            TextButton("检测Windows环境变量(不推荐)", on_click=detect_ng_winpath),
        ],
        open=True
    )
    page.add(warn_type_choose)
    page.update()   

def ident_path(e):
    ngpath = txt_pathto.value