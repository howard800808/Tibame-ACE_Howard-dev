from datetime import date, time, datetime
from sqlalchemy import Column, Integer, String, Date, Time, Text, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.core.database import Base


class EmotionalTask(Base):
    """情感體驗任務資料表"""
    __tablename__ = "emotional_tasks"
    __table_args__ = (UniqueConstraint("task_id", name="uk_emotional_task_id"),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_code = Column(String(20), nullable=True, index=True)
    task_id = Column(String(50), nullable=False)

    dept_code = Column(String(20), nullable=True, index=True)
    dept_name = Column(String(100), nullable=True)

    task_date = Column(Date, nullable=True, index=True)
    time_start = Column(Time, nullable=True)
    time_end = Column(Time, nullable=True)
    location_code = Column(String(50), nullable=True)

    sequence_stage = Column(String(5), nullable=True, comment="P=準備 E=執行 F=收尾")
    task_title = Column(String(255), nullable=True)
    action_item = Column(Text, nullable=True)
    note = Column(Text, nullable=True)

    status = Column(String(30), nullable=True, index=True, default="pending")
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # 任務回報欄位
    report_is_finished = Column(String(10), nullable=True, comment="是否順利完成 (yes/no)")
    report_details = Column(Text, nullable=True, comment="補充說明")
    report_has_interaction = Column(String(10), nullable=True, comment="與顧客有互動嗎 (yes/no)")
    report_sentiment = Column(String(20), nullable=True, comment="顧客情緒 (positive/neutral/negative)")
    report_remarks = Column(Text, nullable=True, comment="備註事項")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
