# MongoDB 整合說明

## 📋 已完成的變更

### 1. 安裝套件
已安裝以下 MongoDB 相關套件：
- `pymongo>=4.6.0` - MongoDB Python 驅動
- `motor>=3.3.0` - 非同步 MongoDB 驅動
- `beanie>=1.24.0` - MongoDB ODM (類似 SQLAlchemy)

### 2. 更新的文件

#### [app/core/config.py](app/core/config.py)
新增 MongoDB 配置：
```python
MONGODB_URL: str = "mongodb://localhost:27017"
MONGODB_DB_NAME: str = "tibame_ace_db"
```

#### [app/core/database.py](app/core/database.py)
- 新增 `connect_to_mongodb()` - 連接到 MongoDB
- 新增 `close_mongodb_connection()` - 關閉連接
- 新增 `get_database()` - 取得資料庫實例
- 保留原有的 SQLAlchemy 配置（備用）

#### [app/models/user.py](app/models/user.py)
改用 Beanie Document：
- 從 SQLAlchemy ORM 改為 MongoDB Document
- 支援索引、唯一性約束
- 自動處理 `created_at` 和 `updated_at`

#### [run.py](run.py)
新增應用程式生命週期事件：
- `startup` - 啟動時連接 MongoDB
- `shutdown` - 關閉時斷開連接

#### [requirements.txt](requirements.txt) 和 [.env.example](.env.example)
已更新相關配置

---

## 🚀 快速開始

### 1. 安裝 MongoDB（選擇一種方式）

**選項 A: 使用 Docker（推薦）**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**選項 B: 本地安裝**
- Windows: 下載並安裝 [MongoDB Community Server](https://www.mongodb.com/try/download/community)
- macOS: `brew install mongodb-community`
- Linux: 參考[官方文檔](https://docs.mongodb.com/manual/installation/)

### 2. 設定環境變數
複製 `.env.example` 為 `.env`：
```bash
cp .env.example .env
```

編輯 `.env` 檔案中的 MongoDB 設定：
```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=tibame_ace_db
```

### 3. 測試連接
執行測試腳本：
```bash
python test_mongodb.py
```

### 4. 啟動應用程式
```bash
python run.py
```

---

## 📊 MongoDB vs SQLAlchemy 差異

| 功能 | SQLAlchemy (舊) | Beanie/MongoDB (新) |
|------|-----------------|---------------------|
| 基礎類別 | `Base` | `Document` |
| 主鍵 | `id = Column(Integer, primary_key=True)` | `id: PydanticObjectId` (自動) |
| 索引 | `index=True` | `Indexed(str, unique=True)` |
| 關聯 | `relationship()` | 嵌入或引用 |
| 查詢 | `session.query()` | `await User.find()` |

---

## 💡 使用範例

### 新增使用者
```python
from app.models.user import User

# 建立新使用者
new_user = User(
    username="john_doe",
    email="john@example.com",
    full_name="John Doe",
    hashed_password="hashed_password_here"
)
await new_user.insert()
```

### 查詢使用者
```python
# 查詢單一使用者
user = await User.find_one(User.username == "john_doe")

# 查詢所有使用者
users = await User.find_all().to_list()

# 條件查詢
active_users = await User.find(User.is_active == True).to_list()
```

### 更新使用者
```python
user = await User.find_one(User.username == "john_doe")
user.full_name = "John Updated"
await user.save()
```

### 刪除使用者
```python
user = await User.find_one(User.username == "john_doe")
await user.delete()
```

---

## 🔧 進階配置

### 使用 MongoDB Atlas（雲端）
在 `.env` 中設定：
```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=tibame_ace_db
```

### 連接池配置
可在 `database.py` 中調整：
```python
client = AsyncIOMotorClient(
    settings.MONGODB_URL,
    maxPoolSize=50,
    minPoolSize=10
)
```

---

## 📚 更多資源

- [Beanie 官方文檔](https://beanie-odm.dev/)
- [Motor 官方文檔](https://motor.readthedocs.io/)
- [MongoDB Python 教學](https://www.mongodb.com/docs/drivers/python/)
- [FastAPI + MongoDB 範例](https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/)

---

## ⚠️ 注意事項

1. **保留 SQLAlchemy 配置**：目前同時保留了 SQLAlchemy 設定，方便逐步遷移
2. **非同步操作**：MongoDB 操作需使用 `await`
3. **索引建立**：首次啟動時會自動建立索引
4. **資料遷移**：如需從 SQLite/MySQL 遷移資料，請另外編寫遷移腳本

---

## 🆘 疑難排解

**問題：連接失敗**
- 確認 MongoDB 服務是否運行
- 檢查 `.env` 中的 `MONGODB_URL` 是否正確
- 檢查防火牆設定

**問題：找不到 collection**
- 第一次啟動時 collection 會自動建立
- 確認 `connect_to_mongodb()` 有正常執行

**問題：導入錯誤**
- 確認已安裝所有依賴：`pip install -r requirements.txt`
