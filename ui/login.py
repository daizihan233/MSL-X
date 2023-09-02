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
    
