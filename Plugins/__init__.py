import os, pkgutil
import sys
sys.path.append("..") 
from loguru import logger
logger.add('Logs/{time:YYYY-MM-DD}-PluginInit.log', format='[{time:HH:mm:ss}][{level}] {message}', encoding='utf-8', backtrace=True, diagnose=True, compression="tar.gz" )
logger.debug("已调用Plugins/__init__.py")
__all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)])) #type:ignore
logger.debug(f"当前__all__变量:{__all__}")