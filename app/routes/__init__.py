from fastapi import FastAPI
from .auth_routes import router as auth_router
from .user_routes import router as user_router
from .system_routes import router as system_router
from .emotion_routes import router as emotion_router
from .video_routes import router as video_router
from .mbti_routes import router as mbti_router
from .adk_routes import router as adk_router
from .task_routes import router as task_router
from .linebot_routes import router as linebot_router, webhook_unified
from .view_routes import router as view_router

def init_routes(app: FastAPI):
    """
    初始化並註冊所有路由
    """
    # API Routes
    app.include_router(auth_router, prefix="/api")
    app.include_router(user_router, prefix="/api")
    app.include_router(system_router, prefix="/api")
    app.include_router(emotion_router, prefix="/api")
    app.include_router(video_router, prefix="/api")
    app.include_router(mbti_router, prefix="/api")
    app.include_router(adk_router, prefix="/api")
    app.include_router(task_router, prefix="/api")
    
    # LINE Bot Routes
    app.include_router(linebot_router)
    
    # [相容性修正] 註冊 /callback 路由以支援舊版 Webhook 設定
    app.add_api_route("/callback", webhook_unified, methods=["POST"])
    
    # Page Routes (View Layer)
    app.include_router(view_router)

__all__ = ["init_routes"]
