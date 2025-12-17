from .auth_routes import router as auth_router
from .user_routes import router as user_router
from .system_routes import router as system_router
from .emotion_routes import router as emotion_router
from .video_routes import router as video_router

__all__ = ["auth_router", "user_router", "system_router", "emotion_router", "video_router"]
