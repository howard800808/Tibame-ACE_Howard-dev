from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import decode_access_token
from app.services.user_service import user_service
from app.models.user import User

# OAuth2 密碼流程
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """取得當前使用者"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="無法驗證憑證",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 解碼 token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    # 從資料庫取得使用者
    user = user_service.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """取得當前啟用的使用者"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="使用者未啟用"
        )
    return current_user


async def get_optional_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """取得可選的當前使用者 (無 token 時返回 None)"""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    
    # 解析 Bearer token
    if not auth_header.startswith("Bearer "):
        return None
    
    token = auth_header[7:]  # 移除 "Bearer " 前綴
    
    payload = decode_access_token(token)
    if payload is None:
        return None
    
    username: str = payload.get("sub")
    if username is None:
        return None
    
    user = user_service.get_user_by_username(db, username=username)
    if user and not user.is_active:
        return None
    
    return user
