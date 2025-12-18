"""
可重複使用的任務範例資料，用來批次寫入資料庫或產生 Flex 卡片。
"""
from templates.pull_task_linebot.flex_templates import create_hotel_task_card

# 單筆資料結構
# {
#     "department_code": "GS",
#     "department_name": "GS 客務部",
#     "priority_code": "P|E|F",
#     "room": "Room 805",
#     "guest": "Mr. Smith",
#     "title": "...",
#     "content": "...",
#     "time": "14:00",
#     "remark": "...",
#     "status": "PENDING|PROGRESS"
# }

SEED_TASKS = [
    {"department_code": "GS", "department_name": "GS 客務部", "priority_code": "P", "room": "Lobby", "guest": "Mr. Smith (VVIP)", "title": "感動服務 - 迎賓接待", "content": "總經理特別交代，客人抵達時請列隊歡迎，並準備好擦手巾。", "time": "14:00", "remark": "客人行動不便，請備好輪椅。", "status": "PENDING"},
    {"department_code": "GS", "department_name": "GS 客務部", "priority_code": "F", "room": "Front Desk", "guest": "Group Tour A", "title": "團體入住準備", "content": "預先製作 20 份房卡，並分裝早餐券。", "time": "16:00", "remark": "領隊姓陳，電話 0912-xxx-xxx。", "status": "PENDING"},
    {"department_code": "HK", "department_name": "HK 房務部", "priority_code": "P", "room": "Room 805", "guest": "Ms. Lee", "title": "客訴處理 - 清潔加強", "content": "客人反應浴室有頭髮，請立即重新清潔並更換備品。", "time": "NOW", "remark": "完成後請值班經理親自檢查。", "status": "PENDING"},
    {"department_code": "HK", "department_name": "HK 房務部", "priority_code": "E", "room": "Room 1201", "guest": "Family Wang", "title": "加床服務", "content": "協助架設嬰兒床 (Baby Cot) 與消毒鍋。", "time": "15:00", "remark": "客人 15:30 進房。", "status": "PENDING"},
    {"department_code": "HK", "department_name": "HK 房務部", "priority_code": "F", "room": "Floor 10", "guest": "N/A", "title": "備品室補貨", "content": "補充 10F 備品室的瓶裝水與沐浴乳庫存。", "time": "11:00", "remark": "盤點單請放在桌上。", "status": "PROGRESS"},
    {"department_code": "CON", "department_name": "CON 門房諮詢", "priority_code": "P", "room": "Main Entrance", "guest": "Mr. Tanaka", "title": "緊急派車", "content": "客人需緊急前往機場，請安排賓士 S-Class。", "time": "NOW", "remark": "客人願意支付急件費用。", "status": "PENDING"},
    {"department_code": "CON", "department_name": "CON 門房諮詢", "priority_code": "E", "room": "Counter", "guest": "Mrs. Jones", "title": "代訂餐廳", "content": "協助預訂鼎泰豐信義店晚餐 (6人)。", "time": "17:00", "remark": "需兒童座椅一張。", "status": "PENDING"},
    {"department_code": "BP", "department_name": "BP 烘焙點心房", "priority_code": "E", "room": "Room 909", "guest": "Ms. Chen", "title": "感動服務 - 生日蛋糕", "content": "製作 6 吋草莓鮮奶油蛋糕，寫上 Happy Birthday Amy。", "time": "18:00", "remark": "附 18 歲蠟燭。", "status": "PENDING"},
    {"department_code": "BP", "department_name": "BP 烘焙點心房", "priority_code": "F", "room": "Buffet Kitchen", "guest": "N/A", "title": "早餐麵包備料", "content": "準備明日早餐的可頌麵團 200 個。", "time": "22:00", "remark": "注意發酵溫度。", "status": "PROGRESS"},
    {"department_code": "FB", "department_name": "F&B 餐飲", "priority_code": "P", "room": "Room 1102", "guest": "Mr. Wu", "title": "In-Room Dining", "content": "送餐服務：總匯三明治 x1、熱美式 x1。", "time": "12:15", "remark": "客人正在開會，請按門鈴後放置門口。", "status": "PENDING"},
    {"department_code": "FB", "department_name": "F&B 餐飲", "priority_code": "E", "room": "VIP Room A", "guest": "Tech Corp", "title": "商務午宴設席", "content": "準備 12 人份中式套餐餐具，需分菜。", "time": "11:30", "remark": "全素食者 2 位。", "status": "PENDING"},
    {"department_code": "CBS", "department_name": "CBS 會議宴會", "priority_code": "E", "room": "Ballroom B", "guest": "Wedding Lin", "title": "婚宴場佈", "content": "確認紅地毯鋪設，與主桌香檳塔架設。", "time": "16:30", "remark": "新人彩排時間為 17:00。", "status": "PENDING"},
    {"department_code": "CBS", "department_name": "CBS 會議宴會", "priority_code": "P", "room": "Meeting Room 1", "guest": "Global Inc.", "title": "設備故障排除", "content": "投影機無法顯示畫面，請立即支援。", "time": "NOW", "remark": "會議中斷中，請帶備用線材。", "status": "PENDING"},
    {"department_code": "FS", "department_name": "FS 花房", "priority_code": "F", "room": "Lobby", "guest": "N/A", "title": "大廳主花更換", "content": "更換本週主題花藝：使用黃色文心蘭與百合。", "time": "05:00", "remark": "需於客人早餐時段前完成。", "status": "PENDING"},
    {"department_code": "FS", "department_name": "FS 花房", "priority_code": "E", "room": "Room 1001", "guest": "Mr. Chen (VIP)", "title": "求婚佈置", "content": "床鋪灑玫瑰花瓣 (愛心形狀)。", "time": "14:00", "remark": "花瓣需新鮮，不可有枯邊。", "status": "PENDING"},
    {"department_code": "LUR", "department_name": "LUR 洗衣房與制服室", "priority_code": "P", "room": "Room 703", "guest": "Ms. Huang", "title": "客衣快洗 (Express)", "content": "客人西裝一套，需乾洗，晚宴前歸還。", "time": "17:00", "remark": "承諾 4 小時內交件。", "status": "PROGRESS"},
    {"department_code": "LUR", "department_name": "LUR 洗衣房與制服室", "priority_code": "F", "room": "Uniform Room", "guest": "Staff", "title": "制服縫補", "content": "餐飲部背心釦子脫落修補 (共 5 件)。", "time": "14:00", "remark": "無", "status": "PENDING"},
    {"department_code": "GAE", "department_name": "GAE 總務工程", "priority_code": "P", "room": "Room 606", "guest": "Mr. Zhang", "title": "冷氣報修", "content": "客人反應冷氣有異音且漏水。", "time": "NOW", "remark": "請帶水桶與抹布，避免弄濕地毯。", "status": "PENDING"},
    {"department_code": "GAE", "department_name": "GAE 總務工程", "priority_code": "F", "room": "B2 Parking", "guest": "N/A", "title": "燈管更換", "content": "停車場 B 區照明燈管閃爍更換。", "time": "10:00", "remark": "需使用升降機。", "status": "PENDING"},
    {"department_code": "BB", "department_name": "BB 飲料酒吧", "priority_code": "E", "room": "Lounge Bar", "guest": "Mr. X", "title": "存酒領取", "content": "客人預約今晚開瓶 (Macallan 18Y)，請先送至包廂。", "time": "20:00", "remark": "準備冰球。", "status": "PENDING"},
    {"department_code": "BB", "department_name": "BB 飲料酒吧", "priority_code": "P", "room": "Pool Bar", "guest": "Event", "title": "冰塊緊急支援", "content": "泳池派對冰塊用盡，請支援 5 大包。", "time": "NOW", "remark": "使用推車運送。", "status": "PENDING"},
    {"department_code": "AD", "department_name": "AD 美術設計", "priority_code": "E", "room": "Marketing", "guest": "Hotel", "title": "跨年海報設計", "content": "設計 2026 跨年派對主視覺海報。", "time": "2025-12-20", "remark": "風格需奢華金色系。", "status": "PROGRESS"},
    {"department_code": "AD", "department_name": "AD 美術設計", "priority_code": "F", "room": "Restaurant", "guest": "N/A", "title": "菜單換季更新", "content": "調整義大利餐廳冬季菜單排版。", "time": "2025-12-25", "remark": "需校對英文說明。", "status": "PENDING"},
    {"department_code": "LA", "department_name": "LA 休閒活動部", "priority_code": "E", "room": "Kids Club", "guest": "Family Lin", "title": "DIY 課程準備", "content": "準備下午 3 點的「薑餅屋 DIY」材料包 10 份。", "time": "14:30", "remark": "確認糖霜存量。", "status": "PENDING"},
    {"department_code": "LA", "department_name": "LA 休閒活動部", "priority_code": "P", "room": "Swimming Pool", "guest": "Guest", "title": "毛巾補充", "content": "泳池毛巾架已空，請立即補貨。", "time": "NOW", "remark": "人潮眾多，請多補 2 車。", "status": "PENDING"},
]


def map_priority(code: str) -> str:
    """P/E/F -> TaskPriority str value mapping helper"""
    code = (code or "F").upper()
    if code == "P":
        return "urgent"
    if code == "E":
        return "high"
    return "medium"


def map_status(code: str) -> str:
    code = (code or "PENDING").upper()
    if code == "PROGRESS":
        return "in_progress"
    if code == "COMPLETED":
        return "completed"
    return "pending"


def build_flex(entry: dict) -> dict:
    """以 entry 生成 Flex bubble"""
    return create_hotel_task_card(
        dept=entry["department_name"],
        priority=entry["priority_code"],
        room=entry["room"],
        guest=entry["guest"],
        title=entry["title"],
        content=entry["content"],
        time=entry["time"],
        remark=entry["remark"],
        status=entry["status"],
        task_id=None,
    )


def group_flex_by_department() -> dict[str, list]:
    buckets: dict[str, list] = {}
    for entry in SEED_TASKS:
        buckets.setdefault(entry["department_code"], []).append(build_flex(entry))
    return buckets
