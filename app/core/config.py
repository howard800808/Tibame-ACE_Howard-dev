from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """應用程式配置"""
    
    # 基本配置
    APP_NAME: str = "FastAPI Admin Backend"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 資料庫配置
    DATABASE_URL: str = "sqlite:///./admin.db"
    SQLALCHEMY_MAX_OVERFLOW: Optional[int] = None
    SQLALCHEMY_WARN_20: Optional[int] = None
    DATABASE_POOL_CONNECTION_MIN: Optional[int] = None
    DATABASE_POOL_CONNECTION_MAX_OVERFLOW: Optional[int] = None
    DATABASE_POOL_CONNECTION_TIMEOUT: Optional[int] = None
    DATABASE_POOL_CONNECTION_RECYCLE: Optional[int] = None
    
    # CORS 配置
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # LINE 配置
    LINE_CHANNEL_ACCESS_TOKEN: Optional[str] = None
    LINE_CHANNEL_SECRET: Optional[str] = None
    
    # Azure Language 配置
    AZURE_API_KEY: Optional[str] = None
    AZURE_END_POINT: Optional[str] = None
    
    # Azure Speech-to-Text 配置
    AZURE_SPEECH_API_KEY: Optional[str] = None
    AZURE_SPEECH_ENDPOINT: Optional[str] = None
    AZURE_SPEECH_REGION: str = "eastus"
    
    # AWS 配置 (用于情感分析)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_DEFAULT_REGION: str = "us-east-1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 忽略 .env 中未定義的額外欄位


settings = Settings()
