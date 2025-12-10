from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """使用者基礎 Schema"""
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[str] = "user"  # admin, manager, user


class UserCreate(UserBase):
    """建立使用者 Schema"""
    password: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "john_doe",
                    "email": "john@example.com",
                    "full_name": "John Doe",
                    "password": "secret123",
                    "is_active": True,
                    "role": "user"
                }
            ]
        }
    }


class UserUpdate(BaseModel):
    """更新使用者 Schema"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None


class UserInDB(UserBase):
    """資料庫中的使用者 Schema"""
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }


class User(UserBase):
    """使用者回應 Schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john@example.com",
                    "full_name": "John Doe",
                    "is_active": True,
                    "role": "user",
                    "created_at": "2025-12-10T10:00:00",
                    "updated_at": "2025-12-10T10:00:00"
                }
            ]
        }
    }
