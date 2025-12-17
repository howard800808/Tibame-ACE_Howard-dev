from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base

class HotelTask(Base):
    __tablename__ = "hotel_tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(255), nullable=False)
    task_id = Column(String(50), nullable=False)
    title = Column(String(255))  # 新增 title 欄位
    day = Column(Integer, nullable=False)
    time_start = Column(String(10))
    time_end = Column(String(10))
    dept_code = Column(String(50))
    dept_name = Column(String(100))
    location_code = Column(String(50))
    sequence = Column(String(10))
    action_item = Column(Text)
    note = Column(Text)
    status = Column(String(20), default='pending')
    guest_adults = Column(Integer)
    guest_children = Column(Integer)
    guest_room_id = Column(String(50))
    guest_special_needs = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class TaskReport(Base):
    __tablename__ = "task_reports"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(50), index=True, nullable=False)
    step = Column(Integer, nullable=False)
    answer = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
