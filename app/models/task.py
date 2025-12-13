from beanie import Document
from typing import Optional
from datetime import datetime
from pydantic import Field
from enum import Enum


class TaskStatus(str, Enum):
    """任務狀態"""
    PENDING = "pending"          # 待處理
    IN_PROGRESS = "in_progress"  # 處理中
    COMPLETED = "completed"      # 已完成
    CANCELLED = "cancelled"      # 已取消


class TaskPriority(str, Enum):
    """任務優先級"""
    LOW = "low"           # 低
    MEDIUM = "medium"     # 中
    HIGH = "high"         # 高
    URGENT = "urgent"     # 緊急


class Task(Document):
    """任務資料模型"""
    
    department_code: str = Field(..., description="部門代碼")
    department_name: str = Field(..., description="部門名稱")
    
    # LINE Bot 相關資訊
    line_user_id: str = Field(..., description="LINE 使用者 ID")
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
    
    # LINE 訊息相關
    message_id: Optional[str] = Field(None, description="LINE 訊息 ID")
    message_type: Optional[str] = Field(None, description="訊息類型")
    original_message: Optional[str] = Field(None, description="原始訊息內容")
    
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
