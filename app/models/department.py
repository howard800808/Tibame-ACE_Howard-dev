from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Department(Base):
    """部門資料表模型"""
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False, index=True, comment="部門代碼")
    name_zh = Column(String(100), nullable=False, comment="部門名稱(中文)")
    name_en = Column(String(100), nullable=False, comment="部門名稱(英文)")
    channel_access_token = Column(String(255), nullable=False, comment="LINE Bot Access Token")
    channel_secret = Column(String(255), nullable=False, comment="LINE Bot Channel Secret")
    # is_active = Column(Boolean, default=True, comment="是否啟用") # DB schema 中沒有此欄位
    # description = Column(Text, nullable=True, comment="部門描述") # DB schema 中沒有此欄位
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="建立時間")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新時間")

    @property
    def name(self):
        return self.name_zh

    @property
    def access_token(self):
        return self.channel_access_token

    @property
    def is_active(self):
        return True # 預設為 True，因為 DB 沒有此欄位
