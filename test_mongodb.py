"""
MongoDB 連接測試腳本
執行此腳本以測試 MongoDB 連接是否正常
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


async def test_mongodb_connection():
    """測試 MongoDB 連接"""
    print("=" * 60)
    print("開始測試 MongoDB 連接...")
    print("=" * 60)
    
    try:
        # 建立連接
        print(f"\n1. 正在連接到: {settings.MONGODB_URL}")
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        
        # 測試連接
        print("2. 測試連接...")
        await client.admin.command('ping')
        print("   ✓ 連接成功！")
        
        # 列出所有資料庫
        print("\n3. 列出所有資料庫:")
        db_list = await client.list_database_names()
        for db_name in db_list:
            print(f"   - {db_name}")
        
        # 取得目標資料庫
        print(f"\n4. 使用資料庫: {settings.MONGODB_DB_NAME}")
        db = client[settings.MONGODB_DB_NAME]
        
        # 列出所有集合
        print("5. 列出所有集合 (collections):")
        collections = await db.list_collection_names()
        if collections:
            for coll_name in collections:
                print(f"   - {coll_name}")
        else:
            print("   (尚無集合)")
        
        # 測試寫入
        print("\n6. 測試寫入資料...")
        test_collection = db["test_collection"]
        result = await test_collection.insert_one({"test": "Hello MongoDB!", "type": "connection_test"})
        print(f"   ✓ 成功插入資料，ID: {result.inserted_id}")
        
        # 測試讀取
        print("7. 測試讀取資料...")
        doc = await test_collection.find_one({"_id": result.inserted_id})
        print(f"   ✓ 讀取成功: {doc}")
        
        # 清理測試資料
        print("8. 清理測試資料...")
        await test_collection.delete_one({"_id": result.inserted_id})
        print("   ✓ 測試資料已清除")
        
        # 關閉連接
        client.close()
        
        print("\n" + "=" * 60)
        print("✓ 所有測試通過！MongoDB 連接正常")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ 連接失敗: {str(e)}")
        print("=" * 60)
        print("\n請確認:")
        print("1. MongoDB 服務是否已啟動")
        print("2. MONGODB_URL 設定是否正確")
        print("3. 網路連接是否正常")
        print("\n對於本地開發，請確保 MongoDB 正在運行：")
        print("   - Windows: 啟動 MongoDB 服務")
        print("   - macOS: brew services start mongodb-community")
        print("   - Linux: sudo systemctl start mongod")
        print("   - Docker: docker run -d -p 27017:27017 mongo:latest")


if __name__ == "__main__":
    asyncio.run(test_mongodb_connection())
