import sys
import os

# Add the project root to the python path
sys.path.append(os.getcwd())

from sqlalchemy import create_engine, text
from app.core.config import settings

def check_tasks():
    # Create a direct connection to MySQL using SQLAlchemy
    # Use the DATABASE_URL from settings
    DATABASE_URL = settings.DATABASE_URL
    
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Check for any tasks that don't start with 'T' followed by digits, or just list all
        result = connection.execute(text("SELECT id, task_id, title, dept_code FROM hotel_tasks ORDER BY id DESC LIMIT 20"))
        print(f"{'ID':<5} {'Task ID':<15} {'Dept Code':<10} {'Title'}")
        print("-" * 60)
        for row in result:
            print(f"{row.id:<5} {row.task_id:<15} {row.dept_code:<10} {row.title}")

if __name__ == "__main__":
    check_tasks()
