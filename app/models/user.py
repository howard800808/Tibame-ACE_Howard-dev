from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """使用者資料表模型 (Model層)"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False, comment="使用者名稱")
    email = Column(String(100), unique=True, index=True, comment="電子郵件")
    full_name = Column(String(100), comment="全名")
    hashed_password = Column(String(255), nullable=False, comment="加密後的密碼")
    is_active = Column(Boolean, default=True, comment="帳號是否啟用")
    role = Column(String(20), default="user", comment="使用者角色: admin, manager, user")
    department = Column(String(50), nullable=True, comment="部門: admin, sales, production, warehouse")
    last_login = Column(DateTime(timezone=True), nullable=True, comment="最後登入時間")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="建立時間")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新時間")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
