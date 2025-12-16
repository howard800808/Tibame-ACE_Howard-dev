import asyncio
import sys
import os
import json
from motor.motor_asyncio import AsyncIOMotorClient

# 將專案根目錄加入路徑
sys.path.append(os.getcwd())

# 引入服務與 Flex Template 函式
from app.services.linebot_service import linebot_service
from templates.pull_task_linebot.flex_templates import create_hotel_task_card

from beanie import init_beanie
from app.models.department import Department
from app.models.task import Task

# 設定資料庫連線
MONGO_URI = "mongodb://localhost:27017/tibame_ace_db"

async def test_broadcast_templates():
    # 0. 初始化 Beanie (LineBotService 需要用到 Department Model)
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(database=client.get_default_database(), document_models=[Department, Task])

    # 1. 初始化 LINE Bot 連線
    print("[Init] 正在初始化真實 LINE Bot 連線...")
    await linebot_service.initialize_departments()
    
    # 2. 連線到 MongoDB (使用 Motor 讀取原始文件)
    # client = AsyncIOMotorClient(MONGO_URI) # 已經在上面初始化過了
    db = client.get_default_database()
    collection = db["tasks"]
    
    print(f"\n{'='*50}")
    print(f"開始執行 12 部門廣播測試 (使用資料庫中的範本)")
    print(f"注意：這會發送訊息給所有好友！")
    print(f"{'='*50}\n")

    # 3. 讀取所有任務範本
    cursor = collection.find({})
    tasks = await cursor.to_list(length=1000)
    
    if not tasks:
        print("[Error] 資料庫中沒有找到任何任務範本！")
        return

    print(f"[Info] 總共找到 {len(tasks)} 筆任務範本")

    # 4. 依部門分組並發送 Carousel (左右滑動卡片)
    dept_tasks = {}
    for task_doc in tasks:
        dept_str = task_doc.get("dept", "")
        if not dept_str:
            continue
        
        # 處理 F&B 特殊情況 (資料庫是 F&B，但系統代碼是 FB)
        if "F&B" in dept_str:
             dept_code = "FB"
        else:
             dept_code = dept_str.split(" ")[0]

        if dept_code not in dept_tasks:
            dept_tasks[dept_code] = []
        dept_tasks[dept_code].append(task_doc)

    # 5. 逐一部門發送 Carousel
    for dept_code, task_list in dept_tasks.items():
        print(f"[{dept_code}] 準備廣播 {len(task_list)} 則任務 (Carousel)...")
        
        bubbles = []
        for task_doc in task_list:
             try:
                bubble = create_hotel_task_card(
                    dept=task_doc.get("dept", ""),
                    priority=task_doc.get("priority", "F"),
                    room=task_doc.get("room", "N/A"),
                    guest=task_doc.get("guest", "Guest"),
                    title=task_doc.get("title", "No Title"),
                    content=task_doc.get("content", ""),
                    time=task_doc.get("time", ""),
                    remark=task_doc.get("remark", ""),
                    status=task_doc.get("status", "PENDING"),
                    task_id=str(task_doc.get("_id"))
                )
                bubbles.append(bubble)
             except Exception as e:
                print(f"    [Error] 產生卡片失敗: {e}")

        if not bubbles:
            continue

        # 建立 Carousel Container (這就是左右滑動的關鍵)
        carousel_content = {
            "type": "carousel",
            "contents": bubbles
        }

        # 發送廣播
        try:
            success = await linebot_service.broadcast_flex_to_department(
                department_code=dept_code,
                alt_text=f"收到 {len(bubbles)} 則新任務",
                flex_contents=carousel_content
            )
            
            if success:
                print(f"    [Success] 發送成功")
            else:
                print(f"    [Fail] 發送失敗 (可能該部門 Bot 未初始化或 Token 無效)")
        except Exception as e:
            print(f"    [Error] 發送失敗: {e}")
        
        # 稍微停頓避免觸發 Rate Limit
        await asyncio.sleep(0.5)

    print(f"\n{'='*50}")
    print("測試完成")

if __name__ == "__main__":
    asyncio.run(test_broadcast_templates())
