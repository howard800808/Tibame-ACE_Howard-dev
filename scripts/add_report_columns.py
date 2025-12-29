import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine
from sqlalchemy import text

def add_columns():
    db = SessionLocal()
    try:
        print("Adding report columns to emotional_tasks table...")
        
        # List of columns to add
        columns = [
            "ADD COLUMN report_is_finished VARCHAR(10) COMMENT '是否順利完成 (yes/no)'",
            "ADD COLUMN report_details TEXT COMMENT '補充說明'",
            "ADD COLUMN report_has_interaction VARCHAR(10) COMMENT '與顧客有互動嗎 (yes/no)'",
            "ADD COLUMN report_sentiment VARCHAR(20) COMMENT '顧客情緒 (positive/neutral/negative)'",
            "ADD COLUMN report_remarks TEXT COMMENT '備註事項'"
        ]
        
        for col_sql in columns:
            try:
                sql = f"ALTER TABLE emotional_tasks {col_sql};"
                db.execute(text(sql))
                db.commit()
                print(f"Executed: {sql}")
            except Exception as e:
                print(f"Error executing {sql}: {e}")
                db.rollback()
                
        print("Done.")
    finally:
        db.close()

if __name__ == "__main__":
    add_columns()
