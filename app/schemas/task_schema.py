from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None
    priority: Optional[str] = "Medium"
    is_emergency: Optional[bool] = False
    status: Optional[str] = "Pending"
    due_at: Optional[datetime] = None

class TaskCreate(TaskBase):
    task_uid: str
    assignee_id: Optional[int] = None
    reporter_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None
    assignee_id: Optional[int] = None
    priority: Optional[str] = None
    is_emergency: Optional[bool] = None
    status: Optional[str] = None
    due_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class TaskResponse(TaskBase):
    id: int
    task_uid: str
    assignee_id: Optional[int] = None
    reporter_id: Optional[int] = None
    line_sent: bool
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
