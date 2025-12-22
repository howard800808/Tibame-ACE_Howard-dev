from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task_schema import TaskCreate, TaskUpdate
from typing import List, Optional

class TaskService:
    def get_tasks(self, db: Session, skip: int = 0, limit: int = 100, is_emergency: Optional[bool] = None) -> List[Task]:
        query = db.query(Task)
        if is_emergency is not None:
            query = query.filter(Task.is_emergency == is_emergency)
        return query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()

    def create_task(self, db: Session, task: TaskCreate) -> Task:
        db_task = Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    def update_task_status(self, db: Session, task_id: int, status: str) -> Optional[Task]:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task:
            db_task.status = status
            db.commit()
            db.refresh(db_task)
        return db_task

task_service = TaskService()
