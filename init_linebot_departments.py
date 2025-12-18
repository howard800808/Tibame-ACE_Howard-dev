"""
初始化 12 個部門的 LINE Bot 設定到資料庫
執行此腳本會從 .env 讀取各部門的 ACCESS_TOKEN 和 SECRET，並儲存到 MongoDB
"""
import asyncio
from app.core.config import settings
from app.core.database import connect_to_mongodb, close_mongodb_connection
from app.models.department import Department


# 12 個部門的配置
DEPARTMENTS = [
    {
        "code": "GS",
        "name": "客務部",
        "description": "負責前台接待與客戶服務",
        "access_token_key": "GS_ACCESS_TOKEN",
        "secret_key": "GS_SECRET"
    },
    {
        "code": "HK",
        "name": "房務部",
        "description": "負責客房清潔與整理",
        "access_token_key": "HK_ACCESS_TOKEN",
        "secret_key": "HK_SECRET"
    },
    {
        "code": "CON",
        "name": "門房諮詢",
        "description": "負責門房服務與諮詢",
        "access_token_key": "CON_ACCESS_TOKEN",
        "secret_key": "CON_SECRET"
    },
    {
        "code": "BP",
        "name": "烘焙點心房",
        "description": "負責烘焙與點心製作",
        "access_token_key": "BP_ACCESS_TOKEN",
        "secret_key": "BP_SECRET"
    },
    {
        "code": "FB",
        "name": "餐飲",
        "description": "負責餐飲服務",
        "access_token_key": "FB_ACCESS_TOKEN",
        "secret_key": "FB_SECRET"
    },
    {
        "code": "CBS",
        "name": "會議宴會",
        "description": "負責會議與宴會服務",
        "access_token_key": "CBS_ACCESS_TOKEN",
        "secret_key": "CBS_SECRET"
    },
    {
        "code": "FS",
        "name": "花房",
        "description": "負責花藝佈置與維護",
        "access_token_key": "FS_ACCESS_TOKEN",
        "secret_key": "FS_SECRET"
    },
    {
        "code": "LUR",
        "name": "洗衣房與制服室",
        "description": "負責洗衣與制服管理",
        "access_token_key": "LUR_ACCESS_TOKEN",
        "secret_key": "LUR_SECRET"
    },
    {
        "code": "GAE",
        "name": "總務工程",
        "description": "負責總務與工程維護",
        "access_token_key": "GAE_ACCESS_TOKEN",
        "secret_key": "GAE_SECRET"
    },
    {
        "code": "BB",
        "name": "飲料酒吧",
        "description": "負責飲料與酒吧服務",
        "access_token_key": "BB_ACCESS_TOKEN",
        "secret_key": "BB_SECRET"
    },
    {
        "code": "AD",
        "name": "美術設計",
        "description": "負責美術設計與視覺規劃",
        "access_token_key": "AD_ACCESS_TOKEN",
        "secret_key": "AD_SECRET"
    },
    {
        "code": "LA",
        "name": "休閒活動部",
        "description": "負責休閒活動規劃與執行",
        "access_token_key": "LA_ACCESS_TOKEN",
        "secret_key": "LA_SECRET"
    }
]


async def init_departments():
    """初始化部門資料"""
    await connect_to_mongodb()
    
    print("\n開始初始化 12 個部門的 LINE Bot 設定...")
    print("=" * 60)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for dept_config in DEPARTMENTS:
        code = dept_config["code"]
        name = dept_config["name"]
        
        # 從 settings 取得對應的 token 和 secret
        access_token = getattr(settings, dept_config["access_token_key"], None)
        secret = getattr(settings, dept_config["secret_key"], None)
        
        if not access_token or not secret:
            print(f"⚠️  {code} - {name}: 未設定 ACCESS_TOKEN 或 SECRET，跳過")
            skip_count += 1
            continue
        
        try:
            # 檢查是否已存在
            existing = await Department.find_one({"code": code})
            
            if existing:
                # 更新現有部門
                existing.name = name
                existing.description = dept_config["description"]
                existing.access_token = access_token
                existing.channel_secret = secret
                existing.is_active = True
                await existing.save()
                print(f"✓ {code} - {name}: 更新成功")
            else:
                # 建立新部門
                department = Department(
                    code=code,
                    name=name,
                    description=dept_config["description"],
                    access_token=access_token,
                    channel_secret=secret,
                    is_active=True
                )
                await department.insert()
                print(f"✓ {code} - {name}: 建立成功")
            
            success_count += 1
            
        except Exception as e:
            print(f"✗ {code} - {name}: 失敗 - {str(e)}")
            error_count += 1
    
    print("=" * 60)
    print(f"\n初始化完成:")
    print(f"  成功: {success_count}")
    print(f"  跳過: {skip_count}")
    print(f"  失敗: {error_count}")
    print(f"  總計: {len(DEPARTMENTS)}\n")
    
    await close_mongodb_connection()


if __name__ == "__main__":
    asyncio.run(init_departments())
