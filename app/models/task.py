from beanie import Document
from typing import Optional
from datetime import datetime
from pydantic import Field, validator, root_validator
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



class Task(Document):
    """任務資料模型"""
    
    department_code: Optional[str] = Field(None, description="部門代碼")
    department_name: Optional[str] = Field(None, description="部門名稱")
    
    # LINE Bot 相關資訊
    line_user_id: Optional[str] = Field(None, description="LINE 使用者 ID")
    line_user_name: Optional[str] = Field(None, description="LINE 使用者名稱")
    
    # 任務資訊
    title: str = Field(..., description="任務標題")
    description: Optional[str] = Field(None, description="任務詳細描述")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="任務狀態")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="任務優先級")
    
    # 時間資訊
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = Field(None, description="截止日期")
    completed_at: Optional[datetime] = Field(None, description="完成時間")
    
    # 指派與處理
    assigned_to: Optional[str] = Field(None, description="指派給誰（使用者ID）")
    assigned_by: Optional[str] = Field(None, description="由誰指派")
    
    # 額外資訊
    notes: Optional[str] = Field(None, description="備註")
    tags: list[str] = Field(default_factory=list, description="標籤")

    # 回報流程紀錄
    report_answers: list[dict] = Field(default_factory=list, description="回報流程的答案紀錄")
    report_completed: bool = Field(default=False, description="回報流程是否完成")
    
    # LINE 訊息相關
    message_id: Optional[str] = Field(None, description="LINE 訊息 ID")
    message_type: Optional[str] = Field(None, description="訊息類型")
    original_message: Optional[str] = Field(None, description="原始訊息內容")
    
    # [相容性欄位] 支援舊版資料結構 (seed_tasks.py)
    room: Optional[str] = Field(None, description="房號 (舊版)")
    guest: Optional[str] = Field(None, description="客人名稱 (舊版)")
    content: Optional[str] = Field(None, description="內容 (舊版)")
    time_str: Optional[str] = Field(None, alias="time", description="時間字串 (舊版)")
    remark: Optional[str] = Field(None, description="備註 (舊版)")
    dept: Optional[str] = Field(None, description="部門名稱 (舊版)")

    class Settings:
        name = "tasks"
        indexes = [
            "department_code",
            "status",
            "priority",
            "line_user_id",
            "created_at",
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "department_code": "GS",
                "department_name": "客務部",
                "line_user_id": "U1234567890abcdef",
                "line_user_name": "張三",
                "title": "處理客戶退房問題",
                "description": "501房客戶反映退房流程有問題",
                "status": "pending",
                "priority": "high",
                "tags": ["退房", "客戶服務"]
            }
        }
