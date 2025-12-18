import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from app.core.config import settings
from app.models.task_sql import Base

def init_report_table():
    print("Initializing task_reports table...")
    engine = create_engine(settings.DATABASE_URL)
    
    # This will create the table if it doesn't exist
    Base.metadata.create_all(bind=engine)
    print("Table 'task_reports' created successfully.")

if __name__ == "__main__":
    init_report_table()
