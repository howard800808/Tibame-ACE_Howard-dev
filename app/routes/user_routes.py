from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.controllers.user_controller import user_controller
from app.schemas.user_schema import User, UserUpdate
from app.core.dependencies import get_current_active_user
from app.models.user import User as UserModel

router = APIRouter(prefix="/users", tags=["使用者管理"])


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    取得當前使用者資訊
    
    需要提供有效的 JWT Token
    """
    return user_controller.get_current_user_info(current_user)


@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新當前使用者資訊
    
    需要提供有效的 JWT Token
    
    - **email**: 新的 Email (選填)
    - **full_name**: 新的全名 (選填)
    - **password**: 新的密碼 (選填)
    - **is_active**: 是否啟用 (選填)
    """
    return user_controller.update_current_user(user_update, current_user, db)


@router.get("/", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    取得使用者列表
    
    需要提供有效的 JWT Token
    
    - **skip**: 跳過的筆數 (預設: 0)
    - **limit**: 限制回傳筆數 (預設: 100)
    """
    return user_controller.get_users(skip, limit, db)


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    根據 ID 取得使用者
    
    需要提供有效的 JWT Token
    
    - **user_id**: 使用者 ID
    """
    return user_controller.get_user_by_id(user_id, db)
