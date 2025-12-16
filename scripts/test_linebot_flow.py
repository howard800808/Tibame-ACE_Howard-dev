import asyncio
import sys
import os
from datetime import datetime

# 將專案根目錄加入路徑，確保能 import app 模組
sys.path.append(os.getcwd())

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from linebot import LineBotApi

# 引入你的模型與服務
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

async def ensure_department_exists(dept_info):
    """確保部門存在於資料庫中，若不存在則建立測試用資料"""
    dept = await Department.find_one({"code": dept_info["code"]})
    if not dept:
        print(f"[Setup] 建立測試部門: {dept_info['name']} ({dept_info['code']})")
        dept = Department(
            code=dept_info["code"],
            name=dept_info["name"],
            description=f"測試用{dept_info['name']}",
            access_token="test_token",
            channel_secret="test_secret",
            is_active=True
        )
        await dept.insert()
    return dept

async def mock_setup_department(dept_code):
    """模擬初始化部門 Bot"""
    # 這裡我們直接呼叫 service 的初始化，因為我們已經確保部門存在
    # 由於 Token 是假的，Service 會報錯但我們在 Service 中有 try-except
    # 為了讓測試順利，我們手動注入一個假的 Bot API 到 service 中
    # 這樣 service.get_bot_api 就不會回傳 None
    
    # 建立一個 Mock 物件來攔截 reply_message
    class MockLineBotApi:
        def reply_message(self, reply_token, messages):
            if reply_token == "invalid_token":
                # 模擬真實 API 行為
                from linebot.exceptions import LineBotApiError
                from linebot.models import Error, ErrorDetail
                error = Error(message="Invalid reply token", details=[ErrorDetail(message="Invalid reply token")])
                raise LineBotApiError(status_code=400, message="Invalid reply token", error=error)
            pass # 成功

        def push_message(self, to, messages):
            pass

        def broadcast(self, messages):
            pass

    # 注入 Mock API
    linebot_service.department_bots[dept_code] = (MockLineBotApi(), None)
    return True

async def test_department_flow(dept_info):
    dept_code = dept_info["code"]
    dept_name = dept_info["name"]
    print(f"\n{'='*20} 測試部門: {dept_name} ({dept_code}) {'='*20}")

    # 1. 確保部門存在
    await ensure_department_exists(dept_info)
    
    # 2. Mock Bot Setup
    await mock_setup_department(dept_code)

    # 3. 模擬接收文字訊息 (建立任務)
    user_id = f"U_TEST_{dept_code}"
    reply_token = "dummy_token_for_test"
    message_text = f"緊急 {dept_name}測試任務\n這是由自動化腳本產生的測試任務"
    
    print(f"模擬發送訊息: {message_text.splitlines()[0]}...")
    
    task = await linebot_service.handle_text_message(
        department_code=dept_code,
        user_id=user_id,
        user_name="自動化測試員",
        message_text=message_text,
        message_id=f"msg_{dept_code}_{int(datetime.utcnow().timestamp())}",
        reply_token=reply_token
    )

    if task:
        print(f"[Success] 任務已建立! ID: {task.id}")
    else:
        print(f"[Fail] 任務建立失敗 - {dept_name}")
        return

    # 4. 模擬任務回報 (Postback)
    print(f"模擬任務回報流程...")
    steps = [
        (1, "已收到通知"),
        (2, "前往現場中"),
        (3, "處理中"),
        (4, "處理完畢"),
        (5, "回報完成")
    ]

    for step, answer in steps:
        await linebot_service.record_report_answer(
            task_id=str(task.id),
            step=step,
            answer=answer
        )
        # 不用 sleep 太久，這是自動化測試
        await asyncio.sleep(0.1)

    # 5. 驗證結果
    final_task = await Task.get(task.id)
    if final_task.report_completed:
        print(f"[Pass] {dept_name} 回報流程驗證成功 (5步驟完成)")
    else:
        print(f"[Fail] {dept_name} 回報流程未完成")

async def main():
    await init_db()
    
    print(f"開始掃描 12 個部門的任務與回報流程...")
    
    for dept in DEPARTMENTS:
        await test_department_flow(dept)
        
    print(f"\n{'='*50}")
    print("所有部門測試完成。請檢查上方輸出的 JSON 是否符合預期。")

if __name__ == "__main__":
    asyncio.run(main())
