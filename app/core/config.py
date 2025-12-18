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
    
    # CWB 配置
    CWB_API_TOKEN: Optional[str] = None
    CWB_BASE_URL: Optional[str] = None
    
    # Ollama 配置
    OLLAMA_HOST: Optional[str] = None
    OLLAMA_MODEL: Optional[str] = None

    # Google ADK 配置
    ADK_BASE_URL: str = "https://llm.89.com.tw"
    ADK_APP_NAME: str = "agents"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 忽略 .env 中未定義的額外欄位


settings = Settings()
