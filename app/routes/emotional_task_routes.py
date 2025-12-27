import json
from datetime import date, datetime, timedelta
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.emotional_task import EmotionalTask
from app.schemas.emotional_task_schema import EmotionalTaskResponse
from typing import List

# 兩份資料來源檔
DATA_FILES = [
    # 專案外層 db 目錄（本 repo 位置：.../Tibame-ACE/app/routes -> parents[3] 才到 .../團體專題）
    Path(__file__).resolve().parents[3] / "db" / "運動鞋製造公司_主管大會.json",
    Path(__file__).resolve().parents[3] / "db" / "親子兩天一夜_旅程.json",
]


def _parse_time(value: str):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError:
        return None


def _seed_emotional_tasks(db: Session):
    """從 json 檔案匯入感動任務（有則更新，無則新增）
    注意：不覆蓋既有記錄的 status，避免把執行中/已完成重置為 pending。
    """
    base_date = date.today()

    for file_path in DATA_FILES:
        if not file_path.exists():
            continue

        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        project_code = data.get("project_code")
        tasks = data.get("tasks", [])

        for item in tasks:
            day_offset = max(int(item.get("day", 1)) - 1, 0)
            task_date = base_date + timedelta(days=day_offset)
            task_id = item.get("task_id")
            if not task_id:
                continue

            record = db.query(EmotionalTask).filter_by(task_id=task_id).first()
            is_new = False
            if not record:
                record = EmotionalTask(task_id=task_id)
                db.add(record)
                is_new = True

            # 更新基本欄位（狀態除了新建外不覆蓋）
            record.project_code = project_code
            record.dept_code = item.get("dept_code")
            record.dept_name = item.get("dept_name")
            record.task_date = task_date
            record.time_start = _parse_time(item.get("time_start"))
            record.time_end = _parse_time(item.get("time_end"))
            record.location_code = item.get("location_code")
            record.sequence_stage = item.get("sequence")
            record.task_title = item.get("title")
            record.action_item = item.get("action_item")
            record.note = item.get("note")
            if is_new:
                record.status = item.get("status", "pending")

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # 如果存在重複 task_id，跳過，不中斷系統
        pass

router = APIRouter(
    prefix="/emotional-tasks",
    tags=["Emotional Tasks"]
)

@router.get("/", response_model=List[EmotionalTaskResponse])
def get_all_emotional_tasks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """取得所有感動派工任務"""
    # 僅在應用啟動時匯入，不在每次 GET 時重新匯入以免覆蓋 status 狀態
    # _seed_emotional_tasks(db)

    tasks = (
        db.query(EmotionalTask)
        .order_by(EmotionalTask.task_date, EmotionalTask.time_start, EmotionalTask.task_id)
        .all()
    )
    return [EmotionalTaskResponse.model_validate(t) for t in tasks]

@router.get("/emergency", response_model=List[EmotionalTaskResponse])
def get_emergency_emotional_tasks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """取得所有緊急感動派工任務"""
    # 僅在應用啟動時匯入，不在每次 GET 時重新匯入以免覆蓋 status 狀態
    # _seed_emotional_tasks(db)

    tasks = (
        db.query(EmotionalTask)
        .filter(EmotionalTask.status.in_(["pending", "assigned", "in_progress"]))
        .order_by(EmotionalTask.task_date, EmotionalTask.time_start, EmotionalTask.task_id)
        .all()
    )
    return [EmotionalTaskResponse.model_validate(t) for t in tasks]

@router.patch("/{task_id}/status")
def update_emotional_task_status(
    task_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新感動派工任務狀態"""
    task = db.query(EmotionalTask).filter(EmotionalTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task
