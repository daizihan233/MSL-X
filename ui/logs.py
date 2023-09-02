from flet import \
(
    Theme,
    Text,
    TextField,
    Row,
    Column
)
from .Navbar import nav_side as navbar

def init_page(page):
    page.title = "MSLX | 日志"
    page.window_width = 900
    page.window_height = 600
    page.fonts = \
    {
        "SHS_TC": "fonts/SourceHanSansTC-Regular.otf",
        "SHS_SC": "fonts/SourceHanSansSC-Regular.otf"
    }
    page.theme = Theme(font_family="SHS_SC")
    page.update()
