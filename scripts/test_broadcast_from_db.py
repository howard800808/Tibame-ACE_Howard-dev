import asyncio
import sys
import os
import json
from datetime import datetime

# 將專案根目錄加入路徑
sys.path.append(os.getcwd())

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from linebot.models import FlexSendMessage

# 引入模型與服務
from app.models.department import Department
from app.models.task import Task
from app.services.linebot_service import linebot_service

# 設定資料庫連線
MONGO_URI = "mongodb://localhost:27017/tibame_ace_db"

# 12 個部門列表
DEPARTMENTS = [
    {"code": "GS", "name": "客務部"},
    {"code": "HK", "name": "房務部"},
    {"code": "CON", "name": "門房諮詢"},
    {"code": "BP", "name": "烘焙點心房"},
    {"code": "FB", "name": "餐飲"},
    {"code": "CBS", "name": "會議宴會"},
    {"code": "FS", "name": "花房"},
    {"code": "LUR", "name": "洗衣房與制服室"},
    {"code": "GAE", "name": "總務工程"},
    {"code": "BB", "name": "飲料酒吧"},
    {"code": "AD", "name": "美術設計"},
    {"code": "LA", "name": "休閒活動部"}
]

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(database=client.get_default_database(), document_models=[Department, Task])
    print("[Init] 資料庫連線成功")

async def mock_setup_department(dept_code):
    """
    模擬初始化部門 Bot
    攔截 broadcast 方法，只印出資訊而不實際發送
    """
    class MockLineBotApi:
        def reply_message(self, reply_token, messages):
            pass

        def push_message(self, to, messages):
            pass

        def broadcast(self, messages):
            # 這裡攔截廣播內容
            if isinstance(messages, FlexSendMessage):
                print(f"    [Mock Broadcast] 廣播 Flex 訊息: {messages.alt_text}")
                # print(json.dumps(messages.contents, ensure_ascii=False, indent=2))
            else:
                print(f"    [Mock Broadcast] 廣播文字訊息: {messages.text}")

    # 注入 Mock API
    linebot_service.department_bots[dept_code] = (MockLineBotApi(), None)
    return True

async def test_broadcast_from_db():
    await init_db()
    
    # [重要] 初始化真實的 LINE Bot 連線
    # 這會從資料庫讀取 Token。如果 Token 是 "test_token" 或無效，會顯示錯誤。
    print("[Init] 正在初始化真實 LINE Bot 連線...")
    await linebot_service.initialize_departments()
    
    print(f"\n{'='*50}")
    print(f"開始執行 12 部門廣播測試 (真實發送模式)")
    print(f"注意：這會發送訊息給所有好友！")
    print(f"{'='*50}\n")

    for dept_info in DEPARTMENTS:
        code = dept_info["code"]
        name = dept_info["name"]
        
        print(f"[{code} {name}] 檢查中...")

        # [已關閉模擬] 註解掉這行以啟用真實發送
        # await mock_setup_department(code)

        # 2. 從資料庫找最新的一筆任務
        task = await Task.find({"department_code": code}).sort("-created_at").first_or_none()
        
        if not task:
            print(f"    [Skip] 資料庫中沒有 {name} 的任務，跳過測試。")
            continue

        print(f"    [Found] 找到任務: {task.title} (ID: {task.id})")

        # 3. 產生 Flex Message 內容
        flex_contents = linebot_service.create_task_flex_card(task)
        
        # 4. 執行廣播測試
        # 注意：這裡呼叫的是 service 的方法，service 會去用我們 Mock 的 API
        success = await linebot_service.broadcast_flex_to_department(
            department_code=code,
            alt_text=f"廣播任務: {task.title}",
            flex_contents=flex_contents
        )

        if success:
            print(f"    [Success] 廣播測試成功")
            print(f"    [JSON] Flex 內容預覽:")
            print(json.dumps(flex_contents, ensure_ascii=False, indent=2))
        else:
            print(f"    [Fail] 廣播測試失敗")
        
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(test_broadcast_from_db())
