import json
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.core.config import settings
from app.models.task_sql import HotelTask, Base

def import_data(json_file_path):
    # Read JSON data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Connect to Database
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()

    try:
        project_name = data.get('project_name')
        guest_profile = data.get('guest_profile', {})
        tasks = data.get('tasks', [])

        print(f"Importing project: {project_name}")
        print(f"Found {len(tasks)} tasks.")

        for task_data in tasks:
            task_id = task_data.get('task_id')
            dept_code = task_data.get('dept_code')
            
            # [Fix] Replace 'F&B' with 'FB' to match system code
            if 'F&B' in task_id:
                task_id = task_id.replace('F&B', 'FB')
            if dept_code == 'F&B':
                dept_code = 'FB'
                
            # Use title from JSON if available, otherwise fallback to generated
            generated_title = task_data.get('title', f"任務 #{task_id}")

            # Check if task already exists (optional, by task_id and project_name)
            existing_task = db.query(HotelTask).filter_by(
                task_id=task_id,
                project_name=project_name
            ).first()

            if existing_task:
                print(f"Task {task_id} already exists. Updating...")
                # Update existing task
                existing_task.title = generated_title
                existing_task.day = task_data.get('day')
                existing_task.time_start = task_data.get('time_start')
                existing_task.time_end = task_data.get('time_end')
                existing_task.dept_code = dept_code
                existing_task.dept_name = task_data.get('dept_name')
                existing_task.location_code = task_data.get('location_code')
                existing_task.sequence = task_data.get('sequence')
                existing_task.action_item = task_data.get('action_item')
                existing_task.note = task_data.get('note')
                existing_task.status = task_data.get('status', 'pending')
                existing_task.guest_adults = guest_profile.get('adults')
                existing_task.guest_children = guest_profile.get('children')
                existing_task.guest_room_id = guest_profile.get('room_id')
                existing_task.guest_special_needs = json.dumps(guest_profile.get('special_needs', []), ensure_ascii=False)
                continue

            new_task = HotelTask(
                project_name=project_name,
                task_id=task_id,
                title=generated_title,
                day=task_data.get('day'),
                time_start=task_data.get('time_start'),
                time_end=task_data.get('time_end'),
                dept_code=dept_code,
                dept_name=task_data.get('dept_name'),
                location_code=task_data.get('location_code'),
                sequence=task_data.get('sequence'),
                action_item=task_data.get('action_item'),
                note=task_data.get('note'),
                status=task_data.get('status', 'pending'),
                guest_adults=guest_profile.get('adults'),
                guest_children=guest_profile.get('children'),
                guest_room_id=guest_profile.get('room_id'),
                guest_special_needs=json.dumps(guest_profile.get('special_needs', []), ensure_ascii=False)
            )
            db.add(new_task)
        
        db.commit()
        print("Import completed successfully.")

    except Exception as e:
        print(f"Error importing data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Default path or from argument
    json_path = r"c:\Users\HOWARD\Downloads\hotel_task_scenarios_for_DB.json"
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
    else:
        import_data(json_path)
