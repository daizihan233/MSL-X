import os
import math
import time
import webbrowser as wb
import subprocess as sp
import pyperclip as clip
from typing import TYPE_CHECKING

from loguru import logger
from flet import \
(
    app,
    Row,
    Text,
    Theme,
    Column,
    Slider,
    Switch,
    dropdown,
    Dropdown,
    TextField,
    TextButton,
    FilePicker,
    FilePickerFileType,
    FilePickerResultEvent,
    KeyboardEvent,
    AlertDialog,
    ElevatedButton,
    MainAxisAlignment,
)

import PluginEntry

import ui.logs as logs
import ui.frpconfig as FrpConfig
import ui.settings as Settings
import ui.confcl as CreateConf
import ui.nginxconf as NginxConfUI
from ui.Navbar import nav_side as navbar

from lib.nginxconfig import NgConf
from lib.info_classes import ProgramInfo
from lib.confctl import ConfCtl,LoadServerInfoToServer, SaveServerInfoToConf

if TYPE_CHECKING:
    from flet import Page

@logger.catch
def main(page: 'Page'):

    PluginEntry.before_run("main", page)
    if os.path.exists("Config/Default.json") == False: # 如果默认配置不存在就保存默认配置
        conf = ConfCtl("Default")
        conf.Save_Config()
    else:
        current_server = LoadServerInfoToServer()
    programinfo = ProgramInfo()
    hitokoto = programinfo.hitokoto
    text = hitokoto["hitokoto"][:-1]

    if not os.path.exists("Config"):
        os.mkdir("Config")
    if not os.path.exists("Logs"):
        os.mkdir("Logs")
    if not os.path.exists("Config/__init__.py"):
        with open('__init__.py', 'w') as f:
            f.write('')
            
    logger.add('Logs/{time:YYYY-MM-DD}.log', format='[ {time:HH:mm:ss} ][ {level} ] {message} ', encoding='utf-8', backtrace=True, diagnose=True, compression="tar.gz" )

    def init_page():

        nonlocal current_server,programinfo
        page.title = f"MSLX | 主页"
        page.window_height = 600
        page.window_width = 1350
        page.fonts = \
        {
            "SHS_TC": "fonts/SourceHanSansTC-Regular.otf",
            "SHS_SC": "fonts/SourceHanSansSC-Regular.otf"
        }
        page.theme = Theme(font_family="SHS_SC")
        page.on_keyboard_event = on_keyboard
        programinfo.update_hitokoto()
        page.update()

    def start_server(e):
        nonlocal programinfo
        current_server.start()
        programinfo.running_server_list.append(current_server)

    def create_controls():  # 设置控件

        navbar.on_change = change_navbar

        # 开启服务器摁钮
        btn_start_server = ElevatedButton(
            "开启服务器", width=700, on_click=start_server
        )
        page.add(Row(
            controls=[btn_start_server],
            alignment=MainAxisAlignment.SPACE_EVENLY
        ))

        # Java与服务端路径
        global switch_srv_opti_read_only
        switch_srv_opti_read_only = Switch(
            label="只读", on_change=change_srv_opti_read_only
        )

        global txt_server_option
        server_option_str = ""
        for index in current_server.server_options:
            server_option_str += f"{index} "
        txt_server_option = TextField\
        (
            label="服务器启动参数",
            width=300,
            value=server_option_str,
            read_only=True
        )

        global dd_choose_java
        dd_choose_java = Dropdown(
            label="Java选择",
            width=150,
            options=\
            [
                dropdown.Option("Path"),
                dropdown.Option("Choose Java File"),
            ],
            on_change=change_java
        )
        global txt_server_name
        btn_show_java_path = ElevatedButton(
            "显示Java路径", on_click=show_java_path
        )
        btn_select_server_path = ElevatedButton(
            "选取服务端路径", on_click=select_server_path
        )
        txt_server_name = TextField(
            label="服务端名称(不需要.jar后缀),默认为server", width=300
        )

        global xms, sli_xms, sli_xmx
        sli_xms = Slider(
            label="最小内存(G)", width=500,
            divisions=current_server.xmx-1, min=1, max=current_server.xmx, on_change=change_xms
        )
        sli_xmx = Slider(
            label="最大内存(G)", width=500, 
            divisions=current_server.xmx - current_server.xms, min=1, max=current_server.xmx, on_change=change_xmx
        )

        global xmx, text_xms, text_xmx
        text_xms = Text(f"最小内存:{current_server.xms}G")
        text_xmx = Text(f"最大内存:{current_server.xmx}G")

        nonlocal text
        btn_hitokoto = TextButton(text, on_click=open_hitokoto)

        ui_main = Row(controls=[
            navbar,
            Column(controls=[
                Row(
                    controls=[
                        switch_srv_opti_read_only,
                        txt_server_option,
                        txt_server_name,
                        btn_select_server_path,
                        dd_choose_java,
                        btn_show_java_path
                    ],
                    alignment=MainAxisAlignment.END
                ),
                Column(controls=[
                    Row(controls=[
                        text_xms,
                        text_xmx
                    ]),
                    Row(controls=[
                        sli_xms,
                        sli_xmx
                    ])
                ]),
                btn_hitokoto
            ])
        ])
        page.add(ui_main)
        page.update()

    def change_java(e):
        nonlocal current_server

        def get_result(e: 'FilePickerResultEvent'):
            if e.files is None:
                raise
            file_result = e.files[0].path
            if file_result:
                nonlocal use_java
                use_java = file_result
            else:
                alert_warn_not_chosed_java = AlertDialog\
                (
                    title=Text("选择Java失败,请重新选择"), 
                    modal=True, 
                    open=True
                )
                page.add(alert_warn_not_chosed_java)
                page.update()
                time.sleep(3)
                alert_warn_not_chosed_java.open = False
                page.update()

        java_option = dd_choose_java.value
        if java_option == 'Path':
            use_java = 'java'
        else:
            picker = FilePicker(on_result=get_result)
            page.overlay.append(picker)
            page.update()
            picker.pick_files(dialog_title="选择Java路径")

    def show_java_path(e):
        alert_show_java_path = AlertDialog\
        (
            title=Text(f"Java路径(若为java则使用环境变量):{current_server.use_java}"), 
            modal=True, 
            open=True
        )
        page.add(alert_show_java_path)
        page.update()
        time.sleep(3)
        alert_show_java_path.open = False
        page.update()

    def select_server_path(e):
        nonlocal current_server
        AlertDialog\
        (
            title=Text("请勿选择桌面或者根目录!由此带来的任何后果请自行承担责任!"),
            modal=True, 
            open=True
        )

        def get_result(e: 'FilePickerResultEvent'):
            file_result = e.path
            if file_result:
                nonlocal current_server
                current_server.server_path = file_result
            else:
                alert_warn_not_chosed_java = AlertDialog\
                (
                    title=Text("选择服务端路径失败,请重新选择"), 
                    modal=True, 
                    open=True
                )
                page.add(alert_warn_not_chosed_java)
                page.update()
                time.sleep(3)
                alert_warn_not_chosed_java.open = False
                page.update()

        picker = FilePicker(on_result=get_result)
        page.overlay.append(picker)
        page.update()
        picker.get_directory_path(dialog_title="选择服务端路径")

    def change_srv_opti_read_only(e):

        def unlock_srv_opti(e):

            def close(e):
                nonlocal warn_change_srv_opti
                warn_finish_change.open = False
                warn_change_srv_opti.open = False
                switch_srv_opti_read_only.label = "锁定"
                txt_server_option.read_only = False
                page.update()

            warn_change_srv_opti.open = False
            warn_finish_change = AlertDialog(
                modal=False,
                title=Text("更改服务端启动选项"),
                content=Text("服务端启动选项已经解锁,请务必小心!"),
                actions=\
                [
                    TextButton("确认", on_click=close),
                ],
                open=True
            )
            page.add(warn_finish_change)
            page.update()

        if switch_srv_opti_read_only.value:

            def close(e):
                warn_change_srv_opti.open = False
                switch_srv_opti_read_only.value = False
                switch_srv_opti_read_only.label = "锁定"
                txt_server_option.read_only = True
                page.update()

            warn_change_srv_opti = AlertDialog(
                title=Text("更改服务端启动选项"),
                content=Text(
                    "如果您知道自己正在做什么,并且自行承担此操作带来的所有责任,请点击'继续更改';否则,请点击'取消'"
                ),
                actions=[
                    TextButton("继续更改", on_click=unlock_srv_opti),
                    TextButton("取消", on_click=close),
                ],
                modal=False,
                open=True,
            )
            page.add(warn_change_srv_opti)
            page.update()

        if switch_srv_opti_read_only.value == False:

            def close(e):
                warn_finish_change.open = False
                switch_srv_opti_read_only.value = False
                switch_srv_opti_read_only.label = "解锁"
                txt_server_option.read_only = True
                page.update()

            warn_finish_change = AlertDialog(
                modal=False,
                title=Text("更改服务端启动选项"),
                content=Text("服务端启动选项已经锁定"),
                actions=\
                [
                    TextButton("确认", on_click=close),
                ],
                open=True
            )
            page.add(warn_finish_change)
            page.update()

    def change_xms(e):
        nonlocal current_server
        assert sli_xms.value is not None
        current_server.xms = math.floor(sli_xms.value)
        text_xms.value = f"最小内存:{current_server.xms}G"
        page.update()

    def change_xmx(e):
        nonlocal current_server
        assert sli_xmx.value is not None
        xmx = math.floor(sli_xmx.value)
        current_server.xmx = xmx
        text_xmx.value = f"最大内存:{xmx}G"
        page.update()

    def save_config(e):
        nonlocal current_server
        
        def get_result(e: FilePickerResultEvent):
            nonlocal current_server
            
            def close(e):
                warn_conf.open = False
                page.update()
            
            file_result = e.path
            if file_result:
                logger.debug(f"获取到的文件路径:{file_result}")
                if "json" not in file_result:
                    file_result += ".json"
                current_server = SaveServerInfoToConf(current_server,full_path=file_result)
                warn_conf = AlertDialog(
                    modal=False,
                    title=Text("保存配置文件成功"),
                    actions=[
                        TextButton("确认", on_click=close),
                    ],
                    open=True
                )
                page.add(warn_conf)
            else:
                warn_conf = AlertDialog(
                    modal=False,
                    title=Text("保存配置文件失败"),
                    actions=[
                        TextButton("确认", on_click=close),
                    ],
                    open=True
                )
                page.add(warn_conf)
        
        picker = FilePicker(on_result=get_result)
        page.overlay.append(picker)
        page.update()
        picker.save_file(dialog_title="保存配置文件",file_name="Default",initial_directory=os.path.abspath("Config"+os.sep),file_type=FilePickerFileType.CUSTOM,allowed_extensions=["json"])
        page.update()

    def load_config(e):
        global name
        nonlocal current_server
        def get_result(e: FilePickerResultEvent):
            
            def close(e):
                warn_conf.open = False
                page.update()
            
            file_result = e.files
            if file_result:
                file_name = file_result[0].name
                src_path = file_result[0].path
                logger.debug(f"获取到的文件名:{file_name}")
                logger.debug(f"获取到的文件路径:{src_path}")
                current_server = LoadServerInfoToServer(full_path=src_path)
                warn_conf = AlertDialog(
                    modal=False,
                    title=Text("加载配置文件成功"),
                    actions=[
                        TextButton("确认", on_click=close),
                    ],
                    open=True
                )
                page.add(warn_conf)
            else:
                warn_conf = AlertDialog(
                    modal=False,
                    title=Text("加载配置文件失败"),
                    actions=[
                        TextButton("确认", on_click=close),
                    ],
                    open=True
                )
                page.add(warn_conf)
                
        picker = FilePicker(on_result=get_result)
        page.overlay.append(picker)
        page.update()
        picker.pick_files(dialog_title="选择配置文件",initial_directory=os.path.abspath("Config"+os.sep),file_type=FilePickerFileType.CUSTOM,allowed_extensions=["json"])
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
            txt_pathto.value = wri.decode()
            warn_result = AlertDialog\
            (
                modal = False,
                title = Text("检测结果"),
                content = Text(f"Path:{wri}\nNginx -V Info:{ngv}"),
                actions=\
                [
                    TextButton("确定", on_click=close),
                    TextButton("复制", on_click=copy),
                ],
                open=True
            )
            page.add(warn_result)
            page.update()
            
        def detect_ng_winpath(e):
            
            nonlocal close
            close(e)
            
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
        global ngpath
        ngpath = txt_pathto.value

    def open_hitokoto(e):
        uuid = hitokoto["uuid"]
        wb.open(f"https://hitokoto.cn?uuid={uuid}")

    def on_keyboard(e: KeyboardEvent):
        key = e.key
        shift = e.shift
        ctrl = e.ctrl
        alt = e.alt
        meta = e.meta
        if key == "F5":
            page.update()
        if alt:
            if shift:
                match key:
                    case "N": # 打开Nginx配置页面
                        pass   
                    case "L": # 打开登陆界面
                        pass   
                    case "G": # 打开密钥创建界面 
                        pass
                    case "D": # 打开下载页面
                        pass
                    case "P": # 打开插件列表
                        pass
        
    def change_navbar(e):

        def clrpage():
            if page.controls is None:
                raise
            page.controls.clear()
            page.update()

        def mainpage():
            clrpage()
            init_page()
            create_controls()
            page.update()

        def logspage():
            clrpage()
            logs.init_page(page)
            logs.create_controls(page)
            page.update()

        def frpcpage():
            clrpage()
            FrpConfig.init_page(page)
            FrpConfig.create_controls(page)
            page.update()

        def opendoc():
            wb.open("https://mojavehao.github.io/MSL-X/#/")

        def showinfo():
            def close(e):
                about.open = False
                page.update()
            about = AlertDialog(
                title=Text("MSLX Beta 0.07"),
                actions=[TextButton("确认", on_click=close)],
                modal=True,
                open=True,
            )
            page.add(about)
            page.update()

        def settingspage():
            clrpage() 
            Settings.init_page(page)
            Settings.create_controls(page)
            page.update()

        def cconfigpage():
            clrpage()
            CreateConf.init_page(page)
            btn_save_config = ElevatedButton("保存服务器配置", on_click=save_config)
            btn_load_config = ElevatedButton("加载服务器配置", on_click=load_config)
            page.add(
                Row(controls=[navbar, Column(controls=[btn_save_config, btn_load_config])]))
            page.update()
            
        def ngconfpage():
            clrpage()
            NginxConfUI.init_page(page)
            global txt_pathto
            txt_pathto = TextField(label="Nginx路径",height=400,multiline=True)
            btn_confirm = ElevatedButton("确认",on_click=ident_path)
            btn_auto_detect = ElevatedButton("检测",on_click=detect_nginx)
            row_top = Row(controls=[btn_confirm,btn_auto_detect])
            page.add(Row(controls=[navbar,Column(controls=[txt_pathto,row_top])]))
            page.update()

        index = e.control.selected_index

        match index:
            case 0:
                mainpage()
            case 1:
                logspage()
            case 2:
                frpcpage()
            case 3:
                opendoc()
            case 4:
                showinfo()
            case 5:
                settingspage() 
            case 6:
                cconfigpage()               

    init_page()
    create_controls()
    page.update()
    logger.debug("页面完成初始化")

    PluginEntry.after_run("main", page)
    logger.debug("总入口点已调用")

app(target=main, assets_dir="assets", port=61500)
