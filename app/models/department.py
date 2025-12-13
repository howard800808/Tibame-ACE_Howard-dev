from beanie import Document
from typing import Optional
from datetime import datetime
from pydantic import Field


class Department(Document):
    """部門資料模型"""
    
    code: str = Field(..., description="部門代碼，例如: GS, HK, CON")
    name: str = Field(..., description="部門名稱")
    access_token: str = Field(..., description="LINE Bot Access Token")
    channel_secret: str = Field(..., description="LINE Bot Channel Secret")
    is_active: bool = Field(default=True, description="是否啟用")
    description: Optional[str] = Field(None, description="部門描述")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "departments"
        indexes = [
            "code",
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "GS",
                "name": "客務部",
                "access_token": "your-access-token",
                "channel_secret": "your-channel-secret",
                "is_active": True,
                "description": "負責前台接待與客戶服務"
            }
        }
