import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from sqlalchemy import text
from app.core.database import engine

def fix_schema():
    with engine.connect() as connection:
        print("Altering table emotion_analysis...")
        try:
            # Modify columns to support larger data
            # emotions_json -> TEXT
            # face_details_json -> TEXT
            # analysis_result_json -> LONGTEXT (to be safe)
            
            connection.execute(text("ALTER TABLE emotion_analysis MODIFY COLUMN emotions_json TEXT"))
            print("Modified emotions_json to TEXT")
            
            connection.execute(text("ALTER TABLE emotion_analysis MODIFY COLUMN face_details_json TEXT"))
            print("Modified face_details_json to TEXT")
            
            connection.execute(text("ALTER TABLE emotion_analysis MODIFY COLUMN analysis_result_json LONGTEXT"))
            print("Modified analysis_result_json to LONGTEXT")
            
            connection.commit()
            print("Schema updated successfully!")
        except Exception as e:
            print(f"Error updating schema: {e}")

if __name__ == "__main__":
    fix_schema()
