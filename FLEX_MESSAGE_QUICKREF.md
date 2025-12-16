# Flex Message 快速參考卡

## 🎯 核心概念

### 從資料庫到 Flex Message
```
Task (資料庫) 
    ↓
create_task_flex_card(task) 
    ↓
Flex Message JSON (可在 LINE 上顯示)
```

---

## 📍 主要方法速查

### 1. 產生 Flex Message
```python
flex_card = linebot_service.create_task_flex_card(task)
# 回傳: {"type": "bubble", "header": {...}, "body": {...}, "footer": {...}}
```

### 2. 發送給個別使用者
```python
await linebot_service.send_task_flex_card("GS", "U1234...", task, use_push=True)
```

### 3. 廣播給整個部門
```python
await linebot_service.send_task_flex_card("GS", None, task, use_push=False)
```

### 4. 回覆用戶訊息
```python
await linebot_service.send_task_flex_reply(department_code, reply_token, task)
```

---

## 🔌 API 端點速查

### 查詢任務卡片
| 端點 | 方法 | 說明 |
|------|------|------|
| `/api/linebot/tasks/{id}/flex` | GET | 查詢任務，回傳 Flex JSON |
| `/api/linebot/departments/{CODE}/tasks/{id}/flex` | GET | 查詢部門任務，回傳 Flex |
| `/api/linebot/departments/{CODE}/pending-tasks/flex` | GET | 查詢待處理任務，回傳 Carousel |

### 發送任務卡片
| 端點 | 方法 | 說明 |
|------|------|------|
| `/api/linebot/departments/{CODE}/send-task-flex` | POST | 發送給個別使用者 |
| `/api/linebot/departments/{CODE}/broadcast-task-flex` | POST | 廣播給整個部門 |

---

## 🧪 快速測試

### 執行測試
```bash
python test_flex_message.py
```

### 測試項目
- ✅ Flex Message 結構驗證
- ✅ Carousel 生成
- ✅ 任務狀態轉移
- ✅ JSON 匯出

---

## 📊 狀態與優先級

### 任務狀態
| 狀態 | 值 | 文字 | 顏色 | 按鈕 |
|------|-----|------|------|------|
| 待處理 | PENDING | ● 未執行 | 🔴 紅 | 接受任務 (藍) |
| 執行中 | IN_PROGRESS | ▶ 執行中 | 🟢 綠 | 已完成 (綠) |
| 已完成 | COMPLETED | ✔ 已完成 | 灰 | 查看歸檔 (灰) |
| 已取消 | CANCELLED | ✗ 已取消 | 灰 | 查看原因 (灰) |

### 優先級
| 優先級 | 值 | Label | 顏色 | 文字 |
|--------|-----|-------|------|------|
| 緊急 | URGENT | P | 🔴 #D93025 | 🔴 緊急 |
| 高 | HIGH | E | 🟠 #F59E0B | 🟠 高 |
| 中 | MEDIUM | F | 🟢 #188038 | 🟢 中 |
| 低 | LOW | F | 🟢 #188038 | 🟢 低 |

---

## 💻 使用情境

### 情境 1: 使用者發送訊息 → 自動回覆卡片
```
使用者: "緊急 房間 805 投訴"
  ↓
系統: 建立任務
  ↓
系統: 回覆 Flex Message 卡片
  ↓
使用者: 點擊「接受任務」
  ↓
系統: 更新狀態，回覆新卡片
```

### 情境 2: API 查詢並發送
```bash
# 查詢部門所有待處理任務
curl "http://localhost/api/linebot/departments/GS/pending-tasks/flex"

# 回傳 Carousel (多張卡片)

# 發送給特定使用者
curl -X POST "http://localhost/api/linebot/departments/GS/send-task-flex?task_id=xxx&user_id=Uxxx"
```

### 情境 3: 批量廣播
```python
# 查詢所有待處理任務
tasks = await Task.find({"status": TaskStatus.PENDING}).to_list()

# 產生 Carousel
bubbles = [linebot_service.create_task_flex_card(t) for t in tasks]
carousel = {"type": "carousel", "contents": bubbles}

# 廣播給部門
await linebot_service.broadcast_flex_to_department("GS", "待處理任務", carousel)
```

---

## 🔧 修改指南

### 修改優先級顏色
檔案: `app/services/linebot_service.py`
```python
def _get_priority_config(self, priority: TaskPriority) -> dict:
    PRIORITY_MAP = {
        TaskPriority.URGENT: {"label": "P", "color": "#D93025"},  # ← 修改這裡
        TaskPriority.HIGH: {"label": "E", "color": "#F59E0B"},
        ...
    }
```

### 修改按鈕文字
檔案: `app/services/linebot_service.py`
```python
def _get_status_config(self, status: TaskStatus) -> dict:
    STATUS_MAP = {
        TaskStatus.PENDING: {
            "btn_label": "接受任務 (Accept)",  # ← 修改這裡
            ...
        },
        ...
    }
```

### 修改卡片欄位
檔案: `app/services/linebot_service.py`
方法: `create_task_flex_card()`
```python
# Body 中的欄位順序與內容在這裡定義
"contents": [
    # 修改/新增欄位...
]
```

---

## ⚠️ 常見問題

### Q: 為什麼卡片沒有顯示？
- [ ] 檢查 Task 物件是否有正確資料
- [ ] 確認 MongoDB 連線正常
- [ ] 查看控制台是否有錯誤訊息
- [ ] 檢查 Flex Message JSON 結構是否有效

### Q: 如何新增自訂欄位到卡片？
1. 在 Task 模型添加字段
2. 在 `create_task_flex_card()` 的 body 中添加欄位
3. 格式參考現有欄位的佈局

### Q: Carousel 最多支援幾張卡片？
- LINE 官方限制: 最多 10 張
- 系統預設: 單次查詢最多 100 件（可自訂）

### Q: 如何支援多語言？
在 `_priority_label()` 和 `_get_status_config()` 中添加語言選項

---

## 📁 相關檔案

| 檔案 | 說明 |
|------|------|
| `app/services/linebot_service.py` | Flex Message 核心邏輯 |
| `app/controllers/linebot_controller.py` | Webhook 事件處理 |
| `app/routes/linebot_routes.py` | API 端點定義 |
| `app/models/task.py` | Task 資料模型 |
| `test_flex_message.py` | 測試腳本 |
| `FLEX_MESSAGE_GUIDE.md` | 詳細指南 |
| `templates/pull_task_linebot/flex_templates.py` | 舊版 Flex 模板（參考用） |

---

## ✅ 檢查清單

部署前：
- [ ] 執行 `python test_flex_message.py` 通過
- [ ] 資料庫有測試任務資料
- [ ] API 端點可訪問
- [ ] LINE Webhook 配置正確
- [ ] 手動測試發送訊息並接收卡片

---

## 🚀 部署步驟

```bash
# 1. 驗證語法
python -m py_compile app/services/linebot_service.py
python -m py_compile app/controllers/linebot_controller.py
python -m py_compile app/routes/linebot_routes.py

# 2. 初始化部門
python init_linebot_departments.py

# 3. 建立測試資料
python templates/seed_tasks.py

# 4. 執行測試
python test_flex_message.py

# 5. 啟動服務
python run.py

# 6. 測試 API
curl "http://localhost:8000/api/linebot/webhook/verify"
```

---

**Flex Message 整合完成！** 🎉

