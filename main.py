from flet import *

import os
import psutil
import math
import requests
import json
import time
import subprocess as sp
import webbrowser as web
from loguru import logger


from lib.create_settings import *
from lib.nginxconfig import *
from lib.confctl import ConfCtl

import ui.logs as logs
import ui.frpconfig as FrpConfig
import ui.settings as Settings
import ui.confcl as CreateConf
from ui.Navbar import nav_side as navbar

import PluginEntry

@logger.catch
def main(page: Page):

    PluginEntry.before_run("main", page)
    use_java = 'java'  # 保存Java路径，为'JAVA'时使用环境变量(默认)
    xms = 1  # G省略
    xmx = 4
    server_path = ''
    server_file = 'server.jar'
    server_options = '-XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=100 -XX:+DisableExplicitGC -XX:TargetSurvivorRatio=90 -XX:G1NewSizePercent=50 -XX:G1MaxNewSizePercent=80 -XX:G1MixedGCLiveThresholdPercent=35 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -Dusing.aikars.flags=mcflags.emc.gs'
    vsmem = psutil.virtual_memory()
    xmx = math.floor((vsmem.total - vsmem.used)/1000000000*0.7)
    name = "Default"
    hitokoto_html = requests.get(
        url="https://v1.hitokoto.cn/?c=i&encode=json&charset=utf-8")
    hitokoto = json.loads(hitokoto_html.text)

    if not os.path.exists("Config"):
        os.mkdir("Config")
    if not os.path.exists("Logs"):
        os.mkdir("Logs")
    if not os.path.exists("Config/__init__.py"):
        with open('__init__.py', 'w') as f:
            f.write('')
    logger.add('Logs/{time:YYYY-MM-DD}.log', format='[ {time:HH:mm:ss} ][ {level} ] {message} ', encoding='utf-8', backtrace=True, diagnose=True, compression="tar.gz" )

    def init_page():

        nonlocal hitokoto,name,server_file,server_options,server_path,xms,xmx,use_java
        text = hitokoto["hitokoto"][:-1]
        page.title = f"MSLX | 主页"
        page.window_height = 600
        page.window_width = 1350
        page.fonts = {
            "SHS_TC": "fonts/SourceHanSansTC-Regular.otf",
            "SHS_SC": "fonts/SourceHanSansSC-Regular.otf"
        }
        page.theme = Theme(font_family="SHS_SC")
        
        if os.path.exists("Config/Default.json"): # 加载默认配置
            with open("Config/Default.json") as f:
                conf = ConfCtl("Default")
                conf.Load_Config()
                server_path = conf.server_path
                server_file = conf.server
                use_java = conf.java                
                xms = conf.xms
                xmx = conf.xmx
                name = conf.name
                for option in conf.jvm_options:
                    server_options += f"{option} "
                page.title += f" | {name}"
                    
        else: # 如果默认配置不存在就保存默认配置
            conf = ConfCtl()
            conf.server_path = server_path
            conf.server = server_file
            conf.java = use_java
            conf.xms = xms
            conf.xmx = xmx
            conf.name = "Default"
            conf.jvm_options = server_options.split(' ')
            conf.Save_Config()

    def start_server(e):
        if xms > xmx:
            warn_ram = AlertDialog(
                title=Text("警告"),
                content=Text("最小内存不能大于最大内存"),
                open=True, modal=True)
            page.add(warn_ram)
            page.update()
            time.sleep(1.5)
            warn_ram.open = False
            page.update()
            return
        if txt_server_name.value:
            server_file = txt_server_name.value + ".jar"
        else:
            server_file = 'server.jar'
        server = server_path + os.sep + server_file
        sp.run(f"{use_java} -Xms{xms}G -Xmx{xmx}G {server_options} -jar {server}",
               check=True, shell=True, cwd=server_path)

    def create_controls():  # 设置控件

        navbar.on_change = change_navbar

        # 开启服务器摁钮
        btn_start_server = ElevatedButton(
            "开启服务器", width=700, on_click=start_server)
        row_ui_top = Row(controls=[btn_start_server],
                         alignment=MainAxisAlignment.SPACE_EVENLY)
        page.add(row_ui_top)

        # Java与服务端路径
        global switch_srv_opti_read_only
        switch_srv_opti_read_only = Switch(
            label="只读", on_change=change_srv_opti_read_only)

        global txt_server_option
        txt_server_option = TextField(
            label="服务器启动参数",
            width=300,
            value=server_options,
            read_only=True
        )

        global dd_choose_java
        dd_choose_java = Dropdown(
            label="Java选择",
            width=150,
            options=[
                dropdown.Option("Path"),
                dropdown.Option("Choose Java File"),
            ],
            on_change=change_java
        )
        global txt_server_name
        btn_show_java_path = ElevatedButton(
            "显示Java路径", on_click=show_java_path)
        btn_select_server_path = ElevatedButton(
            "选取服务端路径", on_click=select_server_path)
        txt_server_name = TextField(
            label="服务端名称(不需要.jar后缀),默认为server", width=300)

        global sli_xms
        global sli_xmx
        sli_xms = Slider(label="最小内存(G)", width=500,
                         divisions=xmx-1, min=1, max=xmx, on_change=change_xms)
        sli_xmx = Slider(label="最大内存(G)", width=500, divisions=xmx -
                         xms, min=1, max=xmx, on_change=change_xmx)

        global text_xms
        global text_xmx
        text_xms = Text(f"最小内存:{xms}G")
        text_xmx = Text(f"最大内存:{xmx}G")

        nonlocal hitokoto
        btn_hitokoto = TextButton(hitokoto["hitokoto"], on_click=open_hitokoto)

        ui_main = Row(
            controls=[navbar, Column(
                controls=[
                    Row(controls=[switch_srv_opti_read_only,
                                  txt_server_option,
                                  txt_server_name,
                                  btn_select_server_path,
                                  dd_choose_java,
                                  btn_show_java_path],
                        alignment=MainAxisAlignment.END),
                    Column(controls=[
                        Row(controls=[
                            text_xms,
                            text_xmx]),
                        Row(controls=[
                            sli_xms,
                            sli_xmx])
                    ]
                    ), btn_hitokoto])])
        page.add(ui_main)
        page.update()

    def change_java(e):
        nonlocal use_java

        def get_result(e: FilePickerResultEvent):
            if e.files is None:
                raise
            file_result = e.files[0].path
            if file_result:
                nonlocal use_java
                use_java = file_result
            else:
                alert_warn_not_chosed_java = AlertDialog(
                    title=Text("选择Java失败,请重新选择"), modal=True, open=True)
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
        alert_show_java_path = AlertDialog(
            title=Text(f"Java路径(若为java则使用环境变量):{use_java}"), modal=True, open=True
        )
        page.add(alert_show_java_path)
        page.update()
        time.sleep(3)
        alert_show_java_path.open = False
        page.update()

    def select_server_path(e):
        nonlocal server_path
        AlertDialog(
            title=Text("请勿选择桌面或者根目录!由此带来的任何后果请自行承担责任!"), modal=True, open=True
        )

        def get_result(e: FilePickerResultEvent):
            file_result = e.path
            if file_result:
                nonlocal server_path
                server_path = file_result
            else:
                alert_warn_not_chosed_java = AlertDialog(
                    title=Text("选择服务端路径失败,请重新选择"), modal=True, open=True)
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

            warn_finish_change = AlertDialog(
                modal=False,
                title=Text("更改服务端启动选项"),
                content=Text("服务端启动选项已经解锁,请务必小心!"),
                actions=[
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
                modal=False,
                title=Text("更改服务端启动选项"),
                content=Text(
                    "如果您知道自己正在做什么,并且自行承担此操作带来的所有责任,请点击'继续更改';否则,请点击'取消'"),
                actions=[
                    TextButton("继续更改", on_click=unlock_srv_opti),
                    TextButton("取消", on_click=close),
                ],
                open=True
            )
            page.add(warn_change_srv_opti)
            page.update()

        if switch_srv_opti_read_only.value == False:

            def close(e):
                warn_finish_change.open = False
                switch_srv_opti_read_only.value = True
                switch_srv_opti_read_only.label = "解锁"
                txt_server_option.read_only = True
                page.update()

            warn_finish_change = AlertDialog(
                modal=False,
                title=Text("更改服务端启动选项"),
                content=Text("服务端启动选项已经锁定"),
                actions=[
                    TextButton("确认", on_click=close),
                ],
                open=True
            )
            page.add(warn_finish_change)
            page.update()

    def change_xms(e):
        nonlocal xms
        if sli_xms.value is None:
            raise
        xms = math.floor(sli_xms.value)
        text_xms.value = f"最小内存:{xms}G"
        page.update()

    def change_xmx(e):
        nonlocal xmx
        if sli_xmx.value is None:
            raise
        xmx = math.floor(sli_xmx.value)
        text_xmx.value = f"最大内存:{xmx}G"
        page.update()

    def save_config(e):
        nonlocal server_path, server_file, use_java, xms, xmx
        txt_conf_name = TextField(
            label="配置文件名称"
            )
        
        if txt_conf_name != "":
            conf = ConfCtl()
            conf.server_path = server_path
            conf.server = server_file
            conf.java = use_java
            conf.xms = xms
            conf.xmx = xmx
            conf.name = name
            conf.jvm_options = server_options.split(' ')
            conf.Save_Config()
            def close(e):
                warn_conf.open = False
                page.update()
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
            def close(e):
                warn_conf.open = False
                page.update()
            warn_conf = AlertDialog(
                modal=False,
                title=Text("请输入配置文件名称"),
                actions=[
                    TextButton("确认", on_click=close),
                ],
                open=True
            )
            page.add(warn_conf)
            
        page.update()

    def load_config(e):
        global name
        nonlocal server_path, server_file, use_java, xms, xmx
        def get_result(e: FilePickerResultEvent):
            file_result = e.path
            if file_result:
                file_result_array = file_result.split('/') # 切割路径,最后一项为文件名
                file_name_array = file_result_array[-1].split('.') # 切割后缀
                conf = ConfCtl(file_name_array[0]) # 传入文件名
                conf.Load_Config()
                
                server_path = conf.server_path
                server_file = conf.server
                use_java = conf.java                
                xms = conf.xms
                xmx = conf.xmx
                name = conf.name
                for option in conf.jvm_options:
                    server_options += f"{option} "
                    
                def close(e):
                    warn_conf.open = False
                    page.update()
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
                def close(e):
                    warn_conf.open = False
                    page.update()
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
        picker.get_directory_path(dialog_title="选择服务端路径")
        page.update()

    def open_hitokoto(e):
        uuid = hitokoto["uuid"]
        web.open(f"https://hitokoto.cn?uuid={uuid}")

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
            web.open("https://mojavehao.github.io/MSL-X/#/")

        def showinfo():
            def close(e):
                about.open = False
                page.update()
            about = AlertDialog(title=Text("MSLX Beta 0.07"), modal=True, open=True, actions=[
                                TextButton("确认", on_click=close),],)
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
