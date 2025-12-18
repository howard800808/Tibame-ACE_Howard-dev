from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


class LineBotView:
    """LINE Bot 管理介面視圖"""
    
    async def linebot_dashboard(self, request: Request) -> HTMLResponse:
        """LINE Bot 儀表板頁面"""
        return templates.TemplateResponse(
            "linebot_dashboard.html",
            {"request": request, "title": "LINE Bot 管理"}
        )
    
    async def department_tasks(self, request: Request, department_code: str) -> HTMLResponse:
        """部門任務管理頁面"""
        return templates.TemplateResponse(
            "department_tasks.html",
            {
                "request": request,
                "title": f"{department_code} 任務管理",
                "department_code": department_code
            }
        )


linebot_view = LineBotView()
