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
    
    def init_page():
        
        page.title = "MSL X  Preview with Flutter(Flet)"
        page.window_height = 600
        page.window_width = 1100
        
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
        global dd_choose_java
        dd_choose_java = Dropdown(
        label = "Java选择",
        width = 100,
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
        row_ui_java = Row([txt_server_name,btn_select_server_path,dd_choose_java,btn_show_java_path],alignment = MainAxisAlignment.END)
        page.add(row_ui_java)
        
        #侧边五个摁钮
        btn_log = ElevatedButton("日志",on_click=open_log)
        btn_frp = ElevatedButton("映射")
        btn_about = ElevatedButton("关于",on_click=about)
        btn_help = ElevatedButton("帮助")
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
        AlertDialog(
        title=Text("MSLX Beta 0.01 with Flet(Flutter)\nMade by MojaveHao with ❤️"), modal=True ,open=True)
        
    def help(e):
        web.open("https://mojavehao.github.io/MSL-X/#/")
         
    init_page()
    create_controls()
    page.update()
    
flet.app(target=main)