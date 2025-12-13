from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from typing import Optional

# MongoDB 客戶端
mongodbClient: Optional[AsyncIOMotorClient] = None


async def connect_to_mongodb():
    """連接到 MongoDB"""
    global mongodbClient
    try:
        mongodbClient = AsyncIOMotorClient(settings.MONGODB_URL)
        # 測試連接
        await mongodbClient.admin.command('ping')
        print(f"✓ 成功連接到 MongoDB: {settings.MONGODB_URL}")
        
        # 初始化 Beanie (需要導入所有文檔模型)
        from app.models.user import User
        from app.models.department import Department
        from app.models.task import Task
        
        await init_beanie(
            database=mongodbClient[settings.MONGODB_DB_NAME],
            document_models=[User, Department, Task]
        )
        print(f"✓ Beanie 初始化完成，使用資料庫: {settings.MONGODB_DB_NAME}")
    except Exception as e:
        print(f"✗ MongoDB 連接失敗: {str(e)}")
        raise


async def close_mongodb_connection():
    """關閉 MongoDB 連接"""
    global mongodbClient
    if mongodbClient:
        mongodbClient.close()
        print("✓ MongoDB 連接已關閉")


def get_database():
    """取得 MongoDB 資料庫實例"""
    if mongodbClient is None:
        raise Exception("MongoDB 尚未連接")
    return mongodbClient[settings.MONGODB_DB_NAME]


# 為了向後兼容保留的 SQLAlchemy 配置 (如需要可移除)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """取得資料庫 session (SQLAlchemy - 保留備用)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
