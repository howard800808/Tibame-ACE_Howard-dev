# ACE服務管理後台 - 開發文檔

> FastAPI MVC 架構後台系統,包含 OAuth2.0 JWT 認證、HTML 頁面渲染、完整的 CRUD 操作

---

## 📚 目錄

1. [專案概述](#專案概述)
2. [架構說明](#架構說明)  
3. [LINE Bot 整合](#line-bot-整合)
4. [專案結構](#專案結構)
5. [快速開始](#快速開始)
6. [開發指南](#開發指南)
7. [API 端點](#api-端點)
8. [環境配置](#環境配置)
9. [技術棧](#技術棧)
10. [常見問題](#常見問題)

---

## 專案概述

ACE服務管理後台採用 **MVC (Model-View-Controller)** 架構,將資料驗證 (Schemas) 與視圖渲染 (Views) 分離:

### 核心特色

- ✅ **分層架構**: Routes → Controllers → Services → Models
- ✅ **LINE Bot 整合**: 支援 12 個部門的自動化任務管理與 Flex Message 互動
- ✅ **OAuth2.0 JWT**: 安全的認證機制,Token 有效期 30 分鐘
- ✅ **權限系統**: 基於角色的存取控制 (admin / manager / user)
- ✅ **前端渲染**: JavaScript 動態載入資料,Token 自動驗證
- ✅ **雙重響應**: API (JSON) + 頁面 (HTML)
- ✅ **自動文檔**: Swagger UI + ReDoc
- ✅ **模組化設計**: Schemas (資料驗證) + Views (頁面渲染)
- ✅ **側邊選單**: 依據使用者權限動態顯示功能列表

### 測試帳號

```
帳號: admin
密碼: admin123
```

### 重要路徑

```
登入頁面: http://localhost:8000/login
儀表板:   http://localhost:8000/dashboard (需登入, 前端驗證 Token)
使用者:   http://localhost:8000/users (需登入, 前端驗證 Token)
API 文檔: http://localhost:8000/docs
健康檢查: http://localhost:8000/api/health
```

### 頁面渲染機制

- 登入頁面: 純前端表單提交,Token 存於 localStorage
- Dashboard/Users: 前端 JavaScript 自動檢查 Token 並呼叫 API 獲取資料
- Token 失效時自動導向登入頁面

---

## 架構說明

### 架構流程圖

```
        ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
        │  API 請求     │         │  頁面請求     │         │  LINE Webhook│
        │  (JSON)      │         │  (HTML)      │         │  (Event)     │
        └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
               │                        │                        │
               ↓                        ↓                        ↓
        ┌────────────────────────────────────────────────────────────────┐
        │                   Routes Layer (路由層)                         │
        │  • API Routes           • Page Routes          • LineBot Routes│
        └──────┬─────────────────────┬───────────────────────┬───────────┘
               │                     │                       │
               ↓                     ↓                       ↓
        ┌─────────────┐       ┌─────────────┐       ┌──────────────────┐
        │ Controllers │       │    Views    │       │ LineBotController│
        │  (業務邏輯)  │       │  (頁面渲染)  │       │   (訊息處理)     │
        └──────┬──────┘       └──────┬──────┘       └────────┬─────────┘
               │                     │                       │
               ↓                     │                       ↓
        ┌─────────────┐              │              ┌──────────────────┐
        │  Services   │              │              │  LineBotService  │
        │(資料存取層)  │              │              │  (Flex Message)  │
        └──────┬──────┘              │              └────────┬─────────┘
               │                     │                       │
               ↓                     │                       ↓
        ┌─────────────┐              │              ┌──────────────────┐
        │   Models    │              │              │      Models      │
        │ (ORM 模型)   │              │              │ (Task/Department)│
        └──────┬──────┘              │              └────────┬─────────┘
               │                     │                       │
               ↓                     │                       ↓
        ┌─────────────┐              │              ┌──────────────────┐
        │  Database   │              │              │     Database     │
        └──────┬──────┘              │              └──────┬───────────┘
               │                     │                     │

---

## LINE Bot 整合

本系統已完整整合 12 個飯店部門的 LINE Bot 功能，並全面升級至 **LINE Bot SDK v3**，提供更穩定且強大的 Messaging API 支援。

詳細說明請參考：[LineBot.md](LineBot.md)

### 主要功能
- **SDK v3 架構**: 採用最新的 LINE Bot SDK v3，支援異步操作與更嚴謹的型別檢查。
- **統一 Webhook**: 所有部門共用單一 Webhook URL，簡化管理。
- **Flex Message**: 使用豐富的互動式卡片介面，取代傳統文字指令。
- **自動化流程**: 支援任務指派、狀態更新、完成回報等完整生命週期。
- **多部門支援**: 獨立管理 GS, HK, FB 等 12 個部門的任務與權限。
               ↓                     ↓
        ┌─────────────┐       ┌─────────────┐
        │   Schemas   │       │  Templates  │
        │ (資料驗證)   │       │ (HTML 模板) │
        └──────┬──────┘       └──────┬──────┘
               │                     │
               ↓                     ↓
        ┌────────────────────────────────────────┐
        │           Client (客戶端)               │
        │  • JSON Response (API)                 │
        │  • HTML Page (Web)                     │
        └────────────────────────────────────────┘
```

### 各層職責

| 層級 | 位置 | 職責 | 範例 |
|------|------|------|------|
| **Routes** | `app/routes/` | 接收請求、參數驗證、調用 Controller | `auth_routes.py` |
| **Controllers** | `app/controllers/` | 業務邏輯、錯誤處理、調用 Service | `auth_controller.py` |
| **Services** | `app/services/` | 資料庫 CRUD、資料處理 | `user_service.py` |
| **Models** | `app/models/` | ORM 模型、資料表定義 | `user.py` |
| **Schemas** | `app/schemas/` | API 資料驗證 (Pydantic) | `user_schema.py` |
| **Views** | `app/views/` | HTML 頁面渲染 (Jinja2) | `dashboard_view.py` |
| **Templates** | `templates/` | HTML 模板 + JavaScript | `login.html`, `dashboard.html` |

---

## 專案結構

```
www/
├── app/
│   ├── controllers/      # 🎮 業務邏輯層
│   │   ├── auth_controller.py
│   │   ├── user_controller.py
│   │   ├── system_controller.py
│   │   ├── linebot_controller.py  # (LINE Bot Webhook 處理)
│   │   └── task_controller.py     # (任務管理邏輯)
│   │
│   ├── models/          # 🗄️ ORM 模型層
│   │   ├── user.py      # (含 role 欄位: admin/manager/user)
│   │   ├── task.py      # (任務資料模型)
│   │   └── department.py # (部門設定模型)
│   │
│   ├── schemas/         # 📋 API 資料驗證
│   │   ├── auth_schema.py
│   │   ├── user_schema.py
│   │   ├── task_schema.py
│   │   └── linebot_schema.py
│   │
│   ├── views/           # 👁️ 頁面渲染層
│   │   ├── auth_view.py
│   │   ├── dashboard_view.py
│   │   └── user_view.py
│   │
│   ├── routes/          # 🛣️ API 路由層
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── system_routes.py
│   │   ├── linebot_routes.py      # (LINE Bot 相關路由)
│   │   └── task_routes.py         # (任務相關路由)
│   │
│   ├── services/        # ⚙️ 資料存取層
│   │   ├── user_service.py
│   │   ├── task_service.py
│   │   └── linebot_service.py     # (LINE Bot 業務邏輯 SDK v3)
│   │
│   └── core/            # 🔧 核心配置
│       ├── config.py
│       ├── security.py
│       ├── database.py
│       └── dependencies.py
│
├── templates/           # 🎨 HTML 模板
│   ├── login.html
│   ├── dashboard.html
│   └── users.html
│
├── static/              # 📁 靜態資源
│   └── style.css
│
├── run.py               # 🚀 程式入口
├── requirements.txt     # 📦 依賴套件
├── README.md            # 📖 專案說明文檔
├── .env                 # 🔐 環境變數
└── Dockerfile          # 🐳 Docker 配置
```

---

## 快速開始

### 1. 安裝依賴

```powershell
pip install -r requirements.txt
```

### 2. 設定環境變數

```powershell
# 複製範例檔案
cp .env.example .env

# 編輯 .env,至少修改:
# - SECRET_KEY (必須更換為隨機字串)
# - DATABASE_URL (如需使用 MySQL/PostgreSQL)
```

### 3. 啟動服務

```powershell
python run.py
```

### 4. 訪問系統

- **登入頁面**: http://localhost:8000/login
- **API 文檔**: http://localhost:8000/docs
- **健康檢查**: http://localhost:8000/api/health

### 5. 建立使用者或使用預設帳號

**預設帳號** (如果資料庫已有 admin 使用者):
```
帳號: admin
密碼: admin123
角色: admin (擁有所有權限)
```

**或使用 API 註冊新使用者**:
訪問 Swagger UI (`/docs`),使用 `POST /api/auth/register`:

```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123",
  "full_name": "新使用者",
  "role": "user"
}
```

**角色說明**:
- `admin`: 系統管理員 (所有權限)
- `manager`: 經理 (訂單管理權限)
- `user`: 一般使用者 (基本功能)

### 6. 登入測試

1. 訪問 http://localhost:8000/login
2. 輸入帳號密碼
3. 登入成功後自動跳轉到 `/dashboard`
4. 觀察側邊選單根據角色顯示不同功能

---

## 開發指南

### 新增功能模組流程 (以產品管理為例)

#### Step 1: 建立 Model

```python
# app/models/product.py
from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
```

#### Step 2: 建立 Schema

```python
# app/schemas/product_schema.py
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

class Product(BaseModel):
    id: int
    name: str
    price: float
    model_config = {"from_attributes": True}
```

#### Step 3: 建立 Service

```python
# app/services/product_service.py
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product_schema import ProductCreate

class ProductService:
    @staticmethod
    def create_product(db: Session, product: ProductCreate):
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
```

#### Step 4: 建立 Controller

```python
# app/controllers/product_controller.py
from fastapi import HTTPException
from app.services.product_service import product_service

class ProductController:
    @staticmethod
    def create_product(product_data, db):
        return product_service.create_product(db, product_data)
```

#### Step 5: 建立 Routes

```python
# app/routes/product_routes.py
from fastapi import APIRouter, Depends
from app.controllers.product_controller import product_controller
from app.schemas.product_schema import Product, ProductCreate

router = APIRouter(prefix="/products", tags=["產品管理"])

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return product_controller.create_product(product, db)
```

#### Step 6: 註冊路由

```python
# run.py
from app.routes import product_router

app.include_router(product_router, prefix="/api")
```

### 開發檢查清單

- [ ] Model: 定義 `__tablename__` 和必要欄位
- [ ] Schema: 包含 Create、Update、Response Schema
- [ ] Service: 實作完整 CRUD 方法
- [ ] Controller: 包含錯誤處理
- [ ] Routes: 加上詳細 docstring
- [ ] 在 `__init__.py` 導出新模組
- [ ] 在 `run.py` 註冊路由
- [ ] 測試 API 是否正常運作

### Git 協作流程

```bash
git checkout -b feature/product-management
# 開發功能...
git add .
git commit -m "feat: 新增產品管理功能"
git push origin feature/product-management
# 建立 Pull Request
```

**Commit 規範**: `feat:` 新功能 | `fix:` 修復 | `docs:` 文檔 | `refactor:` 重構

---

## API 端點

### 認證 API (`/api/auth`)

| 方法 | 端點 | 說明 | 認證 |
|------|------|------|------|
| POST | `/api/auth/register` | 註冊新使用者 | ❌ |
| POST | `/api/auth/login` | 登入 (OAuth2) | ❌ |
| POST | `/api/auth/login/json` | 登入 (JSON) | ❌ |

### 使用者 API (`/api/users`)

| 方法 | 端點 | 說明 | 認證 |
|------|------|------|------|
| GET | `/api/users/me` | 取得當前使用者 | ✅ |
| PUT | `/api/users/me` | 更新當前使用者 | ✅ |
| GET | `/api/users/` | 取得使用者列表 | ✅ |

### 系統 API (`/api`)

| 方法 | 端點 | 說明 | 認證 |
|------|------|------|------|
| GET | `/api/health` | 健康檢查 | ❌ |
| GET | `/api/error/404` | 404 錯誤頁面 | ❌ |
| GET | `/api/error/500` | 500 錯誤頁面 | ❌ |

### 頁面路由

| 路徑 | 說明 | 認證 | 渲染方式 |
|------|------|------|----------|
| `/login` | 登入頁面 | ❌ | 靜態 HTML |
| `/dashboard` | 儀表板 | ✅ | 前端 JS 動態載入 |
| `/users` | 使用者列表 | ✅ | 前端 JS 動態載入 |

### 權限系統

系統支援三種使用者角色:

| 角色 | 說明 | 可見功能 |
|------|------|----------|
| **admin** | 系統管理員 | 所有功能 (角色管理、廠房管理、機台管理、品料管理、訂單管理、工作報告) |
| **manager** | 經理 | 訂單管理、工作報告 |
| **user** | 一般使用者 | 儀表板、人員管理、工作報告 |

### 側邊選單功能列表

**主選單** (所有角色):
- 🏠 儀表板
- 👥 人員管理

**管理功能** (僅 admin):
- 🔐 角色管理
- 🏭 廠房管理
- ⚙️ 機台管理
- 📦 品料管理

**訂單管理** (admin + manager):
- 🛒 訂單管理
- 📋 開工列表ing
- 📅 製令單排程
- ✅ 製令單Close

**工作報告** (所有角色):
- 📊 報工單ALL
- 📝 報工單

---

## 環境配置

### 核心配置

```env
# 應用程式
APP_NAME=FastAPI Admin Backend
VERSION=1.0.0
DEBUG=True

# JWT 認證
SECRET_KEY=banana-feel-good  # ⚠️ 生產環境務必更換
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 資料庫
DATABASE_URL=sqlite:///./admin.db
# DATABASE_URL=mysql+pymysql://user:password@host:3306/database

# CORS
BACKEND_CORS_ORIGINS=["*"]  # 生產環境改為指定網域
```

### 安全注意事項

1. **不要提交 `.env` 到 Git**
2. **務必更換 SECRET_KEY**:
   ```bash
   openssl rand -hex 32
   ```
3. **生產環境必須設定**:
   ```env
   DEBUG=False
   SECRET_KEY=<隨機密鑰>
   BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
   ```

---

## 技術棧

### 核心框架

- **FastAPI** 0.109.0 - Web 框架
- **Uvicorn** 0.27.0 - ASGI 服務器
- **Pydantic** 2.0+ - 資料驗證
- **SQLAlchemy** 2.0+ - ORM
- **Jinja2** 3.1+ - 模板引擎

### 安全性

- **python-jose** 3.3+ - JWT Token
- **bcrypt** 5.0+ - 密碼加密
- **python-multipart** - 表單處理

### 資料庫

- **SQLite** - 開發環境 (預設)
- **MySQL** - 生產環境 (支援)
- **PostgreSQL** - 生產環境 (支援)

---

## 常見問題

### Q: 如何切換資料庫為 MySQL?

```env
# .env
DATABASE_URL=mysql+pymysql://username:password@host:3306/database
```

```bash
pip install pymysql cryptography
```

### Q: Token 過期怎麼辦?

前端會自動檢測 Token 失效並導向登入頁面。手動重新登入即可獲取新 Token。

### Q: 如何修改使用者角色?

目前需要直接修改資料庫:
```sql
UPDATE users SET role = 'admin' WHERE username = 'username';
```

未來版本會在 UI 提供角色管理功能。

### Q: 如何新增欄位到 User 模型?

1. 修改 `app/models/user.py` 新增欄位
2. 修改 `app/schemas/user_schema.py` 新增欄位
3. 使用 ALTER TABLE 或重建資料庫

範例:
```sql
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
```

### Q: 頁面顯示 "Not authenticated" 怎麼辦?

這表示 Token 驗證失敗,可能原因:
1. Token 已過期 (30分鐘有效期)
2. Token 格式錯誤
3. localStorage 中沒有 Token

解決方式: 重新登入即可。

### Q: 如何查看資料庫內容?

```bash
# SQLite
sqlite3 admin.db
SELECT * FROM users;

# MySQL
mysql -h 114.32.4.178 -u ace_web -p ace
SELECT * FROM users;
```

### Q: 如何部署到 Docker?

```bash
docker build -t ace-backend .
docker run -d -p 8000:8000 --name ace-backend ace-backend
```

---

## 程式碼範例

### Python 客戶端

```python
import requests

BASE_URL = "http://localhost:8000"

# 登入
response = requests.post(
    f"{BASE_URL}/api/auth/login/json",
    json={"username": "admin", "password": "admin123"}
)
token = response.json()["access_token"]

# 使用 Token
headers = {"Authorization": f"Bearer {token}"}
user = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
print(user.json())
```

### JavaScript 客戶端 (前端範例)

```javascript
const BASE_URL = 'http://localhost:8000';

// 登入
const loginResponse = await fetch(`${BASE_URL}/api/auth/login/json`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: 'admin123' })
});
const { access_token } = await loginResponse.json();

// 儲存到 localStorage
localStorage.setItem('access_token', access_token);

// 使用 Token 獲取使用者資料
const token = localStorage.getItem('access_token');
const userResponse = await fetch(`${BASE_URL}/api/users/me`, {
  headers: { 'Authorization': `Bearer ${token}` }
});

if (!userResponse.ok) {
  // Token 失效,重新登入
  window.location.href = '/login';
} else {
  const user = await userResponse.json();
  console.log(user.role); // 取得使用者角色
}
```

### cURL

```bash
# 登入
curl -X POST "http://localhost:8000/api/auth/login/json" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 使用 Token
TOKEN="your_token_here"
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 測試工具

### LLM 連線測試 (`test_LLM.py`)

此腳本用於測試與 LLM 服務 (`https://llm.89.com.tw`) 的連線與互動。

**功能：**
1. 建立 Session
2. 發送測試訊息 ("你好，請幫我查詢台北的天氣")
3. 生成 GET 模式的 URL (用於除錯)
4. 執行 POST 請求並顯示回應結果

**使用方式：**

```bash
python test_LLM.py
```

**主要變數：**
- `BASE_URL`: LLM 服務位址
- `APP_NAME`: 應用程式名稱 (預設: "agents")
- `USER_ID`: 使用者 ID (預設: "wilsonsu")

---

## 授權

本專案採用 **MIT 授權**。

---

## 更新日誌

### v1.1.0 (2025-12-10)
- ✅ 新增權限系統 (admin / manager / user)
- ✅ 前端動態渲染機制 (JavaScript + localStorage)
- ✅ 側邊功能選單 (依角色顯示)
- ✅ Token 自動驗證與過期處理
- ✅ User model 新增 role 欄位
- ✅ Dashboard 和 Users 頁面改為前端渲染

### v1.0.0 (初始版本)
- ✅ MVC 架構建立
- ✅ OAuth2.0 JWT 認證
- ✅ 基本 CRUD 操作
- ✅ Swagger API 文檔

---

**祝您開發順利！🚀**
