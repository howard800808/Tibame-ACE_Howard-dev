from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Task(Base):
    """任務資料表模型"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="內部流水號")
    task_uid = Column(String(50), unique=True, nullable=False, comment="任務編號")
    title = Column(String(255), nullable=False, comment="任務標題")
    description = Column(Text, comment="任務詳細描述")
    location = Column(String(100), nullable=True, comment="發生地點")
    
    department = Column(String(50), nullable=True, index=True, comment="負責部門")
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="被指派人員ID")
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="通報人員ID")
    
    priority = Column(String(20), default="Medium", comment="優先順序")
    is_emergency = Column(Boolean, default=False, comment="是否為緊急事件")
    status = Column(String(20), default="Pending", index=True, comment="狀態")
    
    line_sent = Column(Boolean, default=False, comment="是否已發送 Line 通知")
    line_message_id = Column(String(100), nullable=True, comment="Line 訊息 ID")
    line_sent_at = Column(DateTime, nullable=True, comment="Line 發送時間")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="建立時間")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新時間")
    completed_at = Column(DateTime(timezone=True), nullable=True, comment="實際完成時間")
    due_at = Column(DateTime(timezone=True), nullable=True, comment="預計完成期限")

    # 關聯
    assignee = relationship("User", foreign_keys=[assignee_id], backref="assigned_tasks")
    reporter = relationship("User", foreign_keys=[reporter_id], backref="reported_tasks")
