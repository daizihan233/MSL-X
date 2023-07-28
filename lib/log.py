import os
import datetime

if not os.path.exists('logs'):
    os.mkdir('logs')
    
with open('logs/latest.log','w',encoding='utf-8') as f:
    f.write('')

def log(content:str,level:int = 0):
    level_list = ['[Information]','[Warning]    ','[Error]      ']
    time = datetime.datetime.now().strftime('[%H:%M:%S]')
    log_content = time+level_list[level]+content
    print(log_content)
    with open('logs/latest.log','a',encoding='utf-8') as f:
        f.write(log_content+'\n')