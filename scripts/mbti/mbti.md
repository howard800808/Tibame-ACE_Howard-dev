# MBTI 模組測試腳本說明

本目錄包含用於測試與驗證 MBTI 影片分析模組的工具腳本。這些腳本不參與應用程式的主要運行邏輯，但在開發、部署與除錯階段非常有用。

## 檔案列表

### 1. `test_mbti_integration.py`
**用途**: 整合測試腳本。
**功能**:
- 驗證所有 MBTI 相關模組 (`Controller`, `Service`, `Routes`, `Views`) 是否能正確導入。
- 檢查 FastAPI 應用是否正確註冊了 MBTI 相關的 API 與頁面路由。
- 檢查前端模板檔案 (`templates/mbti.html`) 是否存在且包含關鍵元素。
- 檢查 `requirements.txt` 中是否包含必要的依賴套件。

**使用時機**:
- 在部署新環境後，確認 MBTI 模組是否安裝完整。
- 修改了專案結構後，確保沒有破壞 MBTI 模組的整合。

**執行方式**:
```bash
python scripts/mbti/test_mbti_integration.py
```

### 2. `verify_gemini.py`
**用途**: Google Gemini 配置驗證腳本。
**功能**:
- 檢查環境變數或設定檔中是否已讀取到 `GEMINI_API_KEY`。
- 嘗試初始化 `MBTIService` 並建立 Gemini 模型實例。
- 確認 API Key 是否有效且模型名稱設定正確。

**使用時機**:
- 當 MBTI 分析功能無法運作時，首先執行此腳本排除配置問題。
- 更新了 API Key 或更換模型版本後進行驗證。

**執行方式**:
```bash
python scripts/mbti/verify_gemini.py
```

### 3. `test_gemini_fix.py` (如果存在)
**用途**: 針對特定 Gemini API 問題的修復測試。
**功能**: 測試特定的 API 呼叫或參數調整是否解決了已知問題。

---

## 維護建議

建議保留這些腳本，它們對於 CI/CD 流程或快速診斷生產環境問題非常有幫助。
