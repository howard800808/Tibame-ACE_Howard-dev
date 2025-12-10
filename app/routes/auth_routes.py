from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.auth_controller import auth_controller
from app.schemas.auth_schema import Token, LoginRequest
from app.schemas.user_schema import User, UserCreate

router = APIRouter(prefix="/auth", tags=["認證"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    註冊新使用者
    
    - **username**: 使用者名稱 (必填, 唯一)
    - **email**: Email (選填, 唯一)
    - **full_name**: 全名 (選填)
    - **password**: 密碼 (必填)
    - **is_active**: 是否啟用 (預設: True)
    """
    return auth_controller.register(user_data, db)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    使用者登入 (OAuth2 標準格式)
    
    使用 OAuth2 密碼流程進行登入，返回 JWT Token
    
    - **username**: 使用者名稱
    - **password**: 密碼
    """
    return auth_controller.login(form_data.username, form_data.password, db)


@router.post("/login/json", response_model=Token)
async def login_json(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    使用者登入 (JSON 格式)
    
    使用 JSON 格式進行登入，返回 JWT Token
    
    - **username**: 使用者名稱
    - **password**: 密碼
    """
    return auth_controller.login(login_data.username, login_data.password, db)
