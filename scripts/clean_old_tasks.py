import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text
from app.core.config import settings

def clean_old_tasks():
    DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Check count before
        result = connection.execute(text("SELECT COUNT(*) FROM hotel_tasks WHERE task_id LIKE 'T%'"))
        count = result.scalar()
        print(f"Found {count} old tasks (starting with 'T').")
        
        if count > 0:
            print("Deleting old tasks...")
            connection.execute(text("DELETE FROM hotel_tasks WHERE task_id LIKE 'T%'"))
            connection.commit()
            print("Old tasks deleted.")
        else:
            print("No old tasks found.")
            
        # Verify
        result = connection.execute(text("SELECT task_id FROM hotel_tasks LIMIT 10"))
        print("Remaining tasks sample:")
        for row in result:
            print(row[0])

if __name__ == "__main__":
    clean_old_tasks()
