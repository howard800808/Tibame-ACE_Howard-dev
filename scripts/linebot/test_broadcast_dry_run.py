import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.department import Department

def test_broadcast_dry_run():
    # Configuration
    DB_HOST = "192.168.50.101"
    DB_PORT = 3306
    DB_USER = "ace_web"
    DB_PASS = "Ace251201!"
    DB_NAME = "ace"
    
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    print(f"Connecting to database at {DB_HOST}...")
    
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Query all departments
        departments = db.query(Department).all()
        
        print(f"Found {len(departments)} departments.")
        print("-" * 60)
        print(f"{'Code':<10} {'Name':<20} {'Status'}")
        print("-" * 60)
        
        message = "這是一則測試廣播訊息 from ace.89.com.tw  (Dry Run)"
        
        for dept in departments:
            print(f"{dept.code:<10} {dept.name_zh:<20} [DRY RUN] Sending message...")
            print(f"  -> Token: {dept.channel_access_token[:20]}...")
            print(f"  -> Message: {message}")
            print("  -> Result: Skipped (Dry Run Mode)")
            print("-" * 30)
            
        print("Test completed. No messages were actually sent.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    test_broadcast_dry_run()
