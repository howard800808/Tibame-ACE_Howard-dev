from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.task_service import task_service
from app.services.linebot_service import linebot_service
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse, TaskDispatchRequest
from app.models.user import User
from typing import List, Optional
from datetime import datetime

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

    async def dispatch_task(self, db: Session, request: TaskDispatchRequest) -> TaskResponse:
        # Generate UID
        uid = f"T{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create Task
        task_create = TaskCreate(
            task_uid=uid,
            **request.model_dump(exclude={'send_line'})
        )
        task = await task_service.create_task_async(db, task_create)
        
        # Send Line Notification
        if request.send_line and request.department:
            user_line_id = None
            # Note: User model currently doesn't have line_user_id, so we default to department broadcast
            # if request.assignee_id:
            #     user = db.query(User).filter(User.id == request.assignee_id).first()
            #     if user and hasattr(user, 'line_user_id'):
            #         user_line_id = user.line_user_id
            
            # Send Flex Card
            success = await linebot_service.send_task_flex_card(
                department_code=request.department,
                user_id=user_line_id,
                task=task
            )
            
            if success:
                task.line_sent = True
                task.line_sent_at = datetime.now()
                db.commit()
                db.refresh(task)
                
        return task

task_controller = TaskController()
