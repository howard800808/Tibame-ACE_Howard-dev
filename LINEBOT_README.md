# LINE Bot 整合說明

## 概述

本專案已整合 12 個部門的 LINE Bot 功能，用於接收和管理各部門的任務訊息。

## 部門列表

| 代碼 | 部門名稱 | 說明 |
|------|---------|------|
| GS | 客務部 | 負責前台接待與客戶服務 |
| HK | 房務部 | 負責客房清潔與整理 |
| CON | 門房諮詢 | 負責門房服務與諮詢 |
| BP | 烘焙點心房 | 負責烘焙與點心製作 |
| FB | 餐飲 | 負責餐飲服務 |
| CBS | 會議宴會 | 負責會議與宴會服務 |
| FS | 花房 | 負責花藝佈置與維護 |
| LUR | 洗衣房與制服室 | 負責洗衣與制服管理 |
| GAE | 總務工程 | 負責總務與工程維護 |
| BB | 飲料酒吧 | 負責飲料與酒吧服務 |
| AD | 美術設計 | 負責美術設計與視覺規劃 |
| LA | 休閒活動部 | 負責休閒活動規劃與執行 |

## 設定步驟

### 1. 確認 .env 配置

確保 `.env` 檔案中已設定所有 12 個部門的 ACCESS_TOKEN 和 SECRET：

```env
# GS - 客務部
GS_ACCESS_TOKEN=your_token_here
GS_SECRET=your_secret_here

# HK - 房務部
HK_ACCESS_TOKEN=your_token_here
HK_SECRET=your_secret_here

# ... 其他部門
```

### 2. 初始化部門資料

執行初始化腳本，將部門配置載入資料庫：

```bash
python init_linebot_departments.py
```

這會：
- 讀取 `.env` 中的所有部門配置
- 將配置儲存到 MongoDB
- 顯示初始化結果

### 3. 啟動應用程式

```bash
python run.py
```

應用程式啟動時會自動初始化所有部門的 LINE Bot。

## API 端點

### Webhook 端點

每個部門都有獨立的 webhook URL：

```
POST /api/linebot/webhook/{department_code}
```

例如：
- GS (客務部): `POST /api/linebot/webhook/GS`
- HK (房務部): `POST /api/linebot/webhook/HK`
- 其他部門以此類推...

**配置方式：**
1. 進入 LINE Developers Console
2. 選擇對應的 Messaging API Channel
3. 設定 Webhook URL 為：`https://your-domain.com/api/linebot/webhook/{DEPT_CODE}`
4. 啟用 "Use webhook"

### 查詢端點

#### 取得部門資訊和統計
```
GET /api/linebot/departments/{department_code}
```

#### 取得部門任務列表
```
GET /api/linebot/departments/{department_code}/tasks?status=pending&limit=50
```

參數：
- `status` (可選): pending, in_progress, completed, cancelled
- `limit` (可選): 返回數量限制 (1-200)

#### 列出所有部門
```
GET /api/linebot/departments
```

#### 更新任務狀態
```
PUT /api/linebot/tasks/{task_id}/status?status=completed&notes=已處理完成
```

參數：
- `status` (必填): pending, in_progress, completed, cancelled
- `notes` (可選): 備註說明

#### 廣播訊息
```
POST /api/linebot/departments/{department_code}/broadcast?message=系統維護通知
```

## 功能說明

### 自動任務建立

當用戶透過 LINE 發送訊息給任一部門時：
1. 系統自動建立任務記錄
2. 解析訊息優先級（緊急、重要、一般、低）
3. 提取任務標題（取訊息第一行或前 50 字）
4. 回覆確認訊息給用戶

### 優先級關鍵字

系統會自動偵測訊息中的關鍵字來判定優先級：

- **緊急 (URGENT)**: "緊急"、"urgent"、"立即"、"馬上"
- **重要 (HIGH)**: "重要"、"high"、"優先"
- **低 (LOW)**: "低"、"low"、"不急"
- **一般 (MEDIUM)**: 預設值

### 狀態更新通知

當任務狀態更新時，系統會自動透過 LINE 推送通知給原始發送者。

## 資料庫結構

### Department Collection
```javascript
{
  "_id": ObjectId,
  "code": "GS",           // 部門代碼
  "name": "客務部",       // 部門名稱
  "access_token": "...",  // LINE Bot Access Token
  "channel_secret": "...", // LINE Bot Channel Secret
  "is_active": true,      // 是否啟用
  "description": "...",   // 部門描述
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### Task Collection
```javascript
{
  "_id": ObjectId,
  "department_code": "GS",        // 部門代碼
  "department_name": "客務部",    // 部門名稱
  "line_user_id": "U123...",      // LINE 使用者 ID
  "line_user_name": "張三",       // LINE 使用者名稱
  "title": "任務標題",
  "description": "任務描述",
  "status": "pending",            // pending, in_progress, completed, cancelled
  "priority": "medium",           // urgent, high, medium, low
  "created_at": ISODate,
  "updated_at": ISODate,
  "due_date": ISODate,            // 截止日期（可選）
  "completed_at": ISODate,        // 完成時間（可選）
  "assigned_to": "user_id",       // 指派給誰（可選）
  "notes": "備註",                // 備註（可選）
  "tags": ["標籤1", "標籤2"],    // 標籤
  "message_id": "...",            // LINE 訊息 ID
  "original_message": "..."       // 原始訊息內容
}
```

## 測試

### 測試 Webhook

使用 curl 或 Postman 測試：

```bash
curl -X POST "http://localhost:8000/api/linebot/webhook/GS" \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: test_signature" \
  -d '{
    "destination": "U1234567890",
    "events": [
      {
        "type": "message",
        "timestamp": 1234567890,
        "source": {
          "type": "user",
          "userId": "U1234567890"
        },
        "replyToken": "test_token",
        "message": {
          "type": "text",
          "id": "123456",
          "text": "緊急處理客戶投訴"
        }
      }
    ]
  }'
```

### 查詢任務

```bash
# 取得客務部所有待處理任務
curl "http://localhost:8000/api/linebot/departments/GS/tasks?status=pending"

# 取得部門統計資訊
curl "http://localhost:8000/api/linebot/departments/GS"
```

## 注意事項

1. **安全性**: 生產環境請確保：
   - 使用 HTTPS
   - 驗證 LINE 簽名
   - 設定適當的 CORS 規則

2. **Webhook 設定**: 
   - 需要公開可訪問的 URL
   - 建議使用 ngrok 進行本地測試
   - LINE 要求 Webhook URL 必須使用 HTTPS

3. **效能考量**:
   - 預設每次查詢限制 50 筆任務
   - 可透過 `limit` 參數調整（最大 200）
   - 建議實作分頁機制

4. **錯誤處理**:
   - 所有 LINE API 錯誤都會被捕獲並記錄
   - 用戶會收到友善的錯誤訊息
   - 系統日誌會記錄詳細錯誤資訊

## 擴展功能

可以考慮添加的功能：

1. **Rich Menu**: 為每個部門設計專屬的快捷功能選單
2. **Flex Message**: 使用更豐富的訊息格式顯示任務資訊
3. **圖文訊息**: 支援圖片、影片等多媒體任務
4. **排程提醒**: 定時推送待處理任務提醒
5. **統計報表**: 部門任務統計與分析
6. **權限管理**: 不同角色的任務查看與處理權限
7. **任務分派**: 自動或手動分派任務給特定人員

## 疑難排解

### 問題：部門初始化失敗

**解決方案**:
1. 檢查 `.env` 檔案中的 TOKEN 和 SECRET 是否正確
2. 確認 MongoDB 連線正常
3. 查看錯誤訊息日誌

### 問題：Webhook 收不到訊息

**解決方案**:
1. 確認 LINE Developers Console 中 Webhook URL 設定正確
2. 檢查 Webhook URL 是否可公開訪問
3. 查看 LINE Developers Console 的 Webhook 測試結果
4. 確認簽名驗證正確

### 問題：訊息發送失敗

**解決方案**:
1. 確認 Access Token 有效
2. 檢查用戶是否已加入好友
3. 確認沒有超過 LINE API 的速率限制

## 文件參考

- [LINE Messaging API 文件](https://developers.line.biz/en/docs/messaging-api/)
- [FastAPI 文件](https://fastapi.tiangolo.com/)
- [MongoDB Beanie 文件](https://beanie-odm.dev/)
