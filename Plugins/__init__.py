import os, pkgutil
import sys
sys.path.append("..") 
from lib.log import log as log
log("已调用Plugins/__init__.py")
__all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))
log(f"当前__all__变量:{__all__}")