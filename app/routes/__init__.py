from .auth_routes import router as auth_router
from .user_routes import router as user_router
from .system_routes import router as system_router
from .adk_routes import router as adk_router
from .task_routes import router as task_router

__all__ = ["auth_router", "user_router", "system_router", "adk_router", "task_router"]
