# MBTI 影片分析工具 - 快速設置指南

## ✅ 實現完成

已為您的 FastAPI 應用添加了一個完整的 **MBTI 影片分析功能**。

---

## 📁 新增檔案結構

```
Team_project/
├── app/
│   ├── controllers/
│   │   └── mbti_controller.py          # MBTI 控制層 (新)
│   ├── routes/
│   │   └── mbti_routes.py              # MBTI 路由層 (新)
│   ├── services/
│   │   └── mbti_service.py             # MBTI 服務層 (新)
│   ├── views/
│   │   └── mbti_view.py                # MBTI 視圖層 (新)
│   └── core/
│       └── config.py                    # ✏️ 已更新 (新增 OpenAI 配置)
├── templates/
│   └── mbti.html                        # MBTI 前端頁面 (新)
├── run.py                               # ✏️ 已更新 (整合 MBTI 路由)
├── requirements.txt                     # ✏️ 已更新 (新增依賴)
├── MBTI_ANALYSIS_GUIDE.md              # 詳細使用指南 (新)
├── MBTI_SETUP.md                       # 本檔案
└── test_mbti_integration.py            # 集成測試腳本 (新)
```

---

## 🚀 快速開始 (5 步)

### 1️⃣ 安裝新依賴
```bash
pip install opencv-python==4.8.0.76 numpy==1.24.0
```

或直接更新所有依賴：
```bash
pip install -r requirements.txt
```

### 2️⃣ 配置 OpenAI API 金鑰

**方法 A: 使用 .env 檔案 (推薦)**

在項目根目錄創建或編輯 `.env` 檔案：
```env
OPENAI_API_KEY=sk-your-api-key-here
```

**方法 B: 環境變數**

Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY='sk-your-api-key-here'
```

Windows (CMD):
```cmd
set OPENAI_API_KEY=sk-your-api-key-here
```

Linux/Mac:
```bash
export OPENAI_API_KEY='sk-your-api-key-here'
```

**獲取 API 金鑰:**
1. 訪問 https://platform.openai.com/api-keys
2. 使用 OpenAI 帳戶登錄
3. 點擊 "Create new secret key"
4. 複製金鑰

### 3️⃣ 測試集成 (可選)

```bash
python test_mbti_integration.py
```

預期輸出：
```
🎬 MBTI 影片分析功能集成測試
==================================================
✓ 導入 mbti_controller...
✓ 導入 mbti_service...
✓ 導入 mbti_routes...
✓ 導入 mbti_view...

✅ 所有模組導入成功！
```

### 4️⃣ 啟動應用

```bash
python run.py
```

您應該看到：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 5️⃣ 訪問頁面

在瀏覽器中打開：
```
http://localhost:8000/mbti
```

---

## 🎯 功能特性

### ✨ 前端功能
- ✅ 拖拽上傳影片
- ✅ 檔案驗證和進度顯示
- ✅ 實時分析狀態
- ✅ 詳細結果展示
- ✅ 響應式設計 (桌面和行動裝置)

### 🧠 MBTI 分析
系統分析四個關鍵維度：

| 維度 | 說明 |
|------|------|
| **I/E** | 內向 vs 外向 |
| **S/N** | 感知 vs 直覺 |
| **T/F** | 思維 vs 情感 |
| **J/P** | 判斷 vs 感知 |

### 📊 分析結果包含
- MBTI 類型 (如 ISFJ)
- 信心度百分比 (0-100)
- 四維度詳細分析
- 觀察到的行為特徵
- 個性發展建議

---

## 📡 API 端點

### MBTI 分析 API
```
POST /api/mbti/analyze
Content-Type: multipart/form-data

參數:
  - file: 視頻文件 (MP4, MOV, AVI, WebM)

返回:
  {
    "success": true,
    "data": {
      "mbti_type": "ISFJ",
      "confidence": 85,
      "analysis": {...},
      "behavioral_traits": [...],
      "recommendations": "..."
    }
  }
```

### 頁面路由
```
GET /mbti                    → MBTI 分析頁面
GET /api/mbti/docs          → API 文檔 (Swagger)
GET /api/mbti/redoc         → API 文檔 (ReDoc)
```

---

## 🔧 系統架構

```
使用者上傳影片
    ↓
FastAPI 路由層 (/api/mbti/analyze)
    ↓
MBTIController (檔案驗證)
    ↓
MBTIService (視頻分析 & AI 預測)
    ├─ 提取影片幀 (cv2)
    ├─ 編碼為 Base64
    └─ 呼叫 Claude API
    ↓
返回 JSON 結果
    ↓
前端 JavaScript 渲染結果
```

---

## 📋 檔案說明

### 後端檔案

#### `app/services/mbti_service.py`
- 核心 MBTI 分析邏輯
- 調用 Claude 3.5 Sonnet API
- 提取和處理視頻幀

#### `app/controllers/mbti_controller.py`
- 處理檔案上傳
- 驗證檔案類型和大小
- 管理臨時檔案

#### `app/routes/mbti_routes.py`
- 定義 `/api/mbti/analyze` 端點
- 請求/回應處理

#### `app/views/mbti_view.py`
- 渲染 HTML 頁面

### 前端檔案

#### `templates/mbti.html`
- 完整的 UI 頁面
- 拖拽上傳區域
- 進度顯示
- 結果視覺化
- JavaScript 檔案處理和 API 調用

### 配置檔案

#### `app/core/config.py`
新增配置：
```python
OPENAI_API_KEY: Optional[str] = None
OPENAI_MODEL: str = "gpt-4-vision-preview"
```

#### `requirements.txt`
新增依賴：
```
opencv-python>=4.8.0
numpy>=1.24.0
```

---

## ⚙️ 配置選項

在 `.env` 或 `app/core/config.py` 中自訂：

```env
# OpenAI 配置
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-4-vision-preview

# 應用配置
DEBUG=True
APP_NAME=FastAPI Admin Backend
```

---

## 🔒 安全考慮

✅ **實現的安全措施：**
- 檔案類型白名單驗證
- 檔案大小限制 (500MB)
- 臨時檔案自動清理
- API 金鑰環境變數存儲
- CORS 配置

---

## 📊 支援的檔案格式

| 格式 | 副檔名 | MIME 類型 |
|------|---------|----------|
| MP4 | .mp4 | video/mp4 |
| MPEG | .mpeg | video/mpeg |
| QuickTime | .mov | video/quicktime |
| AVI | .avi | video/x-msvideo |
| WebM | .webm | video/webm |

**最大檔案大小**: 500MB

---

## 🐛 常見問題

### Q: 分析需要多長時間？
**A:** 通常 1-2 分鐘

### Q: 需要 GPU 嗎？
**A:** 不需要，使用 CPU 即可

### Q: 成本多少？
**A:** 取決於 OpenAI API 使用量 (按 token 計費)

### Q: 可以修改分析維度嗎？
**A:** 可以，編輯 `mbti_service.py` 中的提示詞

### Q: 可以保存分析結果嗎？
**A:** 目前不保存，可以自行擴展資料庫模型

---

## 🔄 下一步

### 可選擴展功能：
1. ✨ 新增資料庫模型存儲分析歷史
2. ✨ 建立結果對比功能
3. ✨ 新增即時攝像頭分析
4. ✨ 批量檔案處理
5. ✨ 生成詳細的 PDF 報告

### 修改分析邏輯：
編輯 `mbti_service.py` 中的 `predict_mbti()` 方法內的提示詞 (Prompt)

---

## 📞 遇到問題？

### 檢查清單：
- [ ] OpenAI API 金鑰已正確設置
- [ ] 已安裝 opencv-python 和 numpy
- [ ] 影片檔案格式正確
- [ ] 網路連線正常
- [ ] 應用成功啟動 (無錯誤)

### 偵錯步驟：
1. 查看應用日誌
2. 執行 `test_mbti_integration.py` 測試
3. 在瀏覽器開發工具中檢查網路請求
4. 檢查 API 配額是否充足

---

## 📖 詳細文檔

查看 [MBTI_ANALYSIS_GUIDE.md](MBTI_ANALYSIS_GUIDE.md) 了解：
- 完整的 API 文檔
- 進階配置
- 故障排除指南
- 擴展建議

---

## 🎉 完成！

您現在已經擁有一個完整的 MBTI 影片分析系統！

**開始使用：**
```bash
python run.py
# 訪問 http://localhost:8000/mbti
```

祝您使用愉快！ 🚀
