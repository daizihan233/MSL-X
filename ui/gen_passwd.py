from flet import Page,dropdown,TextField,Theme,Dropdown,ElevatedButton,Row,AlertDialog,TextButton,Text
import pyperclip as clip

import sys,os
sys.path.append("..")
from lib.crypt import AES_encrypt,AES_decrypt
from lib.crypt import RSA_encrypt,RSA_decrypt
    
def init_page(page:Page):
    page.title = "MSLX | Panel Password Genrate"
    page.window_height = 550
    page.window_width = 900
    page.fonts = {
    "SHS_TC": "fonts/SourceHanSansTC-Regular.otf",
    "SHS_SC": "fonts/SourceHanSansSC-Regular.otf"
}
    page.theme = Theme(font_family="SHS_SC")
    page.update()
    
def create_controls(page):
    
    global txt_passwd
    txt_passwd = TextField(label="在此输入您的原始密码",width=850,height=400,can_reveal_password=True,multiline=True)
    
    global dd_mode
    dd_mode = Dropdown(
        label = "方法选择",
        options=[
        dropdown.Option("AES"),
        dropdown.Option("RSA"),
        ],
        width=500,
        autofocus=True,
        on_change=test_aes
    )
    btn_gen = ElevatedButton("创建",width=100,on_click=process_gen)
    row_top = Row(controls=[dd_mode,btn_gen])
    page.add(row_top,txt_passwd)
    page.update()
    
def test_aes(e):
    
    if dd_mode.value == 'AES' and len(page.controls) < 3:
        txt_passwd.height = 200
        txt_aes_key = TextField(label="在此输入AES将使用的key,登陆时须和您的密钥一起使用",width=850,height=200,can_reveal_password=True,multiline=True)
        page.add(txt_aes_key)
        page.update()
        
    if dd_mode.value == 'RSA' and len(page.controls) >= 3:
        page.controls.pop()
        page.update()

def process_gen(e):
    
    def close(e):
        finish.open=False
        
    def copy_rsa(e):
        content = f"[RSA Login Info]\nPasswd:{result}"    
        clip.copy(content)
    
    def copy_aes(e):
        content = f"[AES Login Info]\nPasswd:{result}\nKey:{aes_key}"    
        clip.copy(content)
        
    if dd_mode.value == "AES":    
        aes_key = txt_aes_key.value
        result = AES_encrypt(org_str=txt_passwd.value,key=aes_key)
        finish = AlertDialog(title=Text("完成！"),content=Text(f"你已经完成了AES加密密码的创建流程,信息如下:\nPasswd:{result}\nKey:{aes_key}"),actions=[
                TextButton("确认", on_click=close),
                TextButton("复制信息到剪贴板", on_click=copy_aes),
            ],open=True)
        page.add(finish)
        page.update()
        
    if dd_mode.value == "RSA":    
        key = RSA.generate(2048)
        pri_key = key.export_key()
        with open("./pri_key.pem", "wb") as f:
            f.write(pri_key)
        pub_key = key.public_key().export_key()
        with open("./pub_key.pem", "wb") as f:
            f.write(pub_key)
        result = RSA_encrypt(text=txt_passwd.value,public_key=pub_key)
        finish = AlertDialog(title=Text("完成！"),content=Text(f"你已经完成了RSA加密密钥的创建流程,信息如下:\nPasswd:{result}"),actions=[
                TextButton("确认", on_click=close),
                TextButton("复制信息到剪贴板", on_click=copy_rsa),
            ],open=True)
        page.add(finish)
        page.update()
