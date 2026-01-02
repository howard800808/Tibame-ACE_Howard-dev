from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.controllers.task_controller import task_controller
from app.schemas.task_schema import TaskResponse, TaskDispatchRequest
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/dispatch", response_model=TaskResponse)
async def dispatch_task(
    request: TaskDispatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """建立並派發任務"""
    return await task_controller.dispatch_task(db, request)

@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """取得所有任務"""
    return task_controller.get_all_tasks(db)

@router.get("/emergency", response_model=List[TaskResponse])
def get_emergency_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """取得所有緊急任務"""
    return task_controller.get_emergency_tasks(db)

@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新任務狀態"""
    return task_controller.update_status(db, task_id, status)
