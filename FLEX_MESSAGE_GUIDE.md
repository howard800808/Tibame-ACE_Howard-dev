# Flex Message 與資料庫整合指南

## 📋 概述

LINE Bot 系統現在完全整合了 **Flex Message 任務卡** 與 **MongoDB 資料庫**。所有任務卡內容均從資料庫動態產生，支援多種任務狀態與優先級。

---

## 🎯 核心功能

### 1. **自動生成 Flex Message**
- ✅ 從 MongoDB Task 物件直接產生 Flex Message
- ✅ 支援 4 種任務狀態（待處理、執行中、已完成、已取消）
- ✅ 支援 4 種優先級（緊急、高、中、低）
- ✅ 動態生成按鈕標籤與顏色

### 2. **文字訊息 → Flex 卡片回覆**
- ✅ 使用者發送文字訊息 → 系統自動建立任務
- ✅ 回覆 Flex Message 任務卡（不再回覆純文字）
- ✅ 卡片包含任務編號、內容、優先級、狀態等完整資訊

### 3. **Postback 事件 → Flex 更新**
- ✅ 點擊任務卡按鈕 → 更新任務狀態
- ✅ 狀態更新後自動回覆新的 Flex 卡片（反映最新狀態）

### 4. **API 端點查詢 & 發送**
- ✅ 查詢指定任務的 Flex Message 結構
- ✅ 發送任務卡給個別使用者 (push)
- ✅ 廣播待處理任務卡給整個部門 (broadcast)

---

## 📦 資料庫結構

### Task 模型字段

```python
{
    "_id": ObjectId,                    # 任務 ID
    "department_code": "GS",            # 部門代碼
    "department_name": "客務部",        # 部門名稱
    "line_user_id": "U1234...",         # LINE 使用者 ID
    "line_user_name": "張三",           # 使用者名稱
    "title": "感動服務 - 迎賓接待",     # 任務標題
    "description": "詳細訊息內容",      # 任務描述
    "status": "pending",                # 狀態: pending|in_progress|completed|cancelled
    "priority": "urgent",               # 優先級: urgent|high|medium|low
    "created_at": ISODate,              # 建立時間
    "updated_at": ISODate,              # 更新時間
    "completed_at": ISODate,            # 完成時間（可選）
    "assigned_to": "user_id",           # 指派給誰（可選）
    "notes": "備註內容",                # 備註（可選）
    "tags": ["標籤1", "標籤2"],         # 標籤
    "report_answers": [                 # 回報流程答案
        {"step": 1, "answer": "yes", "recorded_at": ISODate}
    ],
    "report_completed": false,          # 回報流程是否完成
    "message_id": "message_id",         # LINE 訊息 ID
    "message_type": "text",             # 訊息類型
    "original_message": "原始訊息"      # 原始訊息內容
}
```

---

## 🔧 核心修改說明

### 1. **linebot_service.py** - 新增方法

#### `create_task_flex_card(task: Task) -> dict`
- **功能**: 從 Task 物件產生 Flex Message bubble
- **參數**: Task 資料庫物件
- **回傳**: Flex Message JSON 結構
- **特性**:
  - 自動對應優先級顏色（紅/黃/綠）
  - 自動對應狀態文字與按鈕（待執行/執行中/已完成/已取消）
  - 包含完整任務資訊（標題、內容、優先級、狀態、時間等）
  - 支援 postback 動作（接受/完成）

```python
# 使用範例
flex_card = linebot_service.create_task_flex_card(task)
```

#### `send_task_flex_card(department_code, user_id, task, use_push=True) -> bool`
- **功能**: 發送任務 Flex 卡片給使用者或廣播
- **參數**:
  - `department_code`: 部門代碼
  - `user_id`: LINE 使用者 ID
  - `task`: Task 物件
  - `use_push`: True=發送給個別使用者, False=廣播給全部門
- **回傳**: 發送成功與否

```python
# 發送給個別使用者
await linebot_service.send_task_flex_card("GS", "U1234...", task, use_push=True)

# 廣播給整個部門
await linebot_service.send_task_flex_card("GS", None, task, use_push=False)
```

#### `send_task_flex_reply(department_code, reply_token, task) -> bool`
- **功能**: 回覆任務 Flex Message 卡片
- **用途**: 在 webhook 中回覆用戶訊息

```python
# 在 webhook 回覆
await linebot_service.send_task_flex_reply(department_code, reply_token, task)
```

#### 輔助方法
- `_get_priority_config(priority)`: 取得優先級配置（顏色、標籤）
- `_get_status_config(status)`: 取得狀態配置（文字、顏色、按鈕）
- `_priority_label(priority)`: 將優先級轉換為可讀文字

### 2. **handle_text_message()** - 修改回覆方式

**之前**: 回覆純文字確認訊息
```
✅ 任務已收到！
📋 任務編號: xxx
...
```

**之後**: 回覆 Flex Message 任務卡
```
[Flex Message 卡片，包含所有任務資訊、優先級、狀態、按鈕]
```

### 3. **linebot_controller.py** - Postback 事件增強

```python
# 點擊按鈕時自動回覆更新後的 Flex 卡片
if updated and reply_token:
    await linebot_service.send_task_flex_reply(
        department_code,
        reply_token,
        updated  # 回覆更新後的任務卡
    )
```

### 4. **linebot_routes.py** - 新增 API 端點

#### 查詢任務 Flex 卡片
```
GET /api/linebot/tasks/{task_id}/flex
```
查詢指定任務並回傳 Flex Message JSON

```
GET /api/linebot/departments/{code}/tasks/{task_id}/flex
```
查詢部門內的指定任務

```
GET /api/linebot/departments/{code}/pending-tasks/flex?limit=10
```
查詢部門所有待處理任務，回傳 Carousel (多張卡片)

#### 發送任務卡片
```
POST /api/linebot/departments/{code}/send-task-flex?task_id=xxx&user_id=Uxxx
```
發送任務卡片給個別使用者 (push)

```
POST /api/linebot/departments/{code}/broadcast-task-flex?task_id=xxx
```
廣播任務卡片給整個部門

---

## 🧪 測試方式

### 1. 單元測試
```bash
python test_flex_message.py
```

測試項目：
- ✅ Flex Message 結構驗證
- ✅ Carousel 生成
- ✅ 任務狀態轉移
- ✅ JSON 匯出

### 2. API 測試

#### 查詢任務卡片
```bash
curl "http://localhost:8000/api/linebot/tasks/TASK_ID/flex"
```

回傳：
```json
{
  "status": "success",
  "task_id": "xxx",
  "task_title": "感動服務",
  "task_status": "pending",
  "flex_message": {
    "type": "bubble",
    "header": {...},
    "body": {...},
    "footer": {...}
  }
}
```

#### 發送任務卡片給使用者
```bash
curl -X POST "http://localhost:8000/api/linebot/departments/GS/send-task-flex?task_id=xxx&user_id=Uxxx"
```

#### 廣播待處理任務
```bash
curl "http://localhost:8000/api/linebot/departments/GS/pending-tasks/flex?limit=5"
```

### 3. 手動 LINE 測試

1. 添加 LINE Bot 好友
2. 發送訊息給 Bot
3. Bot 會回覆 **Flex Message 任務卡**（包含優先級、狀態、按鈕）
4. 點擊卡片上的按鈕
5. 任務狀態更新，Bot 回覆 **更新後的任務卡**

---

## 🎨 Flex Message 卡片結構

### Header（頂部）
- 部門名稱 + 優先級 Badge
- 任務標題

### Body（中間內容）
- 📌 目前狀態 (待執行/執行中/已完成/已取消)
- ⚡ 優先級 (紅/黃/綠)
- 🕐 建立時間
- 📝 任務內容
- 📌 備註 (如果有)
- 🆔 任務編號

### Footer（底部）
- 主按鈕：接受任務 / 已完成 / 查看歸檔 / 查看取消原因
- 按鈕顏色與標籤根據任務狀態動態變化

---

## 📊 任務狀態與優先級對應

### 狀態轉移
```
PENDING (待處理)
   ↓ [接受任務]
IN_PROGRESS (執行中)
   ↓ [已完成]
COMPLETED (已完成)
```

### 優先級顏色
- 🔴 **URGENT (緊急)**: 紅色 #D93025
- 🟠 **HIGH (高)**: 黃色 #F59E0B
- 🟢 **MEDIUM/LOW (中/低)**: 綠色 #188038

### 按鈕邏輯
| 狀態 | 按鈕標籤 | 按鈕顏色 | Action |
|------|---------|---------|--------|
| PENDING | 接受任務 | 藍色 | accept |
| IN_PROGRESS | 已完成 | 綠色 | complete |
| COMPLETED | 查看歸檔 | 灰色 | archive |
| CANCELLED | 查看取消原因 | 灰色 | view_cancel |

---

## 🚀 使用流程

### 使用者角度
```
1. 使用者發送訊息給 LINE Bot
   "緊急 需要處理房間 805 的投訴"

2. Bot 自動建立任務並回覆
   [Flex Message 卡片顯示所有資訊]

3. 使用者點擊「接受任務」按鈕
   按鈕 → postback 事件 → 任務狀態改為 IN_PROGRESS

4. Bot 回覆更新後的卡片
   [狀態改為「▶ 任務執行中」，按鈕改為「已完成」]

5. 使用者點擊「已完成」
   按鈕 → postback 事件 → 進入 5 步驟回報流程
```

### 系統管理員角度
```
1. 從資料庫查詢任務
   GET /api/linebot/departments/GS/pending-tasks/flex?limit=10

2. 回傳 Carousel 包含 10 張待處理任務卡片

3. 管理員可分享卡片給特定部門成員
   POST /api/linebot/departments/GS/send-task-flex?task_id=xxx&user_id=Uxxx

4. 部門成員收到卡片，點擊按鈕更新狀態
```

---

## 🔍 常見問題

### Q1: 如何從資料庫直接查詢任務卡片？
```python
from app.services.linebot_service import linebot_service
from beanie import PydanticObjectId
from app.models.task import Task

task = await Task.get(PydanticObjectId(task_id))
flex_card = linebot_service.create_task_flex_card(task)
```

### Q2: 如何廣播任務卡片給整個部門？
```python
# 方式 1：使用服務方法
await linebot_service.send_task_flex_card("GS", None, task, use_push=False)

# 方式 2：使用 API
curl -X POST "http://localhost:8000/api/linebot/departments/GS/broadcast-task-flex?task_id=xxx"
```

### Q3: 如何修改卡片的顏色或按鈕？
編輯 `linebot_service.py` 中的 `_get_priority_config()` 或 `_get_status_config()` 方法：

```python
def _get_priority_config(self, priority: TaskPriority) -> dict:
    PRIORITY_MAP = {
        TaskPriority.URGENT: {"label": "P", "color": "#D93025"},  # 修改顏色
        ...
    }
    return PRIORITY_MAP.get(priority, PRIORITY_MAP[TaskPriority.MEDIUM])
```

### Q4: 卡片包含哪些資訊？
- 部門名稱、優先級 Badge
- 任務標題、優先級、狀態
- 建立時間、任務內容、備註
- 任務編號、操作按鈕

### Q5: 如何支援 Carousel (多卡片)？
系統已自動支援，當任務超過 1 件時自動生成 Carousel：

```python
bubbles = [linebot_service.create_task_flex_card(task) for task in tasks]
carousel = {"type": "carousel", "contents": bubbles}
```

---

## 📝 開發筆記

### 修改的檔案
1. ✅ `app/services/linebot_service.py` - 新增 Flex 生成方法
2. ✅ `app/controllers/linebot_controller.py` - 修改 postback 回覆邏輯
3. ✅ `app/routes/linebot_routes.py` - 新增 4 個 API 端點
4. ✅ `test_flex_message.py` - 新建測試腳本

### 沒有修改的檔案
- `templates/pull_task_linebot/flex_templates.py` - 原本就有 Flex 模板設計
- `app/models/task.py` - 保持不變，包含所有必要欄位
- `seed_tasks.py` - 保持不變，用於建立測試資料

### 設計決策
- ✅ **動態生成而非模板檔案**: 直接從 Task 物件產生，無需維護靜態 JSON
- ✅ **支援所有狀態**: PENDING/IN_PROGRESS/COMPLETED/CANCELLED
- ✅ **Postback 更新**: 點擊按鈕自動回覆更新的卡片
- ✅ **API 可查詢**: 所有卡片可通過 API 查詢和發送

---

## 🎓 下一步

### 可能的擴充功能
1. **Rich Menu** - 快捷選單，快速發送常見任務
2. **Flex Template** - 根據不同任務類型使用不同模板
3. **Image Support** - 任務卡片包含圖片
4. **Auto Assignment** - 自動指派任務給特定部門
5. **Scheduled Reminders** - 定時提醒待處理任務
6. **Role-based Permissions** - 權限控制
7. **Audit Logging** - 完整的操作審計日誌

---

## ✅ 驗證清單

在部署前請確認：

- [ ] 所有語法檢查通過 (`get_errors()`)
- [ ] 資料庫連線正常
- [ ] 12 個部門已初始化 (`python init_linebot_departments.py`)
- [ ] 測試資料已建立 (`python templates/seed_tasks.py`)
- [ ] 測試腳本執行成功 (`python test_flex_message.py`)
- [ ] API 端點可正常訪問
- [ ] LINE Webhook 配置正確
- [ ] Postback 事件可正確處理
- [ ] Flex Message 在 LINE 上正確顯示

---

**完整的 Flex Message 與資料庫整合現已準備就緒！** 🎉

