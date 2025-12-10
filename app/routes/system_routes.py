from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.controllers.system_controller import system_controller

router = APIRouter(tags=["系統"])


@router.get("/health")
async def health_check():
    """
    健康檢查
    
    檢查系統是否正常運作
    """
    return system_controller.health_check()


@router.get("/error/404", response_class=HTMLResponse)
async def error_404():
    """
    404 錯誤頁面 (IIS 格式)
    
    返回標準的 404 錯誤頁面
    """
    return system_controller.not_found_error()


@router.get("/error/500", response_class=HTMLResponse)
async def error_500():
    """
    500 錯誤頁面 (IIS 格式)
    
    返回標準的 500 錯誤頁面
    """
    return system_controller.internal_server_error()
