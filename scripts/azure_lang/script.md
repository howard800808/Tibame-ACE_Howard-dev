# Azure Language & Video Analysis Scripts

本目錄包含用於測試、驗證與維護 Azure 語音轉文字 (Speech-to-Text) 與影片分析功能的腳本集合。

## 📂 檔案列表與功能說明

### 🛠️ 資料庫與維護工具 (Database & Maintenance)

| 檔案名稱 | 功能說明 |
|----------|----------|
| `migrate_db.py` | **資料庫遷移腳本**。用於檢查並更新 SQLite 資料庫結構，新增 `speaker_segments` 與 `speaker_count` 欄位，確保資料庫支援新的分析功能。 |
| `install_ffmpeg.ps1` | **FFmpeg 安裝腳本**。PowerShell 腳本，用於在 Windows 環境下自動下載並設定 FFmpeg，這是音訊提取功能的必要依賴。 |

### 🔍 診斷與除錯 (Diagnostics)

| 檔案名稱 | 功能說明 |
|----------|----------|
| `diagnose_video_error.py` | **API 錯誤診斷工具**。模擬影片上傳流程，用於捕捉並分析 HTTP 500 錯誤，特別針對 JSON 序列化或資料庫寫入問題。 |
| `verify_transcription.py` | **轉錄功能驗證**。直接測試 Azure Speech SDK 的轉錄功能，不經過 Web API，用於確認 Azure 服務連線與金鑰設定是否正確。 |

### 🧪 整合測試 (Integration Tests)

| 檔案名稱 | 功能說明 |
|----------|----------|
| `test_end_to_end.py` | **端到端測試**。模擬完整使用者流程：登入 -> 上傳影片 -> 輪詢狀態 -> 取得結果。用於驗證系統整體運作。 |
| `test_system.py` | **系統級測試**。類似端到端測試，但可能包含更多系統狀態的檢查。 |

### 🧩 單元與組件測試 (Unit & Component Tests)

| 檔案名稱 | 功能說明 |
|----------|----------|
| `test_audio_extraction.py` | **音訊提取測試**。測試 FFmpeg 是否能正確從影片中分離出音軌檔案。 |
| `test_azure_setup.py` | **Azure 環境測試**。檢查環境變數 (`.env`) 中的 Azure API Key 與 Endpoint 是否已正確設定。 |
| `test_language_codes.py` | **語言代碼測試**。驗證 Azure Speech SDK 支援的語言代碼設定 (如 `zh-TW`)。 |
| `test_detail_function.py` | **函數級測試**。針對特定內部函數進行測試。 |

### 📡 API 接口測試 (API Tests)

| 檔案名稱 | 功能說明 |
|----------|----------|
| `test_api.py` | **基礎 API 測試**。測試基本的 API 連線與回應。 |
| `test_api_detailed.py` | **詳細 API 測試**。包含更多邊界條件與參數的 API 測試。 |
| `test_api_endpoints.py` | **路由端點測試**。驗證各個 API 路由 (Routes) 是否可存取。 |
| `test_get_results.py` | **結果獲取測試**。專門測試「獲取分析結果」的 API，驗證回傳的 JSON 格式是否符合預期。 |

### 📦 測試資源 (Test Assets)

| 檔案名稱 | 功能說明 |
|----------|----------|
| `check-in-test.mp4` | **真實測試影片**。用於端到端測試的範例影片檔案。 |
| `test_video.mp4` | **生成測試影片**。由腳本生成的最小化 MP4 檔案，用於快速測試上傳功能。 |
| `TEST_REPORT.txt` | **測試報告**。記錄測試執行結果的文字檔。 |

## 🚀 使用建議

1. **環境設定檢查**：在部署或開發前，先執行 `test_azure_setup.py` 確認 `.env` 設定正確。
2. **功能驗證**：若遇到轉錄問題，使用 `verify_transcription.py` 隔離測試 Azure 服務。
3. **資料庫更新**：若更新了程式碼但資料庫報錯，嘗試執行 `migrate_db.py`。
4. **完整測試**：在提交程式碼前，執行 `test_end_to_end.py` 確保核心流程正常。
