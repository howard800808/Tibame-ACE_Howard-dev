from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.config import settings
from app.core.database import engine, Base
from app.core.security import decode_access_token, create_access_token
from app.routes import init_routes
from app.controllers.system_controller import system_controller
from app.services.linebot_service import linebot_service

# 建立 FastAPI 應用程式 (MVC 架構)
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    description="ACE服務管理後台",
    docs_url="/docs",
    redoc_url="/redoc"
)


# 應用程式啟動事件
@app.on_event("startup")
async def startup_event():
    """應用程式啟動時執行"""
    # 初始化 LINE Bot 服務
    await linebot_service.initialize_departments()
    # SQLAlchemy 建立資料表
    Base.metadata.create_all(bind=engine)


# 應用程式關閉事件
@app.on_event("shutdown")
async def shutdown_event():
    """應用程式關閉時執行"""
    pass

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
    expose_headers=["X-New-Token"],  # 允許前端讀取新 Token
)

# 滑動會話 (Sliding Session) 中間件 - 每次請求自動延長 Token 有效期
@app.middleware("http")
async def sliding_session_middleware(request: Request, call_next):
    response = await call_next(request)
    
    # 檢查請求中是否有 Authorization Header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            # 解碼 Token 以獲取使用者資訊
            payload = decode_access_token(token)
            if payload and "sub" in payload:
                # 重新產生一個新的 Token (有效期限重新計算)
                new_token = create_access_token(data={"sub": payload["sub"]})
                # 將新 Token 放入 Response Header
                response.headers["X-New-Token"] = new_token
        except Exception:
            # 如果 Token 無效或解碼失敗，不執行任何操作，讓後續的驗證邏輯處理
            pass
            
    return response

# 註冊所有路由 (API + Pages)
init_routes(app)

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
        reload=False  # 禁用自動重載，避免服務器重啟
    )
