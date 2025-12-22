# Scripts 目錄說明

本目錄包含用於資料庫維護、資料匯入及系統初始化的 Python 腳本。

## 腳本列表

| 檔案名稱 | 用途 |
|:--- |:--- |
| [check_db_tasks.py](#check_db_taskspy) | 檢查資料庫中的任務資料 |
| [clean_old_tasks.py](#clean_old_taskspy) | 清除舊的測試任務資料 |
| [clean_task_notes.py](#clean_task_notespy) | 清理任務備註中的系統日誌 |
| [fix_fb_data.py](#fix_fb_datapy) | 修正餐飲部 (F&B) 的資料格式 |
| [import_hotel_tasks.py](#import_hotel_taskspy) | 從 JSON 匯入飯店任務資料 |
| [init_mysql_db.py](#init_mysql_dbpy) | 初始化 MySQL 資料庫 (Create Database) |
| [init_report_table.py](#init_report_tablepy) | 初始化資料表 (Create Tables) |

---

## 詳細說明

### check_db_tasks.py
*   **用途**: 快速檢查資料庫 hotel_tasks 表中的最新任務。
*   **用法**: python scripts/linebot/check_db_tasks.py
*   **參數**: 無
*   **功能**: 
    *   連接資料庫。
    *   查詢並列出 ID 最大的前 20 筆任務。
    *   顯示欄位：ID, Task ID, Dept Code, Title。

### clean_old_tasks.py
*   **用途**: 清除資料庫中舊的測試任務（Task ID 以 'T' 開頭的資料）。
*   **用法**: python scripts/linebot/clean_old_tasks.py
*   **參數**: 無
*   **功能**: 
    *   統計 	ask_id 以 'T' 開頭的任務數量。
    *   執行刪除操作。
    *   列出剩餘任務的範例。

### clean_task_notes.py
*   **用途**: 清理 hotel_tasks 表中 
ote 欄位，移除系統自動產生的回報日誌。
*   **用法**: python scripts/linebot/clean_task_notes.py
*   **參數**: 無
*   **功能**: 
    *   搜尋所有有備註的任務。
    *   移除備註中以 [Report Step 開頭或等於 [System] 回報流程完成 的行。
    *   保留使用者輸入的備註內容。

### fix_fb_data.py
*   **用途**: 修正資料庫中餐飲部門代碼不一致的問題（將 'F&B' 統一為 'FB'）。
*   **用法**: python scripts/linebot/fix_fb_data.py
*   **參數**: 無
*   **功能**: 
    *   檢查 dept_code 為 'F&B' 或 	ask_id 包含 'F&B' 的資料。
    *   執行 SQL Update 將其修正為 'FB'。
    *   這是因為 URL 或某些系統不支援 '&' 符號。

### import_hotel_tasks.py
*   **用途**: 將 JSON 格式的任務資料匯入資料庫。
*   **用法**: python scripts/linebot/import_hotel_tasks.py [json_file_path]
*   **參數**: 
    *   json_file_path (選填): JSON 檔案的路徑。若未提供，預設會嘗試讀取 c:\Users\HOWARD\Downloads\hotel_task_scenarios_for_DB.json。
*   **功能**: 
    *   讀取 JSON 檔案。
    *   自動建立資料表（如果不存在）。
    *   將任務資料寫入 hotel_tasks 表。
    *   若任務已存在（根據 	ask_id 和 project_name），則更新該任務資料。
    *   匯入時會自動將 'F&B' 轉換為 'FB'。

### init_mysql_db.py
*   **用途**: 建立 MySQL 資料庫（Database 層級）。
*   **用法**: python scripts/linebot/init_mysql_db.py
*   **參數**: 無
*   **功能**: 
    *   解析 .env 中的 DATABASE_URL。
    *   連接 MySQL Server。
    *   執行 CREATE DATABASE IF NOT EXISTS 指令。

### init_report_table.py
*   **用途**: 建立資料庫中的資料表（Table 層級）。
*   **用法**: python scripts/linebot/init_report_table.py
*   **參數**: 無
*   **功能**: 
    *   使用 SQLAlchemy 的 Base.metadata.create_all。
    *   根據 pp/models 中的定義建立所有尚未存在的資料表（如 	ask_reports, hotel_tasks 等）。
