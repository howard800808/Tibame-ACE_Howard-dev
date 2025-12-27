# AWS Rekognition 情緒分析功能說明

本文件說明如何設定、使用與測試 AWS Rekognition 情緒分析功能。

## 1. 環境設定

### 1.1 AWS 憑證設定
請確保 .env 檔案中包含正確的 AWS 憑證：

`ini
AWS_ACCESS_KEY_ID=你的AccessKey
AWS_SECRET_ACCESS_KEY=你的SecretKey
AWS_REGION=ap-northeast-1  # 或其他區域
`

### 1.2 資料庫 Schema 更新
由於 AWS Rekognition 回傳的分析結果 (JSON) 可能非常大，預設的資料庫欄位 (VARCHAR) 可能不足以儲存。
我們已將 emotion_analysis 資料表的相關欄位更新為 TEXT 和 LONGTEXT。

若您在部署新環境或遇到 Data too long 錯誤，請執行以下修復腳本：

`ash
python scripts/aws_emotion/fix_db_schema.py
`

## 2. 功能測試

我們提供了一個自動化測試腳本，用於驗證：
1. 系統登入 (取得 JWT Token)
2. 上傳圖片並呼叫情緒分析 API
3. 驗證資料庫儲存結果

### 2.1 執行測試

請確保虛擬環境已啟動，然後執行：

`ash
python scripts/aws_emotion/test_emotion_api.py
`

### 2.2 測試結果範例

成功執行後，您將看到類似以下的輸出：

`	ext
=== AWS Rekognition 情緒分析測試 ===
正在登入... (admin)
登入成功!

正在分析圖片: .../test_face.jpg
=== 分析成功 ===
主要情緒: CALM (信心度: 99.86%)
偵測到人臉數: 1
...
完整回應已儲存至 'analysis_result.json'
`

## 3. API 路由說明

情緒分析相關的 API 路由已重新整理至 MVC 架構中：

- **圖片分析**: POST /api/emotions/analyze-image-emotion
- **影片分析**: POST /api/emotions/analyze-video-emotion
- **取得圖片結果**: GET /api/emotions/image-results/{analysis_id}
- **取得影片結果**: GET /api/emotions/video-results/{analysis_id}

## 4. 檔案結構

- pp/controllers/emotion_controller.py: 控制層邏輯
- pp/services/emotion_service.py: 業務邏輯與 AWS 整合
- pp/routes/emotion_routes.py: API 路由定義
- pp/models/emotion.py: 資料庫模型
