import flet
from flet import *

import subprocess as sp
import os
import webbrowser as web
import psutil
import math
import random
import requests
import json
import time

from lib.create_settings import *
from lib.nginxconfig import *

import ui.logs as logs
import ui.frpconfig as FrpConfig
import ui.nginxconf as NgConfUI
import ui.settings as Settings
import ui.confcl as CreateConf
from ui.Navbar import nav_side as navbar

import PluginEntry

def main(page:Page):
    
    PluginEntry.before_run("main",page)
    use_java = 'java'#保存Java路径，为'JAVA'时使用环境变量(默认)
    xms = 1#G省略
    xmx = 4
    server_path = ''
    server_file = 'server.jar'
    server_options = '-XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=100 -XX:+DisableExplicitGC -XX:TargetSurvivorRatio=90 -XX:G1NewSizePercent=50 -XX:G1MaxNewSizePercent=80 -XX:G1MixedGCLiveThresholdPercent=35 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -Dusing.aikars.flags=mcflags.emc.gs'
    vsmem = psutil.virtual_memory()
    xmx = math.floor((vsmem.total - vsmem.used)/1000000000*0.7)
    hitokoto_html = requests.get(url="https://v1.hitokoto.cn/?c=i&encode=json&charset=utf-8")
    hitokoto = json.loads(hitokoto_html.text)

    if not os.path.exists("Config"):
        os.mkdir("Config")
        with open('__init__.py','w') as f:
            f.write()   
    
    def init_page():
        
        nonlocal hitokoto
        text = hitokoto["hitokoto"][:-1]
        page.title = f"MSLX | 主页"
        page.window_height = 600
        page.window_width = 1350
        page.fonts = {
        "SHS_TC": "fonts/SourceHanSansTC-Regular.otf",
        "SHS_SC": "fonts/SourceHanSansSC-Regular.otf"
    }
        page.theme = Theme(font_family="SHS_SC")
        
    def start_server(e):
        if xms > xmx:
            warn_ram = AlertDialog(
                title=Text("警告"),
                content=Text("最小内存不能大于最大内存"),
                open=True,modal=True)
            page.add(warn_ram)
            page.update()
            sleep(1.5)
            warn_ram.open = False
            page.update()
            return
        if txt_server_name.value:
            server_file = txt_server_name.value + ".jar"
        else:
            server_file = 'server.jar'
        if server_path:
            server = server_path + os.sep + server_file
        sp.run(f"{use_java} -Xms{xms}G -Xmx{xmx}G {server_options} -jar {server}",check=True,shell=True,cwd=server_path)
        
    def create_controls():#设置控件
        
        navbar.on_change = change_navbar
        
        #开启服务器摁钮
        btn_start_server = ElevatedButton("开启服务器",width = 700,on_click=start_server)
        row_ui_top = Row(controls=[btn_start_server],alignment = MainAxisAlignment.SPACE_EVENLY)
        page.add(row_ui_top)
        
        #Java与服务端路径
        global switch_srv_opti_read_only
        switch_srv_opti_read_only = Switch(label="只读", on_change=change_srv_opti_read_only)
        
        global txt_server_option
        txt_server_option = TextField(
        label="服务器启动参数",
        width=300,
        value=server_options,
        read_only=True
        )
        
        global dd_choose_java
        dd_choose_java = Dropdown(
        label = "Java选择",
        width = 150,
        options = [
            dropdown.Option("Path"),
            dropdown.Option("Choose Java File"),
        ],
        on_change=change_java
    )
        global txt_server_name
        btn_show_java_path = ElevatedButton("显示Java路径",on_click=show_java_path)
        btn_select_server_path = ElevatedButton("选取服务端路径",on_click=select_server_path)
        txt_server_name = TextField(label="服务端名称(不需要.jar后缀),默认为server",width=300,height=50)
        
        global sli_xms
        global sli_xmx
        sli_xms = Slider(label="最小内存(G)",width=500,divisions=xmx-1,min=1,max=xmx,on_change=change_xms)
        sli_xmx = Slider(label="最大内存(G)",width=500,divisions=xmx-xms,min=1,max=xmx,on_change=change_xmx)
        
        global text_xms
        global text_xmx
        text_xms = Text(f"最小内存:{xms}G")
        text_xmx = Text(f"最大内存:{xmx}G")
        
        nonlocal hitokoto
        btn_hitokoto = TextButton(hitokoto["hitokoto"],on_click=open_hitokoto)
        
        ui_main = Row(
            controls = [navbar,Column(    
                controls=[
                    Row(controls=
                        [switch_srv_opti_read_only,
                            txt_server_option,
                            txt_server_name,
                            btn_select_server_path,
                            dd_choose_java,
                            btn_show_java_path],
                        alignment = MainAxisAlignment.END),
                    Column(controls=[
                        Row(controls=[
                            text_xms,
                            text_xmx]),
                        Row(controls=[
                            sli_xms,
                            sli_xmx])
            ]
        ),btn_hitokoto])])
        page.add(ui_main)
        
        '''
        #侧边摁钮
        
        btn_log = ElevatedButton("日志",on_click=open_log)
        btn_frp = ElevatedButton("映射",on_click=open_frpc)
        btn_about = ElevatedButton("关于",on_click=about)
        btn_help = ElevatedButton("文档",on_click=msl_help)
        btn_setting = ElevatedButton("设置")
        column_ui_left = Column(controls=
       [btn_log,
        btn_frp,
        btn_about,
        btn_help,
        btn_setting])
        

        #底部摁钮
        btn_save_config = ElevatedButton("保存服务器配置",on_click=save_config)
        btn_load_config = ElevatedButton("加载服务器配置",on_click=load_config)
        row_bottom = Row(
            controls=[
                btn_save_config,
                btn_load_config
            ]
        )
        '''
        
        page.update()
        
    def change_java(e):
        
        nonlocal use_java
            
        def get_result(e:FilePickerResultEvent):
            file_result = e.files[0].path
            if file_result:
                nonlocal use_java
                use_java = file_result
            else:
                alert_warn_not_chosed_java = AlertDialog(
                title=Text("选择Java失败,请重新选择"), modal=True ,open=True)
                page.add(alert_warn_not_chosed_java)
                page.update()
                sleep(3)
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
            title=Text(f"Java路径(若为java则使用环境变量):{use_java}"), modal=True ,open=True)
        page.add(alert_show_java_path)
        page.update()
        sleep(3)
        alert_show_java_path.open = False
        page.update()
        
    def select_server_path(e):
        nonlocal server_path
        AlertDialog(
        title=Text("请勿选择桌面或者根目录!由此带来的任何后果请自行承担责任!"), modal=True ,open=True)
        
        def get_result(e:FilePickerResultEvent):
            file_result = e.path
            if file_result:
                nonlocal server_path
                server_path = file_result
            else:
                alert_warn_not_chosed_java = AlertDialog(
                title=Text("选择服务端路径失败,请重新选择"), modal=True ,open=True)
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
            modal = False,
            title = Text("更改服务端启动选项"),
            content = Text("服务端启动选项已经解锁,请务必小心!"),
            actions=[
                TextButton("确认", on_click=close),
            ],
            open=True
        )
            page.add(warn_finish_change)
            page.update()
        
        if switch_srv_opti_read_only.value == 1:

            def close(e):
                warn_change_srv_opti.open=False
                switch_srv_opti_read_only.value = 0
                switch_srv_opti_read_only.label = "锁定"
                txt_server_option.read_only = True
                page.update()
                
            warn_change_srv_opti = AlertDialog(
            modal = False,
            title = Text("更改服务端启动选项"),
            content = Text("如果您知道自己正在做什么,并且自行承担此操作带来的所有责任,请点击'继续更改';否则,请点击'取消'"),
            actions = [
                TextButton("继续更改", on_click=unlock_srv_opti),
                TextButton("取消", on_click=close),
            ],
            open=True
        )
            page.add(warn_change_srv_opti)
            page.update()
            
        if switch_srv_opti_read_only.value == 0:
            
            def close(e):
                warn_finish_change.open=False
                switch_srv_opti_read_only.value = 1
                switch_srv_opti_read_only.label = "解锁"
                txt_server_option.read_only = True
                page.update()
            
            warn_finish_change = AlertDialog(
            modal = False,
            title = Text("更改服务端启动选项"),
            content = Text("服务端启动选项已经锁定"),
            actions=[
                TextButton("确认", on_click=close),
            ],
            open=True
        )
            page.add(warn_finish_change)
            page.update()
        
    def change_xms(e):
        nonlocal xms
        xms = math.floor(sli_xms.value)
        text_xms.value = f"最小内存:{xms}G"
        page.update()
        
    def change_xmx(e):
        nonlocal xmx
        xmx = math.floor(sli_xmx.value)
        text_xmx.value = f"最大内存:{xmx}G"
        page.update()
        
    def save_config(e):
        nonlocal server_file, server_path, use_java
        
        def save_conf(e):
            nonlocal server_file, server_path, use_java, txt_config_name, txt_config_describe
            
            def close(e):
                warn_save_successful.open = False
            
            name = txt_config_name.value
            describe = txt_config_describe.value
            create_conf(name, server_file, server_path, use_java, describe)
            page.update()
            
        def close(e):
            bs_save_conf.open = False
            page.update()
        
        text_title = Text("配置文件设置")
        txt_config_name = TextField(label="配置名称(不要含有中文和特殊符号)",value="Default")
        txt_config_describe = TextField(label="配置注释")
        column_save_opti = Column(
            controls=[
                text_title,
                txt_config_name,
                txt_config_describe,
                Row(
                    controls=[
                        TextButton("确认保存", on_click=save_conf),
                        TextButton("取消", on_click=close)
                    ]
                )
                
            ]
        )
        bs_save_conf = BottomSheet(
            content = column_save_opti,
            open = True
        )
        page.add(bs_save_conf)
        page.update()
    
    def load_config(e):
        global name
        nonlocal server_path,server_file,use_java
        dict_tmp_conf = {}
        
        def load_conf(e):
            
            def close(e):
                bs_load_conf_view.open = False
                
            def load(e):
                nonlocal server_path,server_file,use_java,dict_tmp_conf
                server_file = dict_tmp_conf["server"]
                server_path = dict_tmp_conf["path"]
                use_java = dict_tmp_conf["java"]
            
            nonlocal dict_tmp_conf,bs_load_conf_name
            dict_tmp_conf = conf_load(name)
            bs_load_conf_name.open=False
            text_info = Text(f"配置文件{name}.json信息:{dict_tmp_conf}")
            btn_load = TextButton("确认加载",on_click=load)
            btn_cannel = TextButton("取消",on_click=close)
            col_info = Column(
                controls=[
                    text_info,
                    btn_load,
                    btn_cannel
                ]
            )
            bs_load_conf_view = BottomSheet(
                content=text_info
            ) 
            page.add(bs_load_conf_view)
            page.update()
            
        txt_load_name = TextField(label="配置文件名称",value="Default")
        name = txt_load_name.value

        btn_load = TextButton("加载",on_click=load_conf)
        col_load_opti = Column(
            controls=[
                txt_load_name,
                btn_load
            ]
        )
        bs_load_conf_name = BottomSheet(
            content=col_load_opti,
            open=True
        )
        page.add(bs_load_conf_name)
        page.update()
        
    def open_hitokoto(e):
        uuid = hitokoto["uuid"]
        web.open(f"https://hitokoto.cn?uuid={uuid}")
        
    def change_navbar(e):
        
        def clrpage():
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
            about = AlertDialog(title=Text("MSLX Beta 0.07"), modal=True ,open=True, actions=[TextButton("确认", on_click=close),],)
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
            btn_save_config = ElevatedButton("保存服务器配置",on_click=save_config)
            btn_load_config = ElevatedButton("加载服务器配置",on_click=load_config)
            page.add(Row(controls=[navbar,Column(controls=[btn_save_config,btn_load_config])]))
            page.update()
        
        index = e.control.selected_index
        
        if index == 0:
            mainpage()
        
        elif index == 1:
            logspage()
        
        elif index == 2:
            frpcpage()
        
        elif index == 3:
            opendoc()
        
        elif index == 4:
            showinfo()
        
        elif index == 5:
            settingspage()
        
        else:
            cconfigpage()
            
    init_page()
    create_controls()
    page.update()
    
    PluginEntry.after_run("main",page)
    
flet.app(target=main,assets_dir="assets",port=61500)