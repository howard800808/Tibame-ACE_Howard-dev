# MBTI 影片分析工具 - 完整架構文檔

## 1️⃣ 系統架構概覽

```
┌─────────────────────────────────────────────────────────────┐
│                    使用者瀏覽器                              │
│                  (HTML + JavaScript)                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │     FastAPI 應用 (MVC 架構)         │
        │         (run.py)                   │
        └────────┬───────────────────────────┘
                 │
    ┌────────────┴──────────┬─────────────┐
    ▼                       ▼             ▼
┌─────────┐           ┌──────────┐   ┌────────┐
│  Routes │           │ Views    │   │ Controllers
│         │           │          │   │ (MBTI)
└────┬────┘           └──────────┘   └────┬───┘
     │                                     │
     │ Routes: /api/mbti/analyze          │
     │         /mbti                      │
     │                                     ▼
     │                            ┌──────────────────┐
     │                            │ mbti_controller  │
     │                            │                  │
     │                            │ • 檔案驗證        │
     │                            │ • 臨時檔案管理    │
     │                            │ • 呼叫服務層      │
     │                            └────────┬─────────┘
     │                                     │
     │                                     ▼
     │                            ┌──────────────────┐
     │                            │ mbti_service     │
     │                            │                  │
     │                            │ • 視頻幀提取      │
     │                            │ • Base64 編碼    │
     │                            │ • AI 預測         │
     │                            │ • 結果解析        │
     │                            └────────┬─────────┘
     │                                     │
     │                                     ▼
     │                            ┌──────────────────┐
     │                            │ Claude API       │
     │                            │ (Anthropic)      │
     │                            └──────────────────┘
     │
     ▼
    返回 JSON 結果
```

---

## 2️⃣ 檔案樹狀結構

```
Team_project/
│
├── 📄 run.py                           # ✏️ 已更新 - FastAPI 主應用
│                                       #   • 導入 mbti_router
│                                       #   • 導入 mbti_view
│                                       #   • 註冊 /mbti 頁面路由
│
├── 📄 requirements.txt                 # ✏️ 已更新
│                                       #   + opencv-python>=4.8.0
│                                       #   + numpy>=1.24.0
│
├── 📁 app/
│   │
│   ├── 📁 core/
│   │   └── 📄 config.py               # ✏️ 已更新
│   │                                   #   + OPENAI_API_KEY
│   │                                   #   + OPENAI_MODEL
│   │
│   ├── 📁 controllers/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 auth_controller.py
│   │   ├── 📄 system_controller.py
│   │   ├── 📄 user_controller.py
│   │   └── 📄 mbti_controller.py       # 🆕 新增
│   │                                   #   • MBTIController 類別
│   │                                   #   • analyze_video() 方法
│   │
│   ├── 📁 routes/
│   │   ├── 📄 __init__.py              # ✏️ 已更新
│   │   ├── 📄 auth_routes.py
│   │   ├── 📄 system_routes.py
│   │   ├── 📄 user_routes.py
│   │   └── 📄 mbti_routes.py           # 🆕 新增
│   │                                   #   • POST /api/mbti/analyze
│   │
│   ├── 📁 services/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 user_service.py
│   │   └── 📄 mbti_service.py          # 🆕 新增
│   │                                   #   • MBTIService 類別
│   │                                   #   • analyze_video_frames()
│   │                                   #   • predict_mbti()
│   │
│   ├── 📁 views/
│   │   ├── 📄 __init__.py              # ✏️ 已更新
│   │   ├── 📄 auth_view.py
│   │   ├── 📄 dashboard_view.py
│   │   ├── 📄 user_view.py
│   │   └── 📄 mbti_view.py             # 🆕 新增
│   │                                   #   • MBTIView 類別
│   │                                   #   • mbti_page() 方法
│   │
│   └── 📁 models/
│       ├── 📄 __init__.py
│       └── 📄 user.py
│
├── 📁 templates/
│   ├── 📄 login.html
│   ├── 📄 dashboard.html
│   ├── 📄 users.html
│   └── 📄 mbti.html                    # 🆕 新增 - 前端頁面
│                                       #   • 拖拽上傳
│                                       #   • 進度顯示
│                                       #   • 結果展示
│
├── 📁 static/
│   └── 📄 style.css
│
├── 📄 MBTI_SETUP.md                    # 🆕 新增 - 快速設置指南
├── 📄 MBTI_ANALYSIS_GUIDE.md           # 🆕 新增 - 詳細使用指南
└── 📄 test_mbti_integration.py         # 🆕 新增 - 集成測試
```

---

## 3️⃣ 資料流程

### 請求流程 (Request Flow)

```
1. 使用者訪問 /mbti
   ↓
2. FastAPI 匹配路由: @app.get("/mbti")
   ↓
3. 呼叫 mbti_view.mbti_page(request)
   ↓
4. 返回 templates/mbti.html
   ↓
5. 瀏覽器加載 HTML、CSS、JavaScript
```

### 分析流程 (Analysis Flow)

```
1. 使用者在前端頁面上傳影片
   ↓
2. JavaScript 驗證檔案
   ↓
3. FormData 上傳到 POST /api/mbti/analyze
   ↓
4. mbti_controller.analyze_video() 接收
   ├─ 驗證檔案類型 (video/mp4, video/mov 等)
   ├─ 驗證檔案大小 (< 500MB)
   └─ 保存到臨時目錄
   ↓
5. 呼叫 mbti_service.predict_mbti()
   ├─ analyze_video_frames() 提取 5 個幀
   │  └─ 使用 OpenCV (cv2) 讀取影片
   │  └─ 調整影像大小
   │  └─ 編碼為 Base64
   │
   └─ 調用 Claude API
      ├─ 發送視頻幀 + 提示詞
      ├─ Claude 分析人物行為
      └─ 返回 JSON 結果
   ↓
6. 結果返回給前端
   ├─ MBTI 類型
   ├─ 信心度
   ├─ 四維度分析
   ├─ 行為特徵
   └─ 建議
   ↓
7. JavaScript 渲染結果
   ├─ 更新 MBTI 類型顯示
   ├─ 填充信心度條
   ├─ 建立分析卡片
   ├─ 顯示特徵標籤
   └─ 顯示建議文字
   ↓
8. 清理臨時檔案
```

---

## 4️⃣ 核心類別和方法

### MBTIService (app/services/mbti_service.py)

```python
class MBTIService:
    """MBTI 預測服務"""
    
    def __init__(self):
        """初始化 Claude API 客戶端"""
        self.client = OpenAI(api_key=...)
        
    def analyze_video_frames(
        self,
        video_path: str,
        num_frames: int = 5
    ) -> List[str]:
        """
        從影片中提取關鍵幀
        
        輸入: 影片路徑
        輸出: Base64 編碼的影像清單
        """
        
    def predict_mbti(self, video_path: str) -> Dict:
        """
        使用 Claude 分析並預測 MBTI
        
        輸入: 影片路徑
        輸出: {
            mbti_type: "ISFJ",
            confidence: 85,
            analysis: {...},
            behavioral_traits: [...],
            recommendations: "..."
        }
        """
        
    def _parse_response_to_json(self, response_text: str) -> Dict:
        """解析 API 回應"""
```

### MBTIController (app/controllers/mbti_controller.py)

```python
class MBTIController:
    """MBTI 控制層"""
    
    @staticmethod
    async def analyze_video(file: UploadFile) -> Dict:
        """
        1. 驗證檔案類型
        2. 驗證檔案大小
        3. 保存臨時檔案
        4. 呼叫服務層分析
        5. 返回結果
        6. 清理臨時檔案
        """
```

### MBTIView (app/views/mbti_view.py)

```python
class MBTIView:
    """MBTI 視圖層"""
    
    @staticmethod
    async def mbti_page(request: Request) -> HTMLResponse:
        """渲染 MBTI 分析頁面"""
```

---

## 5️⃣ API 請求和回應

### 請求

```http
POST /api/mbti/analyze HTTP/1.1
Host: localhost:8000
Content-Type: multipart/form-data; boundary=----Boundary

------Boundary
Content-Disposition: form-data; name="file"; filename="video.mp4"
Content-Type: video/mp4

[影片二進制資料]
------Boundary--
```

### 成功回應 (200 OK)

```json
{
  "success": true,
  "data": {
    "mbti_type": "ISFJ",
    "confidence": 85,
    "analysis": {
      "introversion_extroversion": {
        "type": "I",
        "description": "表現出內向傾向，傾向於反思和獨處...",
        "score": 80
      },
      "sensing_intuition": {
        "type": "S",
        "description": "注重現實和細節，務實的方式...",
        "score": 75
      },
      "thinking_feeling": {
        "type": "F",
        "description": "情感導向的決策，關注他人感受...",
        "score": 85
      },
      "judging_perceiving": {
        "type": "J",
        "description": "有組織和計劃性，喜歡有序...",
        "score": 80
      }
    },
    "behavioral_traits": [
      "細心",
      "負責任",
      "善於傾聽",
      "實際",
      "可靠",
      "有同情心"
    ],
    "recommendations": "ISFJ 類型適合需要細心、組織和人際關係技能的工作..."
  }
}
```

### 錯誤回應

```json
{
  "success": false,
  "error": "不支援的影片格式: video/unknown"
}
```

---

## 6️⃣ 配置管理

### app/core/config.py

```python
class Settings(BaseSettings):
    # ... 現有配置 ...
    
    # OpenAI 配置 (新增)
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-vision-preview"
```

### .env 檔案範例

```env
# OpenAI 配置
OPENAI_API_KEY=sk-proj-xxxxxx...

# 其他配置
DEBUG=True
APP_NAME=FastAPI Admin Backend
```

---

## 7️⃣ 依賴管理

### 新增依賴

```txt
opencv-python>=4.8.0      # 視頻幀提取
numpy>=1.24.0            # 數值計算
# OpenAI (已存在)
# FastAPI (已存在)
# Pydantic (已存在)
```

### 依賴用途

| 套件 | 用途 | 版本 |
|------|------|------|
| opencv-python | 視頻處理、幀提取 | >=4.8.0 |
| numpy | 陣列操作、影像処理 | >=1.24.0 |
| openai | Claude API 調用 | (現有) |
| fastapi | Web 框架 | (現有) |
| pydantic | 資料驗證 | (現有) |

---

## 8️⃣ 安全考慮

### 檔案驗證

```python
# 檔案類型白名單
allowed_types = [
    'video/mp4',
    'video/mpeg',
    'video/quicktime',
    'video/x-msvideo',
    'video/webm'
]

# 檔案大小限制
max_size = 500 * 1024 * 1024  # 500MB
```

### 臨時檔案管理

```python
# 自動清理
try:
    result = mbti_service.predict_mbti(temp_path)
finally:
    if temp_path and os.path.exists(temp_path):
        os.remove(temp_path)
```

### API 安全

```python
# 環境變數存儲敏感資訊
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# CORS 配置
app.add_middleware(CORSMiddleware, allow_origins=["*"])
```

---

## 9️⃣ 前端架構 (templates/mbti.html)

### HTML 結構

```html
<body>
  <div class="container">
    <!-- 標題區 -->
    <div class="header"></div>
    
    <!-- 主要內容 (兩列) -->
    <div class="main-content">
      <!-- 左列: 上傳區 -->
      <div class="upload-section">
        <div class="upload-area"></div>
        <input type="file" id="fileInput">
        <button class="analyze-btn">開始分析</button>
      </div>
      
      <!-- 右列: 結果區 -->
      <div class="result-section">
        <div class="loading"></div>
        <div class="mbti-result"></div>
        <div class="analysis-grid"></div>
        <div class="traits"></div>
        <div class="recommendations"></div>
      </div>
    </div>
  </div>
</body>
```

### JavaScript 流程

```javascript
1. 監聽檔案上傳
   ├─ uploadArea.addEventListener('drop', ...)
   ├─ uploadArea.addEventListener('click', ...)
   └─ fileInput.addEventListener('change', ...)

2. 驗證檔案
   └─ handleFileSelect(file)

3. 發送 API 請求
   └─ fetch('/api/mbti/analyze', {method: 'POST', body: formData})

4. 顯示加載狀態
   └─ loadingSection.style.display = 'block'

5. 接收結果
   └─ displayResults(result)

6. 更新 DOM
   ├─ document.getElementById('mbtiType').textContent = ...
   ├─ 建立分析卡片
   └─ 顯示特徵和建議

7. 錯誤處理
   └─ errorMessage.classList.add('show')
```

### CSS 設計

```css
主色: #667eea (紫藍)
副色: #764ba2 (紫)
背景: 漸變 (135deg)

響應式斷點:
  • 桌面: 兩列 (1fr 1fr)
  • 行動: 單列 (1fr)

元件:
  • .upload-area: 拖拽上傳
  • .result-section: 結果展示
  • .analysis-grid: 四維度卡片
  • .trait-badge: 特徵標籤
```

---

## 🔟 測試和驗證

### 集成測試 (test_mbti_integration.py)

```python
test_imports()              # ✓ 檢查模組導入
test_fastapi_integration()  # ✓ 檢查路由註冊
test_template_exists()      # ✓ 檢查前端檔案
test_requirements()         # ✓ 檢查依賴
```

執行測試：
```bash
python test_mbti_integration.py
```

---

## 總結表格

| 層級 | 檔案 | 功能 |
|------|------|------|
| **Route** | mbti_routes.py | 定義 API 端點 |
| **Controller** | mbti_controller.py | 請求處理和驗證 |
| **Service** | mbti_service.py | 核心業務邏輯 |
| **View** | mbti_view.py | 頁面渲染 |
| **Frontend** | mbti.html | 使用者介面 |
| **Config** | config.py | 應用設定 |

---

希望這個完整的架構文檔對您有幫助！🎉
