from datetime import date, time, datetime
from typing import Optional
from pydantic import BaseModel


class EmotionalTaskBase(BaseModel):
    project_code: Optional[str] = None
    task_id: str
    dept_code: Optional[str] = None
    dept_name: Optional[str] = None
    task_date: Optional[date] = None
    time_start: Optional[time] = None
    time_end: Optional[time] = None
    location_code: Optional[str] = None
    sequence_stage: Optional[str] = None
    task_title: Optional[str] = None
    action_item: Optional[str] = None
    note: Optional[str] = None
    status: Optional[str] = None
    completed_at: Optional[datetime] = None
    
    # 回報欄位
    report_is_finished: Optional[str] = None
    report_details: Optional[str] = None
    report_has_interaction: Optional[str] = None
    report_sentiment: Optional[str] = None
    report_remarks: Optional[str] = None


class EmotionalTaskReportCreate(BaseModel):
    report_is_finished: str
    report_details: Optional[str] = None
    report_has_interaction: str
    report_sentiment: str
    report_remarks: Optional[str] = None


class EmotionalTaskResponse(EmotionalTaskBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
