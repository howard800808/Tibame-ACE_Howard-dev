import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    BroadcastRequest,
    TextMessage,
    ApiException
)

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.department import Department

def test_broadcast_real():
    # Configuration
    DB_HOST = '192.168.50.101'
    DB_PORT = 3306
    DB_USER = 'ace_web'
    DB_PASS = 'Ace251201!'
    DB_NAME = 'ace'
    
    DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    print(f'Connecting to database at {DB_HOST}...')
    
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Query all departments
        departments = db.query(Department).all()
        
        print(f'Found {len(departments)} departments.')
        print('-' * 60)
        
        message_text = '這是一則測試廣播訊息 from ace.89.com.tw (Real Send v3)'
        
        for dept in departments:
            print(f'[{dept.code}] {dept.name_zh}')
            
            if not dept.channel_access_token:
                print('  -> Error: No Access Token')
                continue
                
            try:
                configuration = Configuration(access_token=dept.channel_access_token)
                with ApiClient(configuration) as api_client:
                    line_bot_api = MessagingApi(api_client)
                    line_bot_api.broadcast(
                        broadcast_request=BroadcastRequest(
                            messages=[TextMessage(text=message_text)]
                        )
                    )
                print('  -> Success: Broadcast sent')
            except ApiException as e:
                print(f'  -> Error: {e.status} {e.reason} {e.body}')
            except Exception as e:
                print(f'  -> Error: {e}')
            
            print('-' * 30)
            
        print('Broadcast test completed.')
        
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if 'db' in locals():
            db.close()

if __name__ == '__main__':
    test_broadcast_real()
