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
from app.models.task import Task, TaskStatus
from app.services.linebot_service import linebot_service
from app.controllers.linebot_controller import LineBotController

# 設定資料庫連線
MONGO_URI = "mongodb://localhost:27017/tibame_ace_db"

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(database=client.get_default_database(), document_models=[Department, Task])
    print("[Init] 資料庫連線成功")

async def mock_setup_department(dept_code):
    """模擬初始化部門 Bot，攔截 reply_message"""
    class MockLineBotApi:
        def reply_message(self, reply_token, messages):
            # 處理單一訊息或訊息列表
            if not isinstance(messages, list):
                messages = [messages]

            for msg in messages:
                if isinstance(msg, FlexSendMessage):
                    print(f"\n[Mock Reply] 收到 Flex 回覆 (Token: {reply_token})")
                    print(f"Alt Text: {msg.alt_text}")
                    
                    # 嘗試將 contents 轉為字串檢查
                    # 注意：SDK 可能會將 dict 轉為 BubbleContainer 物件
                    try:
                        if hasattr(msg.contents, 'as_json_dict'):
                             contents_str = json.dumps(msg.contents.as_json_dict(), ensure_ascii=False)
                        elif isinstance(msg.contents, dict):
                             contents_str = json.dumps(msg.contents, ensure_ascii=False)
                        else:
                             contents_str = str(msg.contents)
                             
                        if "任務執行中" in contents_str:
                            print("[Check] ✅ 卡片狀態已更新為「任務執行中」")
                        elif "未執行" in contents_str:
                            print("[Check] ❌ 卡片狀態仍為「未執行」")
                        
                        if "已完成任務 (Complete)" in contents_str:
                            print("[Check] ✅ 按鈕已更新為「已完成任務」")
                    except Exception as e:
                        print(f"[Check] 檢查內容時發生錯誤: {e}")
                        
                else:
                    # 假設是 TextSendMessage
                    text = getattr(msg, 'text', 'Unknown Message Type')
                    print(f"[Mock Reply] 收到文字回覆: {text}")

        def push_message(self, to, messages):
            pass # 忽略推播

        def broadcast(self, messages):
            pass

    # 注入 Mock API
    linebot_service.department_bots[dept_code] = (MockLineBotApi(), None)
    return True

async def test_postback_accept():
    await init_db()
    
    dept_code = "GS"
    print(f"\n{'='*50}")
    print(f"開始測試「接受任務」按鈕觸發流程 (部門: {dept_code})")
    print(f"{'='*50}\n")

    # 1. 準備 Mock 環境
    await mock_setup_department(dept_code)

    # 2. 建立一個測試任務 (狀態: PENDING)
    task = Task(
        department_code=dept_code,
        department_name="客務部",
        line_user_id="U_TEST_USER",
        title="測試接受任務",
        description="請點擊接受按鈕測試狀態更新",
        status=TaskStatus.PENDING,
        priority="medium"
    )
    await task.insert()
    print(f"[Setup] 建立測試任務 ID: {task.id} (Status: {task.status})")

    # 3. 模擬 Postback 事件
    # 這是 LINE Server 傳過來的 JSON 結構
    postback_event = {
        "type": "postback",
        "replyToken": "dummy_reply_token",
        "source": {"userId": "U_TEST_USER", "type": "user"},
        "postback": {
            "data": f"action=task&op=accept&dept=客務部&room=Lobby&id={task.id}"
        }
    }

    print(f"[Action] 模擬使用者點擊「接受任務」...")
    
    # 4. 呼叫 Controller 處理事件
    controller = LineBotController()
    # 直接呼叫 private method _handle_postback_event 進行測試
    await controller._handle_postback_event(dept_code, postback_event)

    # 5. 驗證資料庫狀態
    updated_task = await Task.get(task.id)
    print(f"\n[Verify] 資料庫任務狀態: {updated_task.status}")
    
    if updated_task.status == TaskStatus.IN_PROGRESS:
        print("[Result] ✅ 測試成功！任務狀態已更新為 IN_PROGRESS")
    else:
        print("[Result] ❌ 測試失敗！任務狀態未更新")

    # 清理測試資料
    await task.delete()
    print("[Cleanup] 測試任務已刪除")

if __name__ == "__main__":
    asyncio.run(test_postback_accept())
