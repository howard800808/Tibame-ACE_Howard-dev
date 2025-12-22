from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from enum import Enum

class TaskStatus(str, Enum):
    """任務狀態"""
    PENDING = "pending"          # 待處理
    IN_PROGRESS = "in_progress"  # 處理中
    COMPLETED = "completed"      # 已完成
    CANCELLED = "cancelled"      # 已取消

    @classmethod
    def _missing_(cls, value):
        # 相容性處理：將大寫轉換為小寫
        if isinstance(value, str):
            lower_val = value.lower()
            if lower_val in cls._value2member_map_:
                return cls._value2member_map_[lower_val]
        return super()._missing_(value)


class TaskPriority(str, Enum):
    """任務優先級"""
    LOW = "low"           # 低
    MEDIUM = "medium"     # 中
    HIGH = "high"         # 高
    URGENT = "urgent"     # 緊急

    @classmethod
    def _missing_(cls, value):
        # 相容性處理：將代碼轉換為 Enum
        mapping = {
            "P": cls.URGENT,
            "E": cls.HIGH,
            "F": cls.MEDIUM,
            "L": cls.LOW
        }
        if value in mapping:
            return mapping[value]
        if isinstance(value, str):
            lower_val = value.lower()
            if lower_val in cls._value2member_map_:
                return cls._value2member_map_[lower_val]
        return super()._missing_(value)

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


class TaskReport(Base):
    """任務回報紀錄"""
    __tablename__ = "task_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(String(50), index=True, nullable=False, comment="任務編號")
    step = Column(Integer, nullable=False, comment="回報步驟")
    answer = Column(Text, comment="回報內容")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="建立時間")