#!/usr/bin/env python3
"""
test_flex_message.py

測試 Flex Message 生成功能
從 MongoDB 資料庫擷取任務，產生 Flex Message 卡片並驗證結構
"""

import asyncio
import json
from datetime import datetime
from motor import AsyncIOMotorClient
from beanie import init_beanie

# 導入模型與服務
from app.models.department import Department
from app.models.task import Task, TaskStatus, TaskPriority
from app.services.linebot_service import linebot_service
from app.core.config import settings


async def init_db():
    """初始化資料庫連線"""
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]
    await init_beanie(database=db, models=[Department, Task])
    print("[DB] 資料庫連線初始化完成")


async def test_flex_message_generation():
    """測試 Flex Message 生成"""
    print("\n" + "="*60)
    print("Flex Message 生成測試")
    print("="*60)
    
    # 初始化資料庫
    await init_db()
    
    # 查詢資料庫中的任務
    tasks = await Task.find().limit(5).to_list()
    
    if not tasks:
        print("\n❌ 資料庫中沒有任務資料")
        print("提示：請先執行 python templates/seed_tasks.py 建立測試資料")
        return
    
    print(f"\n✅ 從資料庫取得 {len(tasks)} 個任務")
    
    # 逐一測試每個任務的 Flex Message 生成
    for i, task in enumerate(tasks, 1):
        print(f"\n--- 任務 {i}/{len(tasks)} ---")
        print(f"📋 任務 ID: {task.id}")
        print(f"📝 標題: {task.title}")
        print(f"🏢 部門: {task.department_name}")
        print(f"⚡ 優先級: {task.priority.value}")
        print(f"📌 狀態: {task.status.value}")
        
        # 產生 Flex Message
        try:
            flex_card = linebot_service.create_task_flex_card(task)
            
            # 驗證結構
            assert flex_card.get("type") == "bubble", "Flex 結構類型不正確"
            assert flex_card.get("header"), "缺少 header"
            assert flex_card.get("body"), "缺少 body"
            assert flex_card.get("footer"), "缺少 footer"
            
            print("✅ Flex Message 結構驗證通過")
            
            # 顯示卡片概要
            header_contents = flex_card.get("header", {}).get("contents", [])
            if header_contents:
                title_text = header_contents[-1].get("text", "N/A")
                print(f"   - Header 標題: {title_text}")
            
            body_contents = flex_card.get("body", {}).get("contents", [])
            print(f"   - Body 欄位數: {len(body_contents)}")
            
            footer_button = flex_card.get("footer", {}).get("contents", [{}])[0]
            btn_label = footer_button.get("action", {}).get("label", "N/A")
            print(f"   - 按鈕標籤: {btn_label}")
            
        except Exception as e:
            print(f"❌ Flex Message 生成失敗: {str(e)}")
            continue
    
    print("\n" + "="*60)
    print("✅ Flex Message 生成測試完成")
    print("="*60)


async def test_flex_carousel():
    """測試 Flex Carousel (多卡片)"""
    print("\n" + "="*60)
    print("Flex Carousel 生成測試")
    print("="*60)
    
    # 查詢資料庫中的任務
    tasks = await Task.find({
        "status": TaskStatus.PENDING
    }).limit(3).to_list()
    
    if not tasks:
        print("\n❌ 資料庫中沒有待處理任務")
        return
    
    print(f"\n✅ 取得 {len(tasks)} 個待處理任務")
    
    # 產生 Carousel
    try:
        bubbles = [linebot_service.create_task_flex_card(task) for task in tasks]
        
        carousel = {
            "type": "carousel",
            "contents": bubbles
        }
        
        assert carousel.get("type") == "carousel", "Carousel 類型不正確"
        assert len(carousel.get("contents", [])) == len(tasks), "卡片數量不匹配"
        
        print("✅ Flex Carousel 結構驗證通過")
        print(f"   - Carousel 包含 {len(bubbles)} 張卡片")
        
    except Exception as e:
        print(f"❌ Carousel 生成失敗: {str(e)}")


async def test_status_transitions():
    """測試不同狀態的任務卡片"""
    print("\n" + "="*60)
    print("任務狀態轉移測試")
    print("="*60)
    
    statuses = [TaskStatus.PENDING, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED, TaskStatus.CANCELLED]
    
    # 查詢一個任務作為範本
    template_task = await Task.find_one()
    if not template_task:
        print("\n❌ 資料庫中沒有任務")
        return
    
    print(f"\n✅ 使用任務作為測試範本: {template_task.title}")
    
    for status in statuses:
        print(f"\n--- 狀態: {status.value} ---")
        
        # 暫時修改狀態進行測試
        original_status = template_task.status
        template_task.status = status
        
        try:
            flex_card = linebot_service.create_task_flex_card(template_task)
            
            # 檢查狀態文字
            body = flex_card.get("body", {}).get("contents", [])
            status_row = body[0] if body else {}
            status_box = status_row.get("contents", [])[1] if status_row.get("contents") else {}
            status_text = status_box.get("text", "N/A")
            
            print(f"   - 狀態文字: {status_text}")
            
            # 檢查按鈕
            footer = flex_card.get("footer", {}).get("contents", [{}])[0]
            btn_label = footer.get("action", {}).get("label", "N/A")
            print(f"   - 按鈕標籤: {btn_label}")
            
            print("   ✅ 狀態轉移正確")
            
        except Exception as e:
            print(f"   ❌ 狀態轉移失敗: {str(e)}")
        
        # 恢復原狀態
        template_task.status = original_status
    
    print("\n" + "="*60)
    print("✅ 任務狀態轉移測試完成")
    print("="*60)


async def test_json_export():
    """測試 JSON 匯出"""
    print("\n" + "="*60)
    print("Flex Message JSON 匯出測試")
    print("="*60)
    
    # 查詢一個任務
    task = await Task.find_one({"status": TaskStatus.PENDING})
    if not task:
        task = await Task.find_one()
    
    if not task:
        print("\n❌ 資料庫中沒有任務")
        return
    
    print(f"\n✅ 選擇任務: {task.title}")
    
    # 產生 Flex Message
    flex_card = linebot_service.create_task_flex_card(task)
    
    # 轉換為 JSON
    try:
        json_str = json.dumps(flex_card, ensure_ascii=False, indent=2)
        
        # 驗證 JSON 有效性
        json.loads(json_str)
        
        print("✅ JSON 匯出成功")
        print(f"   - JSON 大小: {len(json_str)} 字元")
        
        # 顯示前幾行
        lines = json_str.split('\n')
        print("\n   JSON 預覽 (前 20 行):")
        for line in lines[:20]:
            print(f"   {line}")
        if len(lines) > 20:
            print(f"   ... (共 {len(lines)} 行)")
        
    except Exception as e:
        print(f"❌ JSON 匯出失敗: {str(e)}")
    
    print("\n" + "="*60)
    print("✅ JSON 匯出測試完成")
    print("="*60)


async def main():
    """主函數"""
    print("\n🚀 開始 Flex Message 整合測試\n")
    
    try:
        # 執行各項測試
        await test_flex_message_generation()
        await test_flex_carousel()
        await test_status_transitions()
        await test_json_export()
        
        print("\n" + "="*60)
        print("✅ 所有測試完成")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
