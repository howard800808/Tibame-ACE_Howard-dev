"""
ACE服務管理後台 - 感動派工列表視圖
處理感動派工列表頁面渲染
"""

from fastapi import Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates


class EmotionalTaskView:
    """感動派工列表頁面視圖"""
    
    @staticmethod
    async def emotional_task_list_page(request: Request) -> HTMLResponse:
        """
        渲染感動派工列表頁面 (需要登入)
        
        Args:
            request: FastAPI Request 物件
            
        Returns:
            HTMLResponse: 感動派工列表頁面 HTML
        """
        return templates.TemplateResponse(
            "emotional_tasks.html",
            {
                "request": request,
                "title": "感動派工列表 - ACE服務管理後台",
                "system_name": "ACE服務管理後台",
                "header_title": "💝 感動派工列表"
            }
        )


# 建立全域實例
emotional_task_view = EmotionalTaskView()
