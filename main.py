import flet
from flet import *
import subprocess as sp
import os
import webbrowser as web

def main(page:Page):
    
    use_java = 'java'#保存Java路径，为'JAVA'时使用环境变量(默认)
    xms = 1#G省略
    xmx = 4
    server_path = ''
    server_file = 'server.jar'
    server_options = '-XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=100 -XX:+DisableExplicitGC -XX:TargetSurvivorRatio=90 -XX:G1NewSizePercent=50 -XX:G1MaxNewSizePercent=80 -XX:G1MixedGCLiveThresholdPercent=35 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -Dusing.aikars.flags=mcflags.emc.gs'
    srv_opti_read_only = 1
    
    def init_page():
        
        page.title = "MSL X  Preview with Flutter(Flet)"
        page.window_height = 600
        page.window_width = 1300
        
    def start_server(e):
        if txt_server_name.value:
            server_file = txt_server_name.value + ".jar"
        else:
            server_file = 'server.jar'
        server = server_path + os.sep + server_file
        print(f"{use_java} -Xms{xms}G -Xmx{xmx}G {server_options} -jar {server}")
        sp.run(f"{use_java} -Xms{xms}G -Xmx{xmx}G {server_options} -jar {server}",check=True,shell=True,cwd=server_path)
        
    def create_controls():#设置控件
        
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
        row_ui_java = Row([switch_srv_opti_read_only,txt_server_option,txt_server_name,btn_select_server_path,dd_choose_java,btn_show_java_path],alignment = MainAxisAlignment.END)
        page.add(row_ui_java)
        
        #侧边五个摁钮
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
        page.add(column_ui_left)
        
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
                sleep(3)
                alert_warn_not_chosed_java.open = False
                page.update()
        
        picker = FilePicker(on_result=get_result)
        page.overlay.append(picker)
        page.update()
        picker.get_directory_path(dialog_title="选择服务端路径")
        
    def open_log(e):
        web.open(f"{server_path}/logs/latest.log")
        
    def about(e):
        about = AlertDialog(
        title=Text("MSLX Beta 0.02 with Flet(Flutter)\nMade by MojaveHao with ❤️\n特别鸣谢:\n\t-Frp节点提供:终末、谎言"), modal=True ,open=True)
        page.add(about)
        page.update()
        sleep(3)
        about.open = False
        page.update()
        
    def msl_help(e):
        web.open("https://mojavehao.github.io/MSL-X/#/")
        
    def change_srv_opti_read_only(e):

        nonlocal srv_opti_read_only
        
        def unlock_srv_opti(e):
            nonlocal srv_opti_read_only
            
            def close(e):
                nonlocal warn_change_srv_opti
                warn_finish_change.open = False
                warn_change_srv_opti.open = False
                switch_srv_opti_read_only.label = "锁定"
                txt_server_option.read_only = False
                page.update()
            
            srv_opti_read_only = 0
            
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
        
        if srv_opti_read_only == 1:

            def close(e):
                warn_change_srv_opti.open=False
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
            
        if srv_opti_read_only == 0:
            srv_opti_read_only = 1
            def close(e):
                warn_finish_change.open=False
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
            
    def open_frpc(e):
        sp.run(['python','frpconfig.py'])
            
    init_page()
    create_controls()
    page.update()
    
flet.app(target=main)