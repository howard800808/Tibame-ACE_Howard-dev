import asyncio
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.linebot_service import linebot_service
from app.core.database import connect_to_mongodb, close_mongodb_connection

async def test_broadcast():
    print("Initializing services...")
    await connect_to_mongodb()
    await linebot_service.initialize_departments()
    
    departments = ["GS", "HK", "CON", "BP", "FB", "CBS", "FS", "LUR", "GAE", "BB", "AD", "LA"]
    
    print("\nStarting broadcast test from MySQL DB...")
    
    for dept in departments:
        print(f"\nProcessing department: {dept}")
        try:
            # 1. Get tasks from MySQL
            bubbles = linebot_service.get_tasks_for_department(dept)
            print(f"  - Found {len(bubbles)} tasks in MySQL")
            
            if not bubbles:
                print("  - No tasks found, skipping broadcast.")
                continue
                
            # 2. Broadcast to Line
            carousel = {"type": "carousel", "contents": bubbles}
            ok = await linebot_service.broadcast_flex_to_department(
                dept, 
                alt_text=f"{dept} 測試任務 (DB)", 
                flex_contents=carousel
            )
            
            if ok:
                print(f"  - [SUCCESS] Broadcast sent to {dept}")
            else:
                error = linebot_service.get_last_error(dept)
                print(f"  - [FAILED] Broadcast failed: {error}")
                
        except Exception as e:
            print(f"  - [ERROR] Exception: {e}")

    await close_mongodb_connection()

if __name__ == "__main__":
    asyncio.run(test_broadcast())
