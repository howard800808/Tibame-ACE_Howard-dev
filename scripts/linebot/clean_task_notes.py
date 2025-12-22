import sys
import os
import re

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy import create_engine, text
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.task_sql import HotelTask

def clean_task_notes():
    print("Cleaning up task notes...")
    db = SessionLocal()
    
    try:
        tasks = db.query(HotelTask).filter(HotelTask.note.isnot(None)).all()
        count = 0
        
        for task in tasks:
            if not task.note:
                continue
                
            original_note = task.note
            lines = original_note.split('\n')
            new_lines = []
            
            modified = False
            for line in lines:
                # Filter out report lines
                if line.strip().startswith('[Report Step') or line.strip() == '[System] 回報流程完成':
                    modified = True
                else:
                    new_lines.append(line)
            
            if modified:
                task.note = '\n'.join(new_lines).strip()
                count += 1
                print(f"Cleaned task {task.task_id}")
        
        db.commit()
        print(f"Cleanup completed. Modified {count} tasks.")
        
    except Exception as e:
        print(f"Error cleaning notes: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_task_notes()
