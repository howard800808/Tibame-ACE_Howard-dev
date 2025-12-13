from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    """建立任務的請求結構"""
    department_code: str
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    tags: list[str] = Field(default_factory=list)
    assigned_to: Optional[str] = None


class TaskUpdate(BaseModel):
    """更新任務的請求結構"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    tags: Optional[list[str]] = None
    assigned_to: Optional[str] = None
    notes: Optional[str] = None


class TaskResponse(BaseModel):
    """任務回應結構"""
    id: str
    department_code: str
    department_name: str
    line_user_id: str
    line_user_name: Optional[str]
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    assigned_to: Optional[str]
    tags: list[str]
    
    class Config:
        from_attributes = True


class LineBotWebhookEvent(BaseModel):
    """LINE Bot Webhook 事件基礎結構"""
    type: str
    timestamp: int
    source: dict
    replyToken: Optional[str] = None


class LineBotMessageEvent(LineBotWebhookEvent):
    """LINE Bot 訊息事件"""
    message: dict


class LineBotWebhookRequest(BaseModel):
    """LINE Bot Webhook 請求結構"""
    destination: str
    events: list[dict]


class DepartmentCreate(BaseModel):
    """建立部門的請求結構"""
    code: str = Field(..., description="部門代碼", min_length=2, max_length=10)
    name: str = Field(..., description="部門名稱")
    access_token: str = Field(..., description="LINE Bot Access Token")
    channel_secret: str = Field(..., description="LINE Bot Channel Secret")
    is_active: bool = Field(default=True)
    description: Optional[str] = None


class DepartmentUpdate(BaseModel):
    """更新部門的請求結構"""
    name: Optional[str] = None
    access_token: Optional[str] = None
    channel_secret: Optional[str] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None


class DepartmentResponse(BaseModel):
    """部門回應結構"""
    id: str
    code: str
    name: str
    is_active: bool
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
