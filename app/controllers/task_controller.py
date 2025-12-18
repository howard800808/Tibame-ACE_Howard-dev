from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.task_service import task_service
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from typing import List, Optional

class TaskController:
    def get_emergency_tasks(self, db: Session) -> List[TaskResponse]:
        return task_service.get_tasks(db, is_emergency=True)

    def get_all_tasks(self, db: Session) -> List[TaskResponse]:
        return task_service.get_tasks(db)

    def update_status(self, db: Session, task_id: int, status: str) -> TaskResponse:
        task = task_service.update_task_status(db, task_id, status)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

task_controller = TaskController()
