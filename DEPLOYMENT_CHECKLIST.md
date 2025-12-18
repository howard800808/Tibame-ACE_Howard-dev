# 📋 LINE Bot 12 部門整合 - 部署清單

## ✅ 整合完成項目

### 1. 資料模型層 ✔️
- [x] `app/models/department.py` - 部門配置資料模型
- [x] `app/models/task.py` - 任務管理資料模型（支援優先級、狀態、標籤）

### 2. 資料驗證層 ✔️
- [x] `app/schemas/linebot_schema.py` - 請求/回應資料結構
  - TaskCreate, TaskUpdate, TaskResponse
  - LineBotWebhookEvent, LineBotWebhookRequest
  - DepartmentCreate, DepartmentUpdate, DepartmentResponse

### 3. 業務邏輯層 ✔️
- [x] `app/services/linebot_service.py` - LINE Bot 服務
  - 訊息接收和處理
  - 優先級自動識別
  - 任務狀態管理
  - 用戶通知推送
  - 部門統計資訊

### 4. 控制層 ✔️
- [x] `app/controllers/linebot_controller.py` - Webhook 控制器
  - Webhook 簽名驗證
  - 事件分發和處理
  - 訊息事件處理
  - 好友追蹤/取消追蹤事件

### 5. 路由層 ✔️
- [x] `app/routes/linebot_routes.py` - API 路由定義
  - 12 個獨立的 Webhook 端點
  - 任務查詢 API
  - 任務狀態更新 API
  - 廣播訊息 API
  - 部門列表 API

### 6. 檢視層 ✔️
- [x] `app/views/linebot_view.py` - 管理介面視圖
  - LINE Bot 儀表板
  - 部門任務管理頁面
- [x] `templates/linebot_dashboard.html` - 儀表板 HTML

### 7. 配置管理 ✔️
- [x] `app/core/config.py` - 添加 12 部門 TOKEN 和 SECRET
- [x] `app/core/database.py` - 添加 Department 和 Task 模型初始化
- [x] `run.py` - 註冊 LINE Bot 路由和初始化服務

### 8. 初始化腳本 ✔️
- [x] `init_linebot_departments.py` - 一鍵初始化所有部門配置

### 9. 文檔 ✔️
- [x] `LINEBOT_README.md` - 完整使用說明
- [x] `LINEBOT_QUICKSTART.md` - 快速開始指南
- [x] `PROJECT_STRUCTURE.md` - 專案結構說明
- [x] `DEPLOYMENT_CHECKLIST.md` - 部署清單（本文件）

---

## 🚀 部署步驟

### Step 1: 環境準備
```bash
# 1.1 確認 Python 版本 (3.8+)
python --version

# 1.2 建立虛擬環境 (如未建立)
python -m venv .venv

# 1.3 啟用虛擬環境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 1.4 安裝依賴
pip install -r requirements.txt
```

### Step 2: 資料庫準備
```bash
# 2.1 確認 MongoDB 已啟動
# 檢查 MongoDB 是否在運行
# Windows: 檢查 MongoDB 服務
# macOS: brew services list | grep mongodb
# Linux: systemctl status mongod

# 2.2 測試 MongoDB 連線
mongosh  # 或 mongo (舊版本)
# 應該能進入 MongoDB shell
```

### Step 3: 環境變數配置
```bash
# 3.1 確認 .env 檔案已配置所有 12 部門
# 檢查清單：
# ✓ GS_ACCESS_TOKEN & GS_SECRET
# ✓ HK_ACCESS_TOKEN & HK_SECRET
# ✓ CON_ACCESS_TOKEN & CON_SECRET
# ✓ BP_ACCESS_TOKEN & BP_SECRET
# ✓ FB_ACCESS_TOKEN & FB_SECRET
# ✓ CBS_ACCESS_TOKEN & CBS_SECRET
# ✓ FS_ACCESS_TOKEN & FS_SECRET
# ✓ LUR_ACCESS_TOKEN & LUR_SECRET
# ✓ GAE_ACCESS_TOKEN & GAE_SECRET
# ✓ BB_ACCESS_TOKEN & BB_SECRET
# ✓ AD_ACCESS_TOKEN & AD_SECRET
# ✓ LA_ACCESS_TOKEN & LA_SECRET

# 3.2 驗證 .env 格式
# 使用文字編輯器打開 .env，確保：
# - 沒有額外空格
# - TOKEN 和 SECRET 格式正確
# - 沒有引號包圍 Token/Secret
```

### Step 4: 初始化部門資料
```bash
# 4.1 運行初始化腳本
python init_linebot_departments.py

# 4.2 檢查輸出
# 應該看到每個部門的建立/更新成功訊息
# 例如：
# ✓ GS - 客務部: 建立成功
# ✓ HK - 房務部: 建立成功
# ... 等等

# 4.3 驗證資料庫
# 進入 MongoDB
mongosh
# 選擇資料庫
use tibame_ace_db
# 查詢部門集合
db.departments.find().pretty()
# 應該看到 12 個部門記錄
```

### Step 5: 應用程式啟動
```bash
# 5.1 啟動 FastAPI 應用
python run.py

# 5.2 檢查啟動訊息
# 應該看到：
# ✓ 成功連接到 MongoDB: mongodb://localhost:27017
# ✓ Beanie 初始化完成
# ✓ 初始化部門 GS (客務部) LINE Bot
# ✓ 初始化部門 HK (房務部) LINE Bot
# ... 其他部門
# INFO:     Uvicorn running on http://0.0.0.0:8000

# 5.3 訪問應用
# 打開瀏覽器進入：http://localhost:8000
# 查看 API 文檔：http://localhost:8000/docs
```

### Step 6: LINE Developers 設定

#### 對於每個部門（以 GS 為例）：

1. **登入 LINE Developers**
   - 進入 https://developers.line.biz/

2. **選擇 Messaging API Channel**
   - 選擇對應的部門 Channel

3. **設定 Webhook URL**
   - 進入 "Channel settings" → "Messaging API"
   - 找到 "Webhook URL"
   - 設定為：`https://your-domain.com/api/linebot/webhook/GS`
   - 點擊 "Verify" 驗證連線
   - 應該看到 "Webhook URL verification succeeded"

4. **啟用 Webhook**
   - 勾選 "Use webhook" ✓
   - 按下 "Save"

5. **測試 Webhook**
   - 在 "Webhook" 區域點擊 "Test" 按鈕
   - 應該看到 "TEST SUCCESSFUL" 訊息

#### 本地測試 (使用 ngrok)：

```bash
# 6.1 下載並安裝 ngrok
# 訪問 https://ngrok.com/download

# 6.2 啟動 ngrok 隧道
ngrok http 8000
# 會顯示公開 URL，例如：
# https://xxxx-xx-xxx-xxx-xx.ngrok.io

# 6.3 在 LINE Developers 設定 Webhook
# Webhook URL: https://xxxx-xx-xxx-xxx-xx.ngrok.io/api/linebot/webhook/GS

# 6.4 測試訊息
# 使用 LINE 應用發送訊息到對應部門的 Bot
# 應該在 MongoDB 看到新的任務記錄
```

### Step 7: 功能驗證

#### A. Webhook 測試
```bash
# 使用 curl 模擬 LINE 訊息
curl -X POST "http://localhost:8000/api/linebot/webhook/GS" \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: test" \
  -d '{
    "destination": "U1234567890",
    "events": [
      {
        "type": "message",
        "timestamp": 1234567890,
        "source": {"type": "user", "userId": "U1234567890"},
        "replyToken": "test_token",
        "message": {
          "type": "text",
          "id": "123456",
          "text": "緊急：客戶投訴"
        }
      }
    ]
  }'
```

#### B. API 端點測試
```bash
# 查詢部門資訊
curl "http://localhost:8000/api/linebot/departments/GS"

# 查詢任務列表
curl "http://localhost:8000/api/linebot/departments/GS/tasks?status=pending"

# 查詢所有部門
curl "http://localhost:8000/api/linebot/departments"
```

#### C. 資料庫驗證
```bash
# 進入 MongoDB
mongosh
use tibame_ace_db

# 查詢部門
db.departments.find().pretty()

# 查詢任務
db.tasks.find({department_code: "GS"}).pretty()

# 查詢特定狀態的任務
db.tasks.find({department_code: "GS", status: "pending"}).pretty()
```

---

## 🔍 驗收測試清單

### 資料庫層
- [ ] MongoDB 連線正常
- [ ] Department 集合存在且有 12 筆記錄
- [ ] Task 集合已建立
- [ ] 索引已正確建立

### 應用層
- [ ] 應用程式正常啟動
- [ ] 所有 12 個部門的 LINE Bot 已初始化
- [ ] FastAPI 文檔頁面可訪問 (/docs)

### 業務邏輯
- [ ] Webhook 簽名驗證正常
- [ ] 收到訊息時自動建立 Task
- [ ] 優先級自動識別正確
- [ ] 用戶收到確認訊息

### API 端點
- [ ] 所有 API 端點都可訪問
- [ ] 任務查詢結果正確
- [ ] 任務狀態更新正常
- [ ] 廣播訊息成功發送

### 管理介面
- [ ] 儀表板頁面正常顯示
- [ ] 部門卡片顯示正確資訊
- [ ] 統計數據正確更新

### LINE 整合
- [ ] 所有 12 個部門的 Webhook URL 已設定
- [ ] 所有部門都能收到訊息
- [ ] 任務狀態變更時推送通知正確

---

## ⚠️ 常見問題排除

### 問題：MongoDB 連線失敗
**解決方案：**
```bash
# 1. 檢查 MongoDB 是否在運行
# Windows: 檢查 MongoDB 服務
# macOS: brew services list | grep mongodb
# Linux: systemctl status mongod

# 2. 檢查連線字串
# 確認 .env 中的 MONGODB_URL 正確
# 預設值：mongodb://localhost:27017

# 3. 測試連線
mongosh
```

### 問題：初始化失敗
**解決方案：**
```bash
# 1. 檢查 .env 是否正確配置
# 確保沒有縺字或格式錯誤

# 2. 檢查 TOKEN 格式
# TOKEN 不應包含引號

# 3. 查看詳細錯誤訊息
python init_linebot_departments.py
# 查看是否有 404 或連線錯誤
```

### 問題：Webhook 收不到訊息
**解決方案：**
```bash
# 1. 驗證 Webhook URL
# 確認 LINE Developers Console 中的設定正確

# 2. 檢查簽名驗證
# 確認 X-Line-Signature 正確

# 3. 查看應用日誌
# 運行時檢查是否有錯誤訊息

# 4. 測試 ngrok 連線（本地測試）
# 確認 ngrok 仍在運行
```

### 問題：訊息發送失敗
**解決方案：**
```bash
# 1. 驗證 Access Token
# 確認 .env 中的 TOKEN 正確

# 2. 檢查用戶狀態
# 確認用戶已加入 Bot 好友

# 3. 檢查 LINE API 限制
# 確認沒有超過速率限制
```

---

## 📞 支援資源

- 📖 [完整文檔](./LINEBOT_README.md)
- 🚀 [快速開始](./LINEBOT_QUICKSTART.md)
- 🏗️ [專案結構](./PROJECT_STRUCTURE.md)
- 📚 [LINE Messaging API 文檔](https://developers.line.biz/en/docs/messaging-api/)
- 🔧 [FastAPI 文檔](https://fastapi.tiangolo.com/)
- 🗄️ [Beanie ODM](https://beanie-odm.dev/)

---

## ✨ 部署完成後的下一步

### 推薦優化項目
1. **添加日誌系統** - 記錄所有 Webhook 事件
2. **實裝 Rich Menu** - 為每個部門設計快捷菜單
3. **任務分派系統** - 自動或手動分派任務
4. **統計報表** - 生成部門績效分析
5. **天氣整合** - 從中央氣象署 API 獲取天氣資訊

### 安全加固
1. **HTTPS 配置** - 確保所有通訊都已加密
2. **速率限制** - 防止濫用 API
3. **權限管理** - 實裝基於角色的訪問控制
4. **金鑰輪轉** - 定期更新 LINE Bot Token

---

**祝部署順利！如有問題，請參考相關文檔或聯繫技術團隊。** 🎉
