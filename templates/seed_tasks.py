"""
templates.seed_tasks.py
12 部門範例任務卡片測試腳本,匯入 MongoDB 資料庫
LineBot Flex Message 任務卡片範例
"""
import pymongo
from datetime import datetime

# 1. 連線設定 (根據你的截圖設定)
# 如果有設定帳號密碼，請修改連線字串，例如: "mongodb://user:password@localhost:27017/"
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["tibame_ace_db"]
collection = db["tasks"]

# 2. 準備資料 (將原本 hotel_task_scenarios.py 的內容轉為字典清單)
# 為了資料庫管理方便，我額外增加了一個 "created_at" 欄位紀錄寫入時間
tasks_data = [
    # --- 1. GS 客務部 ---
    {
        "dept": "GS 客務部", "priority": "P", "room": "Lobby", "guest": "Mr. Smith (VVIP)",
        "title": "感動服務 - 迎賓接待", "content": "總經理特別交代，客人抵達時請列隊歡迎，並準備好擦手巾。",
        "time": "14:00", "remark": "客人行動不便，請備好輪椅。", "status": "PENDING"
    },
    {
        "dept": "GS 客務部", "priority": "F", "room": "Front Desk", "guest": "Group Tour A",
        "title": "團體入住準備", "content": "預先製作 20 份房卡，並分裝早餐券。",
        "time": "16:00", "remark": "領隊姓陳，電話 0912-xxx-xxx。", "status": "PENDING"
    },
    # --- 2. HK 房務部 ---
    {
        "dept": "HK 房務部", "priority": "P", "room": "Room 805", "guest": "Ms. Lee",
        "title": "客訴處理 - 清潔加強", "content": "客人反應浴室有頭髮，請立即重新清潔並更換備品。",
        "time": "NOW", "remark": "完成後請值班經理親自檢查。", "status": "PENDING"
    },
    {
        "dept": "HK 房務部", "priority": "E", "room": "Room 1201", "guest": "Family Wang",
        "title": "加床服務", "content": "協助架設嬰兒床 (Baby Cot) 與消毒鍋。",
        "time": "15:00", "remark": "客人 15:30 進房。", "status": "PENDING"
    },
    {
        "dept": "HK 房務部", "priority": "F", "room": "Floor 10", "guest": "N/A",
        "title": "備品室補貨", "content": "補充 10F 備品室的瓶裝水與沐浴乳庫存。",
        "time": "11:00", "remark": "盤點單請放在桌上。", "status": "PROGRESS"
    },
    # --- 3. CON 門房諮詢 ---
    {
        "dept": "CON 門房諮詢", "priority": "P", "room": "Main Entrance", "guest": "Mr. Tanaka",
        "title": "緊急派車", "content": "客人需緊急前往機場，請安排賓士 S-Class。",
        "time": "NOW", "remark": "客人願意支付急件費用。", "status": "PENDING"
    },
    {
        "dept": "CON 門房諮詢", "priority": "E", "room": "Counter", "guest": "Mrs. Jones",
        "title": "代訂餐廳", "content": "協助預訂鼎泰豐信義店晚餐 (6人)。",
        "time": "17:00", "remark": "需兒童座椅一張。", "status": "PENDING"
    },
    # --- 4. BP 烘焙點心房 ---
    {
        "dept": "BP 烘焙點心房", "priority": "E", "room": "Room 909", "guest": "Ms. Chen",
        "title": "感動服務 - 生日蛋糕", "content": "製作 6 吋草莓鮮奶油蛋糕，寫上 Happy Birthday Amy。",
        "time": "18:00", "remark": "附 18 歲蠟燭。", "status": "PENDING"
    },
    {
        "dept": "BP 烘焙點心房", "priority": "F", "room": "Buffet Kitchen", "guest": "N/A",
        "title": "早餐麵包備料", "content": "準備明日早餐的可頌麵團 200 個。",
        "time": "22:00", "remark": "注意發酵溫度。", "status": "PROGRESS"
    },
    # --- 5. F&B 餐飲 ---
    {
        "dept": "F&B 餐飲", "priority": "P", "room": "Room 1102", "guest": "Mr. Wu",
        "title": "In-Room Dining", "content": "送餐服務：總匯三明治 x1、熱美式 x1。",
        "time": "12:15", "remark": "客人正在開會，請按門鈴後放置門口。", "status": "PENDING"
    },
    {
        "dept": "F&B 餐飲", "priority": "E", "room": "VIP Room A", "guest": "Tech Corp",
        "title": "商務午宴設席", "content": "準備 12 人份中式套餐餐具，需分菜。",
        "time": "11:30", "remark": "全素食者 2 位。", "status": "PENDING"
    },
    # --- 6. CBS 會議宴會 ---
    {
        "dept": "CBS 會議宴會", "priority": "E", "room": "Ballroom B", "guest": "Wedding Lin",
        "title": "婚宴場佈", "content": "確認紅地毯鋪設，與主桌香檳塔架設。",
        "time": "16:30", "remark": "新人彩排時間為 17:00。", "status": "PENDING"
    },
    {
        "dept": "CBS 會議宴會", "priority": "P", "room": "Meeting Room 1", "guest": "Global Inc.",
        "title": "設備故障排除", "content": "投影機無法顯示畫面，請立即支援。",
        "time": "NOW", "remark": "會議中斷中，請帶備用線材。", "status": "PENDING"
    },
    # --- 7. FS 花房 ---
    {
        "dept": "FS 花房", "priority": "F", "room": "Lobby", "guest": "N/A",
        "title": "大廳主花更換", "content": "更換本週主題花藝：使用黃色文心蘭與百合。",
        "time": "05:00", "remark": "需於客人早餐時段前完成。", "status": "PENDING"
    },
    {
        "dept": "FS 花房", "priority": "E", "room": "Room 1001", "guest": "Mr. Chen (VIP)",
        "title": "求婚佈置", "content": "床鋪灑玫瑰花瓣 (愛心形狀)。",
        "time": "14:00", "remark": "花瓣需新鮮，不可有枯邊。", "status": "PENDING"
    },
    # --- 8. LUR 洗衣房與制服室 ---
    {
        "dept": "LUR 洗衣房", "priority": "P", "room": "Room 703", "guest": "Ms. Huang",
        "title": "客衣快洗 (Express)", "content": "客人西裝一套，需乾洗，晚宴前歸還。",
        "time": "17:00", "remark": "承諾 4 小時內交件。", "status": "PROGRESS"
    },
    {
        "dept": "LUR 制服室", "priority": "F", "room": "Uniform Room", "guest": "Staff",
        "title": "制服縫補", "content": "餐飲部背心釦子脫落修補 (共 5 件)。",
        "time": "14:00", "remark": "無", "status": "PENDING"
    },
    # --- 9. GAE 總務工程 ---
    {
        "dept": "GAE 總務工程", "priority": "P", "room": "Room 606", "guest": "Mr. Zhang",
        "title": "冷氣報修", "content": "客人反應冷氣有異音且漏水。",
        "time": "NOW", "remark": "請帶水桶與抹布，避免弄濕地毯。", "status": "PENDING"
    },
    {
        "dept": "GAE 總務工程", "priority": "F", "room": "B2 Parking", "guest": "N/A",
        "title": "燈管更換", "content": "停車場 B 區照明燈管閃爍更換。",
        "time": "10:00", "remark": "需使用升降機。", "status": "PENDING"
    },
    # --- 10. BB 飲料酒吧 ---
    {
        "dept": "BB 飲料酒吧", "priority": "E", "room": "Lounge Bar", "guest": "Mr. X",
        "title": "存酒領取", "content": "客人預約今晚開瓶 (Macallan 18Y)，請先送至包廂。",
        "time": "20:00", "remark": "準備冰球。", "status": "PENDING"
    },
    {
        "dept": "BB 飲料酒吧", "priority": "P", "room": "Pool Bar", "guest": "Event",
        "title": "冰塊緊急支援", "content": "泳池派對冰塊用盡，請支援 5 大包。",
        "time": "NOW", "remark": "使用推車運送。", "status": "PENDING"
    },
    # --- 11. AD 美術設計 ---
    {
        "dept": "AD 美術設計", "priority": "E", "room": "Marketing", "guest": "Hotel",
        "title": "跨年海報設計", "content": "設計 2026 跨年派對主視覺海報。",
        "time": "2025-12-20",
        "remark": "風格需奢華金色系。", "status": "PROGRESS"
    },
    {
        "dept": "AD 美術設計", "priority": "F", "room": "Restaurant", "guest": "N/A",
        "title": "菜單換季更新", "content": "調整義大利餐廳冬季菜單排版。",
        "time": "2025-12-25",
        "remark": "需校對英文說明。", "status": "PENDING"
    },
    # --- 12. LA 休閒活動部 ---
    {
        "dept": "LA 休閒活動部", "priority": "E", "room": "Kids Club", "guest": "Family Lin",
        "title": "DIY 課程準備", "content": "準備下午 3 點的「薑餅屋 DIY」材料包 10 份。",
        "time": "14:30", "remark": "確認糖霜存量。", "status": "PENDING"
    },
    {
        "dept": "LA 休閒活動部", "priority": "P", "room": "Swimming Pool", "guest": "Guest",
        "title": "毛巾補充", "content": "泳池毛巾架已空，請立即補貨。",
        "time": "NOW", "remark": "人潮眾多，請多補 2 車。", "status": "PENDING"
    }
]

# 3. 執行寫入
try:
    # 寫入前先清除舊資料 (選擇性，避免重複執行導致資料重複)
    # collection.delete_many({}) 
    
    # 補上寫入時間戳記
    current_time = datetime.now()
    for task in tasks_data:
        task["created_at"] = current_time

    result = collection.insert_many(tasks_data)
    print(f"成功寫入 {len(result.inserted_ids)} 筆任務資料到 'tasks' 集合中！")
    print("請開啟 MongoDB Compass 點擊 Refresh 查看結果。")

except Exception as e:
    print(f"寫入失敗: {e}")