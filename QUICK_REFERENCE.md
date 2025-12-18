# 🎯 LINE Bot 整合 - 快速參考卡

> 打印或保存此文件，作為快速參考

## 📌 3 步快速開始

```
1️⃣  python check_integration.py
2️⃣  python init_linebot_departments.py  
3️⃣  python run.py
```

---

## 🔑 核心配置

### .env 檔案必填項 (示例)
```env
APP_NAME=ACE服務管理後台
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=tibame_ace_db

# 12 個部門必須全部配置
GS_ACCESS_TOKEN=...
GS_SECRET=...
# ... 其他 11 個部門
```

### 環境變數名稱
```
{DEPT_CODE}_ACCESS_TOKEN
{DEPT_CODE}_SECRET
```

部門代碼: GS HK CON BP FB CBS FS LUR GAE BB AD LA

---

## 📡 重要 API 端點

### 接收訊息 (Webhook)
```
POST /api/linebot/webhook/{DEPT_CODE}
```

### 查詢任務
```
GET /api/linebot/departments/{DEPT_CODE}/tasks?status=pending
```

### 更新狀態
```
PUT /api/linebot/tasks/{TASK_ID}/status?status=completed&notes=...
```

### 管理介面
```
GET /linebot/dashboard
```

---

## 💾 重要資料庫集合

### Department
```
{code, name, access_token, channel_secret, is_active}
```

### Task
```
{department_code, line_user_id, title, description, 
 status, priority, created_at, ...}
```

---

## 🎯 優先級識別

| 訊息內容 | 優先級 | 圖標 |
|---------|--------|------|
| 含「緊急」「urgent」「立即」「馬上」 | URGENT | 🔴 |
| 含「重要」「high」「優先」 | HIGH | 🟠 |
| 含「低」「low」「不急」 | LOW | 🟢 |
| 其他 (預設) | MEDIUM | 🟡 |

---

## ✅ 任務狀態流

```
pending ──→ in_progress ──→ completed
  ↓                            ↑
  └────── cancelled ───────────┘
```

發送通知時機: 建立時 & 狀態變更時

---

## 🚨 常見錯誤排除

| 錯誤 | 解決方案 |
|------|---------|
| MongoDB 連線失敗 | 確認 mongod 已啟動 |
| 初始化失敗 | 檢查 .env TOKEN 格式 |
| Webhook 未接收 | 驗證簽名、檢查 Webhook URL |
| 訊息發送失敗 | 確認 Token 有效、用戶已加好友 |

---

## 📚 文檔速查

| 文件 | 用途 | 推薦讀者 |
|------|------|--------|
| [LINEBOT_QUICKSTART.md](./LINEBOT_QUICKSTART.md) | 快速上手 | 新手 |
| [LINEBOT_README.md](./LINEBOT_README.md) | 完整說明 | 所有人 |
| [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) | 部署步驟 | 部署人員 |
| [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) | 架構說明 | 開發人員 |
| [COMPLETION_REPORT.md](./COMPLETION_REPORT.md) | 完成報告 | 管理層 |

---

## 🔌 部門代碼表

| 代碼 | 部門名稱 |
|------|----------|
| GS | 客務部 |
| HK | 房務部 |
| CON | 門房諮詢 |
| BP | 烘焙點心房 |
| FB | 餐飲 |
| CBS | 會議宴會 |
| FS | 花房 |
| LUR | 洗衣房與制服室 |
| GAE | 總務工程 |
| BB | 飲料酒吧 |
| AD | 美術設計 |
| LA | 休閒活動部 |

---

## 🛠️ 有用的命令

### 初始化
```bash
python init_linebot_departments.py
```

### 啟動應用
```bash
python run.py
```

### 檢查整合
```bash
python check_integration.py
```

### 查看 API 文檔
```
http://localhost:8000/docs
```

### 管理儀表板
```
http://localhost:8000/linebot/dashboard
```

---

## 📞 聯繫資訊

- 📧 技術問題: 查看文檔 → 檢查日誌 → 查詢 API
- 📖 文檔: 本專案資料夾內所有 .md 檔案
- 🔗 官方資源: 
  - LINE: https://developers.line.biz/
  - FastAPI: https://fastapi.tiangolo.com/
  - MongoDB: https://docs.mongodb.com/

---

## ⭐ 記住的 3 件事

1. **配置 .env** - 必須配置所有 12 個部門
2. **初始化資料庫** - `python init_linebot_departments.py`
3. **設定 Webhook** - LINE Developers Console 中設定

---

## 📊 系統架構速覽

```
LINE 訊息
   ↓
Webhook (/api/linebot/webhook/{CODE})
   ↓
控制器 (驗證簽名、分派事件)
   ↓
服務層 (業務邏輯)
   ↓
資料層 (MongoDB)
   ↓
推送通知 → 管理介面
```

---

## ✨ 核心特性

- ✅ 自動任務建立
- ✅ 優先級識別
- ✅ 實時通知
- ✅ 多部門隔離
- ✅ 管理介面
- ✅ 完整 API

---

## 🎓 學習路徑

1. 閱讀本快速參考卡 (5 分鐘)
2. 執行 3 步快速開始 (10 分鐘)
3. 測試 API 端點 (10 分鐘)
4. 讀取完整文檔 (30 分鐘)
5. 自定義和擴展 (自由時間)

---

**保存此卡以備快速查閱！** 📌

---

最後更新: 2025-12-12 | 版本: 1.0.0
