# Flex Message 整合架構圖

## 🏗️ 系統架構全景

```
┌─────────────────────────────────────────────────────────────────────┐
│                         LINE Bot System                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐                    ┌──────────────────┐           │
│  │  LINE User  │                    │  12 Departments  │           │
│  │  (Hotel)    │◄──────────────────►│  (GS/HK/CON...)  │           │
│  └─────────────┘                    └──────────────────┘           │
│         │                                     │                    │
│         │ Message / Postback                  │ Store Tokens      │
│         ▼                                     ▼                    │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │         FastAPI Application (uvicorn)                  │       │
│  ├─────────────────────────────────────────────────────────┤       │
│  │                                                         │       │
│  │  ┌──────────────────────────────────────────────────┐  │       │
│  │  │          LINE Webhook Endpoints                 │  │       │
│  │  ├──────────────────────────────────────────────────┤  │       │
│  │  │  POST /api/linebot/webhook/{department_code}   │  │       │
│  │  │  POST /api/linebot/webhook (unified)           │  │       │
│  │  │  POST /api/linebot/test/postback/{code}        │  │       │
│  │  └──────────────────────────────────────────────────┘  │       │
│  │                       │                                 │       │
│  │                       ▼                                 │       │
│  │  ┌──────────────────────────────────────────────────┐  │       │
│  │  │         LineBotController (Webhook)             │  │       │
│  │  ├──────────────────────────────────────────────────┤  │       │
│  │  │  • handle_webhook()                             │  │       │
│  │  │    - Verify signature                           │  │       │
│  │  │    - Parse events                               │  │       │
│  │  │  • _process_event()                             │  │       │
│  │  │    - Route to handlers                          │  │       │
│  │  │  • _handle_message_event()                      │  │       │
│  │  │    - Extract text message                       │  │       │
│  │  │  • _handle_postback_event()                     │  │       │
│  │  │    - Parse postback data                        │  │       │
│  │  │    - Update task status                         │  │       │
│  │  │    - Send Flex reply                            │  │       │
│  │  └──────────────────────────────────────────────────┘  │       │
│  │                       │                                 │       │
│  │                       ▼                                 │       │
│  │  ┌──────────────────────────────────────────────────┐  │       │
│  │  │       LineBotService (Business Logic)           │  │       │
│  │  ├──────────────────────────────────────────────────┤  │       │
│  │  │  ┌────────────────────────────────────────────┐ │  │       │
│  │  │  │  Message Processing                       │ │  │       │
│  │  │  │  • handle_text_message()                 │ │  │       │
│  │  │  │  • _parse_priority()                     │ │  │       │
│  │  │  │  • _extract_title()                      │ │  │       │
│  │  │  └────────────────────────────────────────────┘ │  │       │
│  │  │                                                  │  │       │
│  │  │  ┌────────────────────────────────────────────┐ │  │       │
│  │  │  │  Flex Message Generation  ★ NEW ★         │ │  │       │
│  │  │  │  • create_task_flex_card(task)           │ │  │       │
│  │  │  │  • _get_priority_config()                │ │  │       │
│  │  │  │  • _get_status_config()                  │ │  │       │
│  │  │  │  • _priority_label()                     │ │  │       │
│  │  │  └────────────────────────────────────────────┘ │  │       │
│  │  │                                                  │  │       │
│  │  │  ┌────────────────────────────────────────────┐ │  │       │
│  │  │  │  Message/Card Sending                     │ │  │       │
│  │  │  │  • send_reply_message()                   │ │  │       │
│  │  │  │  • send_task_flex_reply()  ★ NEW ★       │ │  │       │
│  │  │  │  • send_task_flex_card()   ★ NEW ★       │ │  │       │
│  │  │  │  • reply_flex()                           │ │  │       │
│  │  │  │  • broadcast_flex_to_department()        │ │  │       │
│  │  │  │  • push_message()                        │ │  │       │
│  │  │  └────────────────────────────────────────────┘ │  │       │
│  │  │                                                  │  │       │
│  │  │  ┌────────────────────────────────────────────┐ │  │       │
│  │  │  │  Task Management                          │ │  │       │
│  │  │  │  • get_department_tasks()                 │ │  │       │
│  │  │  │  • update_task_status()                   │ │  │       │
│  │  │  │  • record_report_answer()                 │ │  │       │
│  │  │  │  • get_task_statistics()                  │ │  │       │
│  │  │  └────────────────────────────────────────────┘ │  │       │
│  │  │                                                  │  │       │
│  │  │  ┌────────────────────────────────────────────┐ │  │       │
│  │  │  │  Department Management                    │ │  │       │
│  │  │  │  • initialize_departments()               │ │  │       │
│  │  │  │  • get_bot_api()                          │ │  │       │
│  │  │  │  • get_webhook_handler()                  │ │  │       │
│  │  │  │  • get_last_error()                       │ │  │       │
│  │  │  └────────────────────────────────────────────┘ │  │       │
│  │  └──────────────────────────────────────────────────┘  │       │
│  │                       │                                 │       │
│  ├───────────────────────┼─────────────────────────────────┤       │
│  │                       ▼                                 │       │
│  │  ┌──────────────────────────────────────────────────┐  │       │
│  │  │        API Routes (★ 5 NEW ENDPOINTS ★)        │  │       │
│  │  ├──────────────────────────────────────────────────┤  │       │
│  │  │  GET  /api/linebot/tasks/{id}/flex            │  │       │
│  │  │  GET  /api/linebot/departments/{CODE}/tasks/  │  │       │
│  │  │        {id}/flex                               │  │       │
│  │  │  GET  /api/linebot/departments/{CODE}/         │  │       │
│  │  │        pending-tasks/flex                      │  │       │
│  │  │  POST /api/linebot/departments/{CODE}/         │  │       │
│  │  │        send-task-flex                          │  │       │
│  │  │  POST /api/linebot/departments/{CODE}/         │  │       │
│  │  │        broadcast-task-flex                     │  │       │
│  │  └──────────────────────────────────────────────────┘  │       │
│  │                                                         │       │
│  └─────────────────────────────────────────────────────────┘       │
│         │                                          │                │
│         ▼                                          ▼                │
│  ┌──────────────────┐                   ┌──────────────────┐       │
│  │  LINE Bot API    │                   │   MongoDB DB     │       │
│  │  (Messaging)     │                   │  (Task Storage)  │       │
│  └──────────────────┘                   └──────────────────┘       │
│                                          - Department Collection   │
│                                          - Task Collection        │
│                                                                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 數據流圖

### 1️⃣ 文字訊息 → 自動建立任務 → 回覆 Flex 卡片

```
┌─────────────────┐
│  LINE User      │
│  發送訊息       │
│  "緊急 房間805" │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  LINE Webhook                       │
│  POST /api/linebot/webhook/{CODE}   │
└────────┬────────────────────────────┘
         │
         ▼ (Event: message)
┌─────────────────────────────────────┐
│  handle_webhook()                   │
│  - Verify signature                 │
│  - Parse JSON                       │
└────────┬────────────────────────────┘
         │
         ▼ (Extract: text, user_id, reply_token)
┌─────────────────────────────────────┐
│  handle_text_message()              │
│  - Get department                   │
│  - Parse priority                   │
│  - Create Task object               │
└────────┬────────────────────────────┘
         │
         ▼ (Insert Task to MongoDB)
┌─────────────────────────────────────┐
│  MongoDB                            │
│  tasks: {                           │
│    _id: ObjectId,                   │
│    title: "房間805投訴",             │
│    priority: "urgent",              │
│    status: "pending",               │
│    ...                              │
│  }                                  │
└────────┬────────────────────────────┘
         │
         ▼ (Retrieve Task for rendering)
┌─────────────────────────────────────┐
│  create_task_flex_card(task)        │
│  - Read Task fields                 │
│  - Map priority to config           │
│  - Map status to config             │
│  - Build Flex JSON structure        │
│  Returns: {                         │
│    type: "bubble",                  │
│    header: {...},                   │
│    body: {...},                     │
│    footer: {...}                    │
│  }                                  │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  send_task_flex_reply()             │
│  - Create FlexSendMessage           │
│  - Call bot_api.reply_message()     │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  LINE Bot API   │
│  (Messaging)    │
└────────┬────────┘
         │
         ▼
┌────────────────────────┐
│  LINE User             │
│  收到 Flex Message     │
│  [任務卡片顯示]        │
│  ┌──────────────────┐  │
│  │ 房務部      [P]  │  │
│  │ 房間 805 投訴     │  │
│  ├──────────────────┤  │
│  │ 目前狀態: ● 未執行 │  │
│  │ 優先級: 🔴 緊急   │  │
│  │ 內容: 客人投訴... │  │
│  ├──────────────────┤  │
│  │ [接受任務]       │  │
│  └──────────────────┘  │
└────────────────────────┘
```

### 2️⃣ 點擊按鈕 (Postback) → 更新狀態 → 回覆新卡片

```
┌────────────────────────┐
│  LINE User             │
│  點擊「接受任務」      │
│  按鈕                  │
└────────┬───────────────┘
         │
         ▼ (Postback Event)
┌────────────────────────────────────┐
│  LINE Webhook                      │
│  Event: postback                   │
│  Data: action=task&               │
│        task_id=xxx&               │
│        op=accept&                 │
│        dept=HK                     │
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│  _handle_postback_event()          │
│  - Parse postback data             │
│  - Extract: task_id, op            │
│  - Validate operation              │
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│  update_task_status()              │
│  status_map = {                    │
│    'accept': IN_PROGRESS,          │
│    'complete': COMPLETED,          │
│    'archive': COMPLETED,           │
│    'view_cancel': PENDING          │
│  }                                 │
└────────┬───────────────────────────┘
         │
         ▼ (Get Task by ID, Update status)
┌────────────────────────────────────┐
│  MongoDB                           │
│  updateOne(                        │
│    {_id: xxx},                     │
│    {$set: {status: "in_progress"}} │
│  )                                 │
└────────┬───────────────────────────┘
         │
         ▼ (Return updated Task)
┌────────────────────────────────────┐
│  send_task_flex_reply()            │
│  - Call create_task_flex_card()    │
│    (Task 現在有新狀態)              │
│  - Generate new Flex structure     │
│    (按鈕改為「已完成」,            │
│     狀態改為「▶ 執行中」綠色)      │
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│  bot_api.reply_message()           │
│  (Reply with new Flex)             │
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────────────┐
│  LINE User                 │
│  收到更新後的卡片          │
│  ┌──────────────────────┐  │
│  │ 房務部      [P]      │  │
│  │ 房間 805 投訴         │  │
│  ├──────────────────────┤  │
│  │ 目前狀態: ▶ 執行中 ✓  │  │
│  │ (綠色, 標記為進行中)  │  │
│  │ 優先級: 🔴 緊急       │  │
│  │ 內容: 客人投訴...     │  │
│  ├──────────────────────┤  │
│  │ [已完成]             │  │
│  │ (按鈕變化)           │  │
│  └──────────────────────┘  │
└────────────────────────────┘
```

---

## 🔄 Flex Message 產生流程

```
Task (MongoDB) 
    ↓
    └─► create_task_flex_card(task)
        ├─ _get_priority_config(priority)
        │  └─ Return: {"label": "P", "color": "#D93025"}
        │
        ├─ _get_status_config(status)
        │  └─ Return: {
        │     "text_label": "● 未執行",
        │     "btn_label": "接受任務",
        │     "btn_color": "#1A3B5D",
        │     "btn_action": "accept"
        │   }
        │
        └─ Build Flex Structure:
           ├─ header:        部門 + 優先級 Badge + 標題
           ├─ body:          狀態 + 優先級 + 時間 + 內容 + 備註 + ID
           └─ footer:        (dynamic) 按鈕
               └─ postback:
                   label: "接受任務"
                   data: "action=task&task_id=xxx&op=accept&dept=HK"
                   color: "#1A3B5D"
           
           Returns: {...Flex JSON...}
                ↓
           FlexSendMessage(
               alt_text="任務: 房間805投訴",
               contents=flex_json
           )
                ↓
           bot_api.reply_message() / push_message() / broadcast()
```

---

## 📋 Task 到 Flex 字段映射

```
Task (MongoDB)                 →  Flex Message
─────────────────────────────────────────────────────
department_name              →  header (部門名稱)
priority                     →  header (Badge 顏色)
                             →  body (優先級顏色)
title                        →  header (標題)
status                       →  body (狀態文字)
                             →  footer (按鈕標籤 & 顏色)
created_at                   →  body (建立時間)
description                  →  body (任務內容)
notes                        →  body (備註)
id                           →  body (編號)
                             →  footer (postback data)
```

---

## 🎨 優先級 & 狀態顏色對應

```
優先級:
┌──────────┬────────┬─────────┐
│ Priority │ Label  │ Color   │
├──────────┼────────┼─────────┤
│ URGENT   │   P    │ #D93025 │ 🔴 紅
│ HIGH     │   E    │ #F59E0B │ 🟠 黃
│ MEDIUM   │   F    │ #188038 │ 🟢 綠
│ LOW      │   F    │ #188038 │ 🟢 綠
└──────────┴────────┴─────────┘

狀態:
┌─────────────┬──────────────┬─────────┬──────────┐
│   Status    │  Text Label  │ Color   │ Btn Text │
├─────────────┼──────────────┼─────────┼──────────┤
│ PENDING     │ ● 未執行     │ #D93025 │ 接受任務 │
│             │              │ (紅)    │ (藍)     │
├─────────────┼──────────────┼─────────┼──────────┤
│ IN_PROGRESS │ ▶ 執行中     │ #188038 │ 已完成   │
│             │              │ (綠)    │ (綠)     │
├─────────────┼──────────────┼─────────┼──────────┤
│ COMPLETED   │ ✔ 已完成     │ 灰      │ 查看歸檔 │
│             │              │ (#2C3E) │ (灰)     │
├─────────────┼──────────────┼─────────┼──────────┤
│ CANCELLED   │ ✗ 已取消     │ 灰      │ 查看原因 │
│             │              │ (#888)  │ (灰)     │
└─────────────┴──────────────┴─────────┴──────────┘
```

---

## 🔌 API 端點結構

```
GET /api/linebot/tasks/{id}/flex
├─ Input: task_id (URL parameter)
├─ Process:
│  └─ Task.get(id) → create_task_flex_card() → JSON
└─ Output: {
    "status": "success",
    "task_id": "xxx",
    "flex_message": {...}
   }

GET /api/linebot/departments/{CODE}/pending-tasks/flex
├─ Input: department_code, limit (optional)
├─ Process:
│  ├─ Find all PENDING tasks for dept
│  ├─ Create flex_card for each
│  ├─ If count > 1: wrap in Carousel
│  └─ Else: return single bubble
└─ Output: {
    "status": "success",
    "total": 5,
    "flex_message": {...Carousel or Bubble...}
   }

POST /api/linebot/departments/{CODE}/send-task-flex
├─ Input: task_id, user_id (query params)
├─ Process:
│  ├─ Retrieve Task
│  ├─ Create Flex
│  └─ bot_api.push_message(user_id, flex)
└─ Output: {
    "status": "success",
    "message": "已發送"
   }

POST /api/linebot/departments/{CODE}/broadcast-task-flex
├─ Input: task_id (query param)
├─ Process:
│  ├─ Retrieve Task
│  ├─ Create Flex
│  └─ bot_api.broadcast(flex)
└─ Output: {
    "status": "success",
    "message": "已廣播"
   }
```

---

## 🧪 測試流程

```
test_flex_message.py
├─ init_db()
│  └─ Connect MongoDB
│
├─ test_flex_message_generation()
│  ├─ Query 5 tasks
│  └─ For each task:
│     ├─ create_task_flex_card()
│     ├─ Verify structure
│     └─ Print preview
│
├─ test_flex_carousel()
│  ├─ Query pending tasks
│  ├─ Create carousel
│  └─ Verify contents
│
├─ test_status_transitions()
│  ├─ For each status:
│     ├─ Modify task.status
│     ├─ create_task_flex_card()
│     ├─ Check text label
│     └─ Check button label
│
└─ test_json_export()
   ├─ Serialize to JSON
   ├─ Validate JSON
   └─ Print sample
```

---

## 📦 部署架構

```
生產環境:
┌────────────────────────────────────┐
│  負載均衡器 (Load Balancer)         │
└────────────────┬───────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐   ┌──────────────┐
│ FastAPI      │   │ FastAPI      │
│ Instance 1   │   │ Instance 2   │
└──────┬───────┘   └───────┬──────┘
       │                   │
       └───────────┬───────┘
                   ▼
          ┌──────────────────┐
          │   MongoDB 集群   │
          │ (replicated)     │
          └──────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
   [Primary]            [Secondary]
   
每個實例:
├─ linebot_service (singleton)
│  └─ department_bots dict (initialized on startup)
├─ linebot_controller
├─ linebot_routes
└─ Database connection pool
```

---

完整的架構整合文件已準備完成！ 🎉

