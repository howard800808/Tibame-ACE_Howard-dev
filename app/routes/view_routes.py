"""
頁面路由
處理 HTML 頁面的路由定義
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.views import auth_view, dashboard_view, user_view, mbti_view, task_view, linebot_view
from app.core.templates import templates
from app.core.config import settings

router = APIRouter(tags=["Pages"])


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """登入頁面"""
    return await auth_view.login_page(request)


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """儀表板頁面 (需要登入)"""
    return await dashboard_view.dashboard_page(request)


@router.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    """使用者列表頁面 (需要登入)"""
    return await user_view.user_list_page(request)


@router.get("/video-analysis", response_class=HTMLResponse)
async def video_analysis_page(request: Request):
    """影片情緒分析頁面 (需要登入)"""
    return templates.TemplateResponse(
        "video_analysis.html",
        {"request": request, "title": f"影片情緒分析 - {settings.SYSTEM_NAME}"}
    )


@router.get("/mbti", response_class=HTMLResponse)
async def mbti_analysis_page(request: Request):
    """MBTI 影片分析頁面"""
    return await mbti_view.mbti_page(request)


@router.get("/tasks", response_class=HTMLResponse)
async def tasks_page(request: Request):
    """任務管理頁面 (需要登入)"""
    return await task_view.task_list_page(request)


@router.get("/linebot/dashboard", response_class=HTMLResponse)
async def linebot_dashboard_page(request: Request):
    """LINE Bot 儀表板頁面 (需要登入)"""
    return await linebot_view.linebot_dashboard(request)


@router.get("/linebot/departments/{department_code}/tasks", response_class=HTMLResponse)
async def linebot_department_tasks(request: Request, department_code: str):
    """部門任務管理頁面"""
    return await linebot_view.department_tasks(request, department_code)


@router.get("/service-dashboard", response_class=HTMLResponse)
async def service_dashboard_page(request: Request):
    """JYS服務管理前台頁面"""
    return templates.TemplateResponse(
        "ace_service_dashboard.html",
        {
            "request": request,
            "title": "JYS服務管理前台",
            "header_title": "JYS服務管理前台"
        }
    )
