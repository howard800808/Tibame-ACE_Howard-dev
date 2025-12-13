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
    
    # 資料庫配置 (SQLAlchemy - 保留備用)
    DATABASE_URL: str = "sqlite:///./admin.db"
    SQLALCHEMY_MAX_OVERFLOW: Optional[int] = None
    SQLALCHEMY_WARN_20: Optional[int] = None
    DATABASE_POOL_CONNECTION_MIN: Optional[int] = None
    DATABASE_POOL_CONNECTION_MAX_OVERFLOW: Optional[int] = None
    DATABASE_POOL_CONNECTION_TIMEOUT: Optional[int] = None
    DATABASE_POOL_CONNECTION_RECYCLE: Optional[int] = None
    
    # MongoDB 配置
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "tibame_ace_db"
    
    # CORS 配置
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # LINE Bot 部門配置
    # GS - 客務部
    GS_ACCESS_TOKEN: Optional[str] = "MxuOtBSYhdm1T0XMAHonGiiIyIlwzVQ+4sTxW25Grruzxlz3TC+q50mxkcmu9dnnqkq1e8RNKm0bKoGlQETCC1X0/JoIkhkBobcT4c1Mz97YyvTdGSYMFQnQC/EZ1xwZawymWJihprpaLteucQ6gqgdB04t89/1O/w1cDnyilFU="
    GS_SECRET: Optional[str] = "ca87c1e2f974953a128e7dec4454f4fb"
    
    # HK - 房務部
    HK_ACCESS_TOKEN: Optional[str] = "HpQnEQnQkHnJrjUqnDhCf6VjDUbpFo3vfcgQmoIYRodHh41xBqKi5veh0ng/Fpb83O/bwMb2cl3PectuRXnFhAxUAQ9pOXXImUbhMrsDtX/Ojc8sjut7p8tm62eF7p9PBJHm0cjlU+4XvpQlBiukcgdB04t89/1O/w1cDnyilFU="
    HK_SECRET: Optional[str] = "484246f951afec8dacd6d3ca1f5056b"
    
    # CON - 門房諮詢
    CON_ACCESS_TOKEN: Optional[str] = "GgrwJ9o5Ob96ylf70vUr7yM1iJuyAG7UPWCJ0J7hsCrOXxZbKwuXdWSOmBxnP1VPgmfeEDe4NvF3yZQNnGYSVx/Zz/n/1YL6hHUHOx6NzKe/23rXNJYH9Fg0yrSwNri9xhOA4PlZhQBqaqWo1rnnzQdB04t89/1O/w1cDnyilFU="
    CON_SECRET: Optional[str] = "bec44c0da0920af55cd2af04650c767e"
    
    # BP - 烘焙點心房
    BP_ACCESS_TOKEN: Optional[str] = "p3IKt8qxi38bWa99f9zrFb7O1UNVioV2XspJTXcGOcDl5pGd6BvZiRb/ZiGYtpxweHz5IxaHdWHZ0+4YyBDK5UUTW6Nvr1js3jVa/AhvsODv66Gm17fq4r4PZh5U5FDZxeUesGiLuuXLNju5uTFkSwdB04t89/1O/w1cDnyilFU="
    BP_SECRET: Optional[str] = "246b6237d02d448396b2d8f856827637"
    
    # FB - 餐飲
    FB_ACCESS_TOKEN: Optional[str] = "HLK6AtfByF+obzujnta/XxhT9QD1JeDqYwFjiQryYRwXvKZvW3joLfS12EjI4LDyhsUYQTMFdNWEB2ocOkylOgVtTcaOPf51oFXYWbL6/ri9AVfWqDGMeD5J5q2+TtHzNE092UdhaT35zk85Pp3d6QdB04t89/1O/w1cDnyilFU="
    FB_SECRET: Optional[str] = "43019aef0ed7626c454e1a02795da0cc"
    
    # CBS - 會議宴會
    CBS_ACCESS_TOKEN: Optional[str] = "7iCPU+jjVueLE3GuWB/dBeJnocZD2ugA2S8vP82tocOqepa4wFWKr/jVww37EDk3Xhzr4OViyGYq0XvEpd8nexfpECEVBb0Iz5DQm+3KSex9rtQiNJ+GInCo2fisbsxcJ8wqIIAnvBJzPg5K+DU7kwdB04t89/1O/w1cDnyilFU="
    CBS_SECRET: Optional[str] = "1edff2612ed91a6821bcf393fee7ad97"
    
    # FS - 花房
    FS_ACCESS_TOKEN: Optional[str] = "QARjCy6uOvP55smmIUNiRSq0eTaUIfv3aQxvN6MZc0i/r+kTN1iAVDzpVi3irWWP1bIpeAGhQex8z9PKV133bSsWOYEjdu6QSJtqX+H0afzmoNfcD+Lyg2TVE1PmJCwVduZly9gvSIQOsQ5fPMPtuQdB04t89/1O/w1cDnyilFU="
    FS_SECRET: Optional[str] = "1f99fae43459eb6eb1e8a58cb6ac1c96"
    
    # LUR - 洗衣房與制服室
    LUR_ACCESS_TOKEN: Optional[str] = "UwAvvI1P0oGbX+WaWFTVtVOWUVzEd99cVMuMSxkkvrY5/poKBxmxwTJ2YdtgqXfgaA+pScfrPok7cqutwVIaYvaVF/poRj8mYpLTDXHikGv1uHJ++tmnY+WD1O5nG4II8RFkVaQNRnYwRttP9SH6kQdB04t89/1O/w1cDnyilFU="
    LUR_SECRET: Optional[str] = "10fdf3d150416feab83aeb0f40957ba3"
    
    # GAE - 總務工程
    GAE_ACCESS_TOKEN: Optional[str] = "Kh0qjTWkDHX3AsjwaflwFUh8QP9aEB62dbpKL1D2ExTv/zFdQyvWSrRIXlRSwn1WbEOcT0GQaN1Ec5LO1zCDR0WoG2IghuLvTPnPHPjd1E3ucEtoAS94dhjgtygroVhblhrKWoL9wOWkGuIaSEbaUgdB04t89/1O/w1cDnyilFU="
    GAE_SECRET: Optional[str] = "bc52327ede761af7bf6d69c84d993c79"
    
    # BB - 飲料酒吧
    BB_ACCESS_TOKEN: Optional[str] = "++yCqhlPe8PJCv2IPIzV9WNrvwM4YNYoTHgWakfo3OV9EtPhErAV448X4a+4iStkzNoWO9iL8DltrREPWq49OT4iim3w8Uh1M8ncbNpR5KTherDrlMMuEcQWiz7PpGO+4GCJG4hFAexJAZoz/ZgrJwdB04t89/1O/w1cDnyilFU="
    BB_SECRET: Optional[str] = "79482b03a698feda10a0fdbff7665f78"
    
    # AD - 美術設計
    AD_ACCESS_TOKEN: Optional[str] = "0+VkeT/tTERd640s5RhZTDFQC/Zsoe0xvmcGMko7js6BP8Z4ohpBHCHtC5iUs0swGvCiwlYfXW58FusubQ6YPTc+2nwOMiqgFk/mzKdTvlhHXviTQAudckmoGOBSbB77gEyKDhIht+PbKqVIKmIEsgdB04t89/1O/w1cDnyilFU="
    AD_SECRET: Optional[str] = "dd0455de07c4d1653ba25a8a0b6f9631"
    
    # LA - 休閒活動部
    LA_ACCESS_TOKEN: Optional[str] = "meO4TLMrgqT/uaM5fNTJcMkqhS52MeY+2+nkX1YJpcIAzsx2B/ANdOPE/XDWxj5/bvWGjiY6uaCiiHB0xCQEQOFX7t5NUSWBc/h9UAyJVZbpmr4K6L//PgavPFbgNIWM8walT8ZHPzSW8t0tsxwfYAdB04t89/1O/w1cDnyilFU="
    LA_SECRET: Optional[str] = "024f57951d26aaceb7185834c1269766"
    
    # Azure Language 配置
    AZURE_API_KEY: Optional[str] = None
    AZURE_END_POINT: Optional[str] = None
    
    # CWB 配置
    CWB_API_TOKEN: Optional[str] = None
    CWB_BASE_URL: Optional[str] = None
    
    # Ollama 配置
    OLLAMA_HOST: Optional[str] = None
    OLLAMA_MODEL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 忽略 .env 中未定義的額外欄位


settings = Settings()
