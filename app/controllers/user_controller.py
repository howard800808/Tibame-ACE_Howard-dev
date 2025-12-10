from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user_schema import User, UserUpdate
from app.services.user_service import user_service
from app.models.user import User as UserModel


class UserController:
    """使用者控制器 - 處理使用者管理相關的業務邏輯"""
    
    @staticmethod
    def get_current_user_info(current_user: UserModel) -> User:
        """取得當前使用者資訊"""
        return current_user
    
    @staticmethod
    def update_current_user(user_update: UserUpdate, current_user: UserModel, db: Session) -> User:
        """更新當前使用者資訊"""
        updated_user = user_service.update_user(db, current_user.id, user_update)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="使用者不存在"
            )
        return updated_user
    
    @staticmethod
    def get_users(skip: int, limit: int, db: Session) -> List[User]:
        """取得使用者列表"""
        users = user_service.get_users(db, skip=skip, limit=limit)
        return users
    
    @staticmethod
    def get_user_by_id(user_id: int, db: Session) -> User:
        """根據 ID 取得使用者"""
        user = user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="使用者不存在"
            )
        return user


user_controller = UserController()
