# MBTI 影片分析工具使用指南

## 功能概述

這是一個獨立的影片分析頁面，可以：
- 🎥 上傳影片檔案（MP4、MOV、AVI、WebM）
- 🔍 分析影片中的人物行為特徵
- 🧠 使用 AI 預測人物的 MBTI 類型
- 📊 展示詳細的分析結果和建議

## 技術架構

### 後端架構 (FastAPI MVC)
```
Routes (路由層)
    ↓
Controllers (控制層)
    ↓
Services (服務層) - 核心 AI 分析
    ↓
Models (資料層)
```

### 主要檔案

#### 1. 服務層 (`app/services/mbti_service.py`)
- **MBTIService 類別**
  - `analyze_video_frames()`: 從影片中提取關鍵幀
  - `predict_mbti()`: 使用 Claude 3.5 Sonnet 分析並預測 MBTI
  - `_parse_response_to_json()`: 解析 AI 回應

#### 2. 控制層 (`app/controllers/mbti_controller.py`)
- **MBTIController 類別**
  - `analyze_video()`: 處理檔案上傳和驗證
  - 檔案類型和大小驗證
  - 臨時檔案管理

#### 3. 路由層 (`app/routes/mbti_routes.py`)
- **API 端點**: `POST /api/mbti/analyze`
  - 接收上傳的影片檔案
  - 返回 MBTI 分析結果

#### 4. 視圖層 (`app/views/mbti_view.py`)
- **MBTIView 類別**
  - `mbti_page()`: 渲染前端頁面

#### 5. 前端頁面 (`templates/mbti.html`)
- 拖拽上傳區域
- 實時進度顯示
- 結果視覺化展示
- 響應式設計

## 使用方法

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

新增的依賴包：
- `opencv-python>=4.8.0` - 視頻幀提取
- `numpy>=1.24.0` - 數值計算

### 2. 配置 API 金鑰

在 `.env` 檔案中添加：
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 啟動應用
```bash
python run.py
```

### 4. 訪問頁面
在瀏覽器中打開：
```
http://localhost:8000/mbti
```

## API 文檔

### 分析影片 API

**端點**: `POST /api/mbti/analyze`

**請求**:
- 多部分表單資料 (multipart/form-data)
- 欄位: `file` (必填) - 影片檔案

**支援的格式**:
- video/mp4
- video/mpeg
- video/quicktime
- video/x-msvideo
- video/webm

**最大檔案大小**: 500MB

**範例請求** (JavaScript):
```javascript
const formData = new FormData();
formData.append('file', videoFile);

const response = await fetch('/api/mbti/analyze', {
    method: 'POST',
    body: formData
});
const result = await response.json();
```

**成功回應** (200 OK):
```json
{
  "success": true,
  "data": {
    "mbti_type": "ISFJ",
    "confidence": 85,
    "analysis": {
      "introversion_extroversion": {
        "type": "I",
        "description": "表現出內向傾向...",
        "score": 80
      },
      "sensing_intuition": {
        "type": "S",
        "description": "注重現實和細節...",
        "score": 75
      },
      "thinking_feeling": {
        "type": "F",
        "description": "情感導向的決策...",
        "score": 85
      },
      "judging_perceiving": {
        "type": "J",
        "description": "有組織和計劃性...",
        "score": 80
      }
    },
    "behavioral_traits": [
      "細心",
      "負責任",
      "善於傾聽",
      "實際",
      "可靠"
    ],
    "recommendations": "此人格類型適合需要細心和組織能力的工作..."
  }
}
```

**錯誤回應** (400/500):
```json
{
  "success": false,
  "error": "錯誤訊息"
}
```

## MBTI 分析維度

系統分析四個核心維度：

### 1. 內向 (I) vs 外向 (E)
- **內向 (I)**: 從內部世界獲取能量，傾向反思
- **外向 (E)**: 從外部世界獲取能量，傾向行動

### 2. 感知 (S) vs 直覺 (N)
- **感知 (S)**: 注重現在和實際細節
- **直覺 (N)**: 注重未來可能性和模式

### 3. 思維 (T) vs 情感 (F)
- **思維 (T)**: 邏輯性和客觀分析
- **情感 (F)**: 價值觀和人際考量

### 4. 判斷 (J) vs 感知 (P)
- **判斷 (J)**: 喜歡組織和計劃
- **感知 (P)**: 喜歡靈活和隨機應變

## 前端功能特性

### 文件上傳
- 支援拖拽上傳
- 點擊選擇檔案
- 實時檔案訊息顯示

### 進度顯示
- 分析中加載動畫
- 進度提示訊息
- 預計耗時提示

### 結果展示
- 大型 MBTI 類型顯示
- 信心度百分比和進度條
- 四維度詳細分析卡片
- 觀察到的行為特徵標籤
- 個性發展建議

### 錯誤處理
- 清晰的錯誤訊息
- 檔案驗證反饋
- 網路錯誤提示

## 工作流程

1. **使用者上傳影片**
   - 檔案驗證 (類型、大小)
   - 保存到臨時目錄

2. **影片處理**
   - 提取 5 個關鍵幀 (均勻分佈)
   - 調整影像大小優化
   - 編碼為 Base64

3. **AI 分析**
   - 調用 Claude 3.5 Sonnet API
   - 分析人物行為特徵
   - 預測 MBTI 類型和各維度

4. **結果返回**
   - 結構化 JSON 回應
   - 前端渲染結果
   - 清理臨時檔案

## 系統要求

### 最低配置
- Python 3.8+
- 4GB RAM
- 2GB 磁碟空間 (用於依賴和臨時檔案)

### 推薦配置
- Python 3.10+
- 8GB RAM
- 5GB 磁碟空間

## 常見問題

### Q: 分析需要多長時間？
**A**: 通常 1-2 分鐘，取決於：
- 影片長度和分辨率
- API 響應時間
- 網路連線速度

### Q: 最大可以上傳多大的影片？
**A**: 目前限制為 500MB

### Q: 支援哪些影片格式？
**A**: MP4、MOV、AVI、WebM

### Q: 可以上傳多個影片同時分析嗎？
**A**: 目前不支援，需要逐個上傳分析

### Q: 分析結果的準確度如何？
**A**: 準確度取決於影片清晰度和人物表情、肢體語言的清晰度，信心度百分比可作為參考

### Q: API 金鑰如何獲取？
**A**: 需要 OpenAI 帳戶，訪問 https://platform.openai.com/api-keys

## 故障排除

### 錯誤: "請安裝 opencv-python"
```bash
pip install opencv-python==4.8.0.76
```

### 錯誤: "無法連接到 API"
- 檢查 OPENAI_API_KEY 是否正確設置
- 確認網路連線
- 檢查 API 配額

### 錯誤: "影片處理失敗"
- 確認影片檔案未損壞
- 嘗試使用其他格式轉換
- 檢查磁碟空間是否充足

## 安全考慮

1. **檔案上傳**
   - 嚴格的檔案類型驗證
   - 檔案大小限制 (500MB)
   - 臨時檔案自動清理

2. **API 安全**
   - 環境變數存儲 API 金鑰
   - 不在日誌中記錄敏感資訊

3. **資料隱私**
   - 上傳的檔案不永久存儲
   - 臨時檔案在分析完成後刪除

## 擴展功能建議

1. 支援實時攝像頭分析
2. 批量影片分析
3. 分析歷史記錄保存
4. 性格比較功能
5. 團隊成員分析報告
6. 多語言支援

## 技術支援

有任何問題或建議，請聯絡開發團隊。
