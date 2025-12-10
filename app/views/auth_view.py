"""
ACE服務管理後台 - 認證視圖
處理登入、註冊頁面的渲染
"""

from fastapi import Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates


class AuthView:
    """認證頁面視圖"""
    
    @staticmethod
    async def login_page(request: Request) -> HTMLResponse:
        """
        渲染登入頁面
        
        Args:
            request: FastAPI Request 物件
            
        Returns:
            HTMLResponse: 登入頁面 HTML
        """
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "title": "登入 - ACE服務管理後台",
                "system_name": "ACE服務管理後台"
            }
        )


# 建立全域實例
auth_view = AuthView()
