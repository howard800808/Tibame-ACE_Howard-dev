from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


class MBTIView:
    """MBTI 分析視圖層 - 處理頁面渲染"""
    
    @staticmethod
    async def mbti_page(request: Request) -> HTMLResponse:
        """
        渲染 MBTI 影片分析頁面
        
        Args:
            request: FastAPI 請求物件
            
        Returns:
            渲染後的 HTML 頁面
        """
        return templates.TemplateResponse("mbti.html", {"request": request})


# 建立全域視圖實例
mbti_view = MBTIView()
