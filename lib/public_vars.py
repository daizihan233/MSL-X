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