from flet import \
(
   Theme,
   TextField,
   Dropdown,
   dropdown,
   ElevatedButton,
   Row 
)

import sys,os
sys.path.append("..")
#from lib.crypt import AES_encrypt,AES_decrypt
#from lib.crypt import RSA_encrypt,RSA_decrypt

def init_page(page):
    page.title = "MSLX | Panel Login"
    page.window_height = 550
    page.window_width = 900
    page.fonts = {
    "SHS_TC": "fonts/SourceHanSansTC-Regular.otf",
    "SHS_SC": "fonts/SourceHanSansSC-RegulAES_decryptar.otf"
}
    page.theme = Theme(font_family="SHS_SC")
    page.update()
    
def create_controls(page):
    
    global txt_passwd
    txt_passwd = TextField(label="在此输入您的密钥",width=850,height=400,can_reveal_password=True,multiline=True)
    
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
    btn_login = ElevatedButton("登录",width=100,on_click=process_login)
    row_top = Row(controls=[dd_mode,btn_login])
    page.add(row_top,txt_passwd)
    page.update()
    
def process_login(e):
    type = dd_choose_java.value
    if type == 'AES':
        AES_decrypt(txt_passwd.value, key)
        
def test_aes(e):
    
    if dd_mode.value == 'AES' and len(page.controls) < 3:
        txt_passwd.height = 200
        txt_aes_key = TextField(label="在此输入AES使用的key",width=850,height=200,can_reveal_password=True,multiline=True)
        page.add(txt_aes_key)
        page.update()
        
    if dd_mode.value == 'RSA' and len(page.controls) >= 3:
        page.controls.pop()
        page.update()