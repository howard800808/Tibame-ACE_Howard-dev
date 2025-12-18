"""
ACE服務管理後台 - 派工單列表視圖
處理派工單列表頁面渲染
"""

from fastapi import Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates


class TaskView:
    """派工單列表頁面視圖"""
    
    @staticmethod
    async def task_list_page(request: Request) -> HTMLResponse:
        """
        渲染派工單列表頁面 (需要登入)
        
        Args:
            request: FastAPI Request 物件
            
        Returns:
            HTMLResponse: 派工單列表頁面 HTML
        """
        return templates.TemplateResponse(
            "tasks.html",
            {
                "request": request,
                "title": "派工單列表 - ACE服務管理後台",
                "system_name": "ACE服務管理後台",
                "header_title": "📊 派工單列表"
            }
        )


# 建立全域實例
task_view = TaskView()
