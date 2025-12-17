import asyncio
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, PydanticObjectId
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.department import Department
from app.services.linebot_service import linebot_service

# MongoDB Config
MONGO_URI = "mongodb://localhost:27017/tibame_ace_db"

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(database=client.get_default_database(), document_models=[Task, Department])
    print("[Init] DB Connected")

async def test_postback_logic():
    await init_db()

    # 1. Create a dummy task
    print("\n[Step 1] Creating dummy task...")
    task = Task(
        department_code="HK",
        department_name="房務部",
        title="測試任務 - Postback",
        description="這是一個測試任務",
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM,
        created_at=datetime.utcnow()
    )
    await task.save()
    task_id = str(task.id)
    print(f"  - Task created: {task_id} (Status: {task.status})")

    # 2. Simulate "Accept" Postback (PENDING -> IN_PROGRESS)
    print("\n[Step 2] Simulating 'Accept' button click...")
    # Data format from flex_templates.py: action=task&op=accept&id={task_id}&dept=HK
    postback_data = f"action=task&op=accept&id={task_id}&dept=HK"
    print(f"  - Postback Data: {postback_data}")
    
    # Parse data (logic from controller)
    parsed = dict(item.split("=") for item in postback_data.split("&"))
    action = parsed.get('action')
    op = parsed.get('op')
    tid = parsed.get('id')
    
    if action == 'task' and op == 'accept':
        updated_task = await linebot_service.update_task_status(tid, TaskStatus.IN_PROGRESS, notes="LINEBot accept")
        if updated_task:
            print(f"  - [SUCCESS] Task status updated to: {updated_task.status}")
        else:
            print(f"  - [FAILED] Task update failed")
    
    # Verify in DB
    t_check = await Task.get(PydanticObjectId(task_id))
    assert t_check.status == TaskStatus.IN_PROGRESS
    print("  - DB Verification: OK")

    # 3. Simulate "Complete" Postback (IN_PROGRESS -> COMPLETED)
    print("\n[Step 3] Simulating 'Complete' button click...")
    postback_data = f"action=task&op=complete&id={task_id}&dept=HK"
    print(f"  - Postback Data: {postback_data}")
    
    parsed = dict(item.split("=") for item in postback_data.split("&"))
    op = parsed.get('op')
    
    if op == 'complete':
        updated_task = await linebot_service.update_task_status(tid, TaskStatus.COMPLETED, notes="LINEBot complete")
        if updated_task:
            print(f"  - [SUCCESS] Task status updated to: {updated_task.status}")
        else:
            print(f"  - [FAILED] Task update failed")

    # Verify in DB
    t_check = await Task.get(PydanticObjectId(task_id))
    assert t_check.status == TaskStatus.COMPLETED
    print("  - DB Verification: OK")

    # 4. Simulate "Archive" Postback (COMPLETED -> COMPLETED/Archived)
    print("\n[Step 4] Simulating 'Archive' button click...")
    postback_data = f"action=task&op=archive&id={task_id}&dept=HK"
    print(f"  - Postback Data: {postback_data}")
    
    parsed = dict(item.split("=") for item in postback_data.split("&"))
    op = parsed.get('op')
    
    if op == 'archive':
        # Archive usually just keeps it completed or moves it. Controller logic maps archive -> COMPLETED.
        updated_task = await linebot_service.update_task_status(tid, TaskStatus.COMPLETED, notes="LINEBot archive")
        if updated_task:
            print(f"  - [SUCCESS] Task status updated to: {updated_task.status}")
    
    print("\n[Test Completed] All button actions simulated successfully.")

    # Cleanup
    await task.delete()
    print("  - Dummy task deleted.")

if __name__ == "__main__":
    asyncio.run(test_postback_logic())
