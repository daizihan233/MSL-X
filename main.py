import flet
import subprocess as sp
from flet import *
def main(page:Page):
    
    use_java = 'java'#保存Java路径，为'JAVA'时使用环境变量(默认)
    xms = 1#G省略
    xmx = 4
    server_file = 'server.jar'
    
    def init_page():
        
        page.title = "MSL X  Preview with Flutter(Flet)"
        page.window_height = 600
        page.window_width = 1100
        
    def start_server(e):
        sp.run(f"{use_java} -Xms{xms}G -Xmx{xmx}G -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=100 -XX:+DisableExplicitGC -XX:TargetSurvivorRatio=90 -XX:G1NewSizePercent=50 -XX:G1MaxNewSizePercent=80 -XX:G1MixedGCLiveThresholdPercent=35 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -Dusing.aikars.flags=mcflags.emc.gs -jar {server_file}")
        
    def create_controls():#设置控件
        
        #开启服务器摁钮
        btn_start_server = ElevatedButton("开启服务器",width = 700,on_click=start_server)
        row_ui_top = Row(controls=[btn_start_server],alignment = MainAxisAlignment.SPACE_EVENLY)
        page.add(row_ui_top)
        
        #Java相关
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
        btn_show_java_path = ElevatedButton("显示Java路径",on_click=show_java_path)
        row_ui_java = Row([dd_choose_java,btn_show_java_path],alignment = MainAxisAlignment.END)
        page.add(row_ui_java)
        
        #侧边五个摁钮
        btn_log = ElevatedButton("日志")
        btn_frp = ElevatedButton("映射")
        btn_about = ElevatedButton("关于")
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
        
        def result(e: FilePickerResultEvent):
            global file_result
            file_result = e.files
            
        java_option = dd_choose_java.value
        if java_option == 'Path':
            use_java = 'java'
        else:
            pick_java = FilePicker(on_result=result)
            page.overlay.append(pick_java)
            page.update()
            if file_result != None:
                use_java = pick_java
            else:
                alert_warn_not_chosed_java = AlertDialog(
                title=Text("选择Java失败,请重新选择"), modal=True ,open=True)
                page.add(alert_warn_not_chosed_java)
                page.update()
                sleep(3)
                alert_warn_not_chosed_java.open = False
                page.update()
                
    def show_java_path(e):
        alert_show_java_path = AlertDialog(
            title=Text(f"Java路径(若为java则使用环境变量):{use_java}"), modal=True ,open=True)
        page.add(alert_show_java_path)
        page.update()
        sleep(3)
        alert_show_java_path.open = False
        page.update()
    init_page()
    create_controls()
    page.update()
    
flet.app(target=main)