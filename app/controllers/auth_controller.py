from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.auth_schema import Token, LoginRequest
from app.schemas.user_schema import User, UserCreate
from app.services.user_service import user_service


class AuthController:
    """認證控制器 - 處理認證相關的業務邏輯"""
    
    @staticmethod
    def register(user_data: UserCreate, db: Session) -> User:
        """註冊新使用者"""
        # 檢查使用者名稱是否已存在
        existing_user = user_service.get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="使用者名稱已存在"
            )
        
        # 檢查 Email 是否已存在
        if user_data.email:
            existing_email = user_service.get_user_by_email(db, user_data.email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email 已存在"
                )
        
        # 建立使用者
        user = user_service.create_user(db, user_data)
        return user
    
    @staticmethod
    def login(username: str, password: str, db: Session) -> Token:
        """使用者登入"""
        # 驗證使用者
        user = user_service.authenticate_user(db, username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="使用者名稱或密碼錯誤",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="使用者未啟用"
            )
            
        # 更新最後登入時間 (使用 UTC+8 台北時間)
        taipei_tz = timezone(timedelta(hours=8))
        user.last_login = datetime.now(taipei_tz)
        db.commit()
        
        # 建立 access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")


auth_controller = AuthController()
