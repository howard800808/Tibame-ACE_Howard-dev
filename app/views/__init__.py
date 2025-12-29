"""
ACE服務管理後台 - 視圖層 (Views)
負責處理 HTML 模板渲染和頁面邏輯
"""

from .auth_view import auth_view
from .dashboard_view import dashboard_view
from .user_view import user_view
from .mbti_view import mbti_view
from .task_view import task_view
from .emotional_task_view import emotional_task_view

__all__ = [
    "auth_view",
    "dashboard_view",
    "user_view",
    "task_view",
    "mbti_view",
    "emotional_task_view",
]
