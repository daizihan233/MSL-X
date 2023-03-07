# 欢迎来到Custom.py!在这里你可以自定义MSLX加载时的行为,类似__init__!
# 程序会在定义变量前加载before_run(),定义变量后加载after_run()
def before_run():
    print("Custom Python Option Loaded[Pre]")
    
def after_run():
    print("Custom Python Option Loaded[After]")