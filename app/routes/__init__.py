from .auth_routes import router as auth_router
from .user_routes import router as user_router
from .system_routes import router as system_router
from .mbti_routes import router as mbti_router

__all__ = ["auth_router", "user_router", "system_router", "mbti_router"]
