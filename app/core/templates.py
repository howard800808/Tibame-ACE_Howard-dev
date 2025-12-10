"""
ACE服務管理後台 - 模板配置
統一管理 Jinja2 模板引擎
"""

from fastapi.templating import Jinja2Templates

# 建立全域 Jinja2Templates 實例
templates = Jinja2Templates(directory="templates")
