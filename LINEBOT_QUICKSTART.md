# LINE Bot 整合 - 快速開始指南

## 📋 已完成的整合項目

✅ **資料模型** (`app/models/`)
- `department.py` - 12 個部門的 LINE Bot 配置儲存
- `task.py` - 任務管理資料模型（含優先級和狀態）

✅ **Schema 定義** (`app/schemas/linebot_schema.py`)
- 任務建立、更新和回應結構
- LINE Bot Webhook 事件解析

✅ **服務層** (`app/services/linebot_service.py`)
- 訊息接收和處理
- 任務自動建立
- 優先級自動判斷
- 用戶通知推送

✅ **控制層** (`app/controllers/linebot_controller.py`)
- Webhook 簽名驗證
- 事件分發處理
- 任務狀態管理

✅ **API 路由** (`app/routes/linebot_routes.py`)
- 12 個獨立的 Webhook 端點
- 任務查詢和管理 API

✅ **管理介面** (`app/views/linebot_view.py`)
- LINE Bot 儀表板
- 部門任務管理頁面

✅ **配置管理** (`app/core/config.py`)
- 12 個部門的 TOKEN 和 SECRET 配置

✅ **初始化腳本** (`init_linebot_departments.py`)
- 一鍵初始化所有部門配置到 MongoDB

## 🚀 快速開始

### 1️⃣ 確認環境變數

編輯 `.env` 檔案，確保包含 12 個部門的設定：

```env
GS_ACCESS_TOKEN=your_token
GS_SECRET=your_secret
HK_ACCESS_TOKEN=your_token
HK_SECRET=your_secret
# ... 其他 10 個部門
```

### 2️⃣ 初始化部門資料

```bash
python init_linebot_departments.py
```

輸出範例：
```
開始初始化 12 個部門的 LINE Bot 設定...
============================================================
✓ GS - 客務部: 建立成功
✓ HK - 房務部: 建立成功
... (其他部門)
============================================================

初始化完成:
  成功: 12
  跳過: 0
  失敗: 0
  總計: 12
```

### 3️⃣ 啟動應用程式

```bash
python run.py
```

應用程式會在啟動時自動初始化所有部門的 LINE Bot。

## 📡 LINE Bot Webhook 設定

### 線上部署 (Production)

1. **選擇 LINE Channel**
   - 進入 [LINE Developers Console](https://developers.line.biz)
   - 選擇您的 Messaging API Channel

2. **設定 Webhook URL**
   ```
   https://your-domain.com/api/linebot/webhook/{DEPARTMENT_CODE}
   ```
   例如：
   - GS 部門: `https://your-domain.com/api/linebot/webhook/GS`
   - HK 部門: `https://your-domain.com/api/linebot/webhook/HK`
   - ...以此類推

3. **啟用 Webhook**
   - ✅ 勾選 "Use webhook"
   - 測試連線確認成功

### 本地測試 (Development)

使用 **ngrok** 進行本地隧道測試：

```bash
# 安裝 ngrok
# 訪問 https://ngrok.com/download

# 啟動隧道（代理到 localhost:8000）
ngrok http 8000

# 會顯示公開 URL，例如：
# https://xxxx-xx-xxx-xxx-xx.ngrok.io

# 在 LINE Developers Console 設定：
# https://xxxx-xx-xxx-xxx-xx.ngrok.io/api/linebot/webhook/GS
```

## 🎯 API 端點速查表

### Webhook (接收訊息)
```
POST /api/linebot/webhook/{DEPT_CODE}
```

### 查詢部門資訊
```
GET /api/linebot/departments/{DEPT_CODE}
```

回應範例：
```json
{
  "department": {
    "code": "GS",
    "name": "客務部",
    "is_active": true
  },
  "statistics": {
    "total": 45,
    "pending": 10,
    "in_progress": 5,
    "completed": 30,
    "completion_rate": 66.67
  }
}
```

### 查詢部門任務
```
GET /api/linebot/departments/{DEPT_CODE}/tasks?status=pending&limit=50
```

### 更新任務狀態
```
PUT /api/linebot/tasks/{TASK_ID}/status?status=completed&notes=已處理
```

### 廣播訊息
```
POST /api/linebot/departments/{DEPT_CODE}/broadcast?message=系統維護通知
```

### 列出所有部門
```
GET /api/linebot/departments
```

## 🎨 管理介面

啟動後可訪問以下頁面：

| 路由 | 功能 |
|------|------|
| `/linebot/dashboard` | LINE Bot 管理儀表板 |
| `/linebot/departments/{CODE}/tasks` | 部門任務管理 |

## 💾 資料庫表結構

### Department Collection
```javascript
{
  _id: ObjectId,
  code: "GS",                    // 部門代碼
  name: "客務部",                // 部門名稱
  access_token: "...",           // LINE Bot Access Token
  channel_secret: "...",         // LINE Bot Channel Secret
  is_active: true,               // 是否啟用
  description: "...",            // 部門描述
  created_at: ISODate,
  updated_at: ISODate
}
```

### Task Collection
```javascript
{
  _id: ObjectId,
  department_code: "GS",         // 部門代碼
  department_name: "客務部",     // 部門名稱
  line_user_id: "U123...",       // LINE 用戶 ID
  line_user_name: "張三",        // LINE 用戶名稱
  title: "處理客戶投訴",          // 任務標題
  description: "...",            // 任務詳細描述
  status: "pending",             // 狀態：pending, in_progress, completed, cancelled
  priority: "high",              // 優先級：urgent, high, medium, low
  created_at: ISODate,
  updated_at: ISODate,
  completed_at: ISODate,         // 完成時間（可選）
  assigned_to: "user_id",        // 指派給誰（可選）
  tags: ["標籤1"],              // 標籤
  original_message: "..."        // 原始 LINE 訊息
}
```

## 🔧 優先級自動識別

系統會自動偵測訊息中的關鍵字：

| 優先級 | 關鍵字 |
|--------|--------|
| 🔴 URGENT (緊急) | 緊急、urgent、立即、馬上 |
| 🟠 HIGH (重要) | 重要、high、優先 |
| 🟡 MEDIUM (一般) | （預設值） |
| 🟢 LOW (低) | 低、low、不急 |

## ✅ 測試檢查清單

- [ ] MongoDB 連線正常
- [ ] `.env` 檔案配置完整
- [ ] 執行 `init_linebot_departments.py` 成功
- [ ] 應用程式正常啟動
- [ ] LINE Developers 已設定 Webhook URL
- [ ] 測試傳送訊息到 LINE Bot
- [ ] 任務是否正確建立在 MongoDB

## 🐛 常見問題

### Q: Webhook 收不到訊息？
A: 
1. 檢查 Webhook URL 是否正確
2. 確認已在 LINE Developers 啟用 Webhook
3. 檢查簽名驗證是否通過
4. 查看應用程式日誌

### Q: 訊息發送失敗？
A:
1. 確認 Access Token 有效
2. 檢查用戶是否已加入好友
3. 確認沒有超過 LINE API 限流

### Q: 初始化失敗？
A:
1. 檢查 MongoDB 連線
2. 確認 `.env` TOKEN 格式正確
3. 查看詳細錯誤訊息

## 📚 相關文件

- [完整說明文檔](./LINEBOT_README.md)
- [LINE Messaging API 官方文檔](https://developers.line.biz/en/docs/messaging-api/)
- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)

## 🎓 12 個部門一覽

| # | 代碼 | 部門名稱 | 職責 |
|----|------|---------|------|
| 1 | GS | 客務部 | 前台接待與客戶服務 |
| 2 | HK | 房務部 | 客房清潔與整理 |
| 3 | CON | 門房諮詢 | 門房服務與諮詢 |
| 4 | BP | 烘焙點心房 | 烘焙與點心製作 |
| 5 | FB | 餐飲 | 餐飲服務 |
| 6 | CBS | 會議宴會 | 會議與宴會服務 |
| 7 | FS | 花房 | 花藝佈置與維護 |
| 8 | LUR | 洗衣房與制服室 | 洗衣與制服管理 |
| 9 | GAE | 總務工程 | 總務與工程維護 |
| 10 | BB | 飲料酒吧 | 飲料與酒吧服務 |
| 11 | AD | 美術設計 | 美術設計與視覺規劃 |
| 12 | LA | 休閒活動部 | 休閒活動規劃與執行 |

---

**整合完成！祝您使用愉快！** 🎉
