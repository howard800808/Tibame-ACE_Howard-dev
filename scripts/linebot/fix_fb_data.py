import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy import create_engine, text
from app.core.config import settings

def fix_fb_data():
    DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        print("Checking for 'F&B' data...")
        
        # Check count
        result = connection.execute(text("SELECT COUNT(*) FROM hotel_tasks WHERE dept_code = 'F&B'"))
        count_dept = result.scalar()
        
        result = connection.execute(text("SELECT COUNT(*) FROM hotel_tasks WHERE task_id LIKE '%F&B%'"))
        count_id = result.scalar()
        
        print(f"Found {count_dept} tasks with dept_code='F&B'")
        print(f"Found {count_id} tasks with task_id containing 'F&B'")
        
        if count_dept > 0 or count_id > 0:
            print("Fixing data...")
            
            # Update dept_code
            if count_dept > 0:
                connection.execute(text("UPDATE hotel_tasks SET dept_code = 'FB' WHERE dept_code = 'F&B'"))
                print("Updated dept_code from 'F&B' to 'FB'")
            
            # Update task_id
            if count_id > 0:
                connection.execute(text("UPDATE hotel_tasks SET task_id = REPLACE(task_id, 'F&B', 'FB') WHERE task_id LIKE '%F&B%'"))
                print("Updated task_id replacing 'F&B' with 'FB'")
                
            connection.commit()
            print("Data fix completed.")
        else:
            print("No 'F&B' data found to fix.")
            
        # Verify
        result = connection.execute(text("SELECT task_id, dept_code FROM hotel_tasks WHERE dept_code = 'FB' LIMIT 5"))
        print("\nSample FB tasks:")
        for row in result:
            print(f"ID: {row[0]}, Dept: {row[1]}")

if __name__ == "__main__":
    fix_fb_data()
