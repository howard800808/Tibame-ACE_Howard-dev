from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.config import settings
from app.core.database import engine, Base
from app.routes import auth_router, user_router, system_router, emotion_router, video_router
from app.controllers.system_controller import system_controller
from app.views import auth_view, dashboard_view, user_view

# 建立資料表
Base.metadata.create_all(bind=engine)

# 建立 FastAPI 應用程式 (MVC 架構)
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    description="ACE服務管理後台",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 設定靜態檔案
app.mount("/static", StaticFiles(directory="static"), name="static")

# 設定模板
templates = Jinja2Templates(directory="templates")

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由 (Routes -> Controllers -> Services -> Models)
app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(system_router, prefix="/api")
app.include_router(emotion_router, prefix="/api")
app.include_router(video_router, prefix="/api")


# 登入頁面路由
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """登入頁面"""
    return await auth_view.login_page(request)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """儀表板頁面 (需要登入)"""
    return await dashboard_view.dashboard_page(request)


@app.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    """使用者列表頁面 (需要登入)"""
    return await user_view.user_list_page(request)


@app.get("/video-analysis", response_class=HTMLResponse)
async def video_analysis_page(request: Request):
    """影片情緒分析頁面 (需要登入)"""
    return templates.TemplateResponse(
        "video_analysis.html",
        {"request": request, "title": "影片情緒分析 - ACE服務管理後台"}
    )


# 全域 404 錯誤處理器
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return system_controller.not_found_error()
    return HTMLResponse(content=str(exc.detail), status_code=exc.status_code)


# 全域 500 錯誤處理器
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return system_controller.internal_server_error()


# 驗證錯誤處理器
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return HTMLResponse(
        content=f"<h1>400 - 驗證錯誤</h1><p>{exc.errors()}</p>",
        status_code=400
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
