from beanie import Document, Indexed
from pydantic import Field, EmailStr
from datetime import datetime
from typing import Optional
from bson import ObjectId


class User(Document):
    """使用者文檔模型 (MongoDB Beanie Document)"""
    
    username: Indexed(str, unique=True) = Field(..., description="使用者名稱", max_length=50)
    email: Indexed(EmailStr, unique=True) = Field(..., description="電子郵件")
    full_name: Optional[str] = Field(None, description="全名", max_length=100)
    hashed_password: str = Field(..., description="加密後的密碼")
    is_active: bool = Field(default=True, description="帳號是否啟用")
    role: str = Field(default="user", description="使用者角色: admin, manager, user", max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="建立時間")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新時間")
    
    class Settings:
        name = "users"  # MongoDB collection 名稱
        indexes = [
            "username",
            "email",
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "role": "user"
            }
        }
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
