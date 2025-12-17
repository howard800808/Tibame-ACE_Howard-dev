import asyncio
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.linebot_service import linebot_service
from app.core.database import SessionLocal
from app.models.task_sql import HotelTask

async def test_report_flow():
    print("Testing report flow with MySQL...")
    
    # 1. Find a task in MySQL
    db = SessionLocal()
    task = db.query(HotelTask).first()
    db.close()
    
    if not task:
        print("No tasks found in MySQL.")
        return

    task_id = task.task_id
    print(f"Using task: {task_id} ({task.title})")
    
    # 2. Simulate reporting steps
    steps = [
        (1, "yes"),
        (2, "text"),
        (3, "no"),
        (4, "positive"),
        (5, "done")
    ]
    
    for step, ans in steps:
        print(f"\nSimulating Step {step}: Answer='{ans}'")
        try:
            await linebot_service.record_report_answer(task_id, step, ans)
        except Exception as e:
            print(f"[ERROR] Step {step} failed: {e}")
            
    # 3. Verify the note in MySQL
    db = SessionLocal()
    updated_task = db.query(HotelTask).filter(HotelTask.task_id == task_id).first()
    print("\nUpdated Note:")
    print(updated_task.note)
    db.close()

if __name__ == "__main__":
    asyncio.run(test_report_flow())
