"""
ACE服務管理後台 - 儀表板視圖
處理登入後的儀表板頁面渲染
"""

from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.core.templates import templates


class DashboardView:
    """儀表板頁面視圖"""
    
    @staticmethod
    async def dashboard_page(request: Request) -> HTMLResponse:
        """
        渲染儀表板頁面 (需要登入)
        前端會透過 JavaScript 檢查 token 並獲取使用者資料
        
        Args:
            request: FastAPI Request 物件
            
        Returns:
            HTMLResponse: 儀表板頁面 HTML
        """
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "title": "儀表板 - ACE服務管理後台",
                "system_name": "ACE服務管理後台",
                "header_title": "🏠 ACE服務管理後台"
            }
        )


# 建立全域實例
dashboard_view = DashboardView()
