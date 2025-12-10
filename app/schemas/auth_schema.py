from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Token 回應 Schema"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token 資料 Schema"""
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """登入請求 Schema"""
    username: str
    password: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "admin",
                    "password": "admin123"
                }
            ]
        }
    }
