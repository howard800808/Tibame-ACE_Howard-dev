"""
ACE服務管理後台 - 使用者視圖
處理使用者管理頁面的渲染
"""

from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.services.user_service import user_service
from app.core.templates import templates


class UserView:
    """使用者管理頁面視圖"""
    
    @staticmethod
    async def user_list_page(request: Request) -> HTMLResponse:
        """
        渲染使用者列表頁面 (需要登入)
        前端會透過 JavaScript 檢查 token 並獲取使用者資料
        
        Args:
            request: FastAPI Request 物件
            
        Returns:
            HTMLResponse: 使用者列表頁面 HTML
        """
        return templates.TemplateResponse(
            "users.html",
            {
                "request": request,
                "title": "使用者管理 - ACE服務管理後台",
                "system_name": "ACE服務管理後台"
            }
        )


# 建立全域實例
user_view = UserView()
