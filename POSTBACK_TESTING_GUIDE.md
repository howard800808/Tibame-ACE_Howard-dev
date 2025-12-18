# LINE Bot Postback 互動完整測試指南

## 📋 修復內容

### 1. Webhook 統一端點改進 ✅
- **改善簽名驗證邏輯**：更精確的 `InvalidSignatureError` 檢查
- **增加日誌輸出**：追蹤 Webhook 接收、簽名匹配、事件處理的完整流程
- **錯誤診斷**：當簽名不匹配時，顯示詳細的除錯資訊

### 2. Postback 事件處理改進 ✅
- **逐步回報流程**：不再一次性廣播所有 5 張卡片，改為根據用戶回答逐步回覆下一步
- **自動啟動回報**：當用戶點擊「已完成任務」時，自動開啟 5 步驟回報流程
- **房號保留**：回報卡片的 Postback 資料中包含 `room` 參數，確保房號在整個流程中一致

### 3. 回報卡片改進 ✅
- **Postback 資料完整性**：每個按鈕的 Postback 資料都包含 `room` 參數，供後續步驟使用

---

## 🚀 測試步驟

### 步驟 1️⃣：驗證服務器啟動 ✅

確認所有 12 個部門已初始化且無錯誤：

```powershell
$response = Invoke-WebRequest -Method GET "http://localhost:8000/api/linebot/diagnostics" -UseBasicParsing
$json = $response.Content | ConvertFrom-Json
Write-Host "總共初始化部門數: $($json.departments.Count)"
$json.departments | Select-Object code, name, initialized | Format-Table
```

**預期結果**：顯示 12 個部門，全部 `initialized: true`

---

### 步驟 2️⃣：廣播任務卡片到 LINE ✅

一次性廣播 12 個部門的任務卡片：

```powershell
Write-Host "`n[廣播] 發送 12 部門任務卡片..." -ForegroundColor Cyan
$response = Invoke-WebRequest -Method POST "http://localhost:8000/api/linebot/demo/all/tasks" -UseBasicParsing
$json = $response.Content | ConvertFrom-Json
Write-Host "廣播結果:" -ForegroundColor Green
$json.broadcasted | Format-Table -AutoSize
```

**預期結果**：
- 12 個部門全部 `sent: true`
- 服務器日誌顯示 `[OK] 部門 XX 事件處理完成` (針對邊界情況)

---

### 步驟 3️⃣：在 LINE 上進行互動 📱

1. 開啟 LINE，找到剛才廣播的任務卡片
2. **點擊按鈕**「接受任務 (Accept)」
   - 預期：LINE 立即顯示回覆訊息「✅ 您已接受此派工任務！」
   - **伺服器日誌**應顯示：
     ```
     [Postback] 收到事件，部門: HK
     [Postback] 動作: task，詳細資料: {...}
     [LINEBot 任務] {'department': 'HK', 'op': 'accept', ...}
     ```

---

### 步驟 4️⃣：測試已完成任務 → 自動啟動回報流程 🔄

1. 再次點擊 LINE 上的任務卡片
2. **點擊按鈕**「已完成任務 (Complete)」
   - 預期：LINE 顯示回覆訊息「✅ 任務已標記為完成！現在進入 5 步驟回報流程...」
   - 然後 LINE **自動顯示第 1 步回報卡片**：
     - 標題：「任務回報 (1/5)」
     - 問題：「是否順利完成？」
     - 按鈕：「是 (Yes)」、「否 (No)」

   - **伺服器日誌**應顯示：
     ```
     [Postback] 收到事件，部門: HK
     [Postback] 動作: task，詳細資料: {...}
     [LINEBot 任務] {'department': 'HK', 'op': 'complete', ...}
     [Postback] 自動啟動回報流程，任務ID: ...
     [Postback] [OK] 已送出回報流程第 1 步
     ```

---

### 步驟 5️⃣：逐步完成回報流程 ⬇️

現在在 LINE 上逐步點擊按鈕，觀察自動進展：

| 步驟 | 按鈕選擇 | 期望效果 |
|------|---------|--------|
| 1/5 | 點擊「是 (Yes)」 | LINE 顯示第 2 步卡片「補充說明 / 微調查」|
| 2/5 | 不用點擊（URI 按鈕）| 用戶可輸入文字或語音 |
| 3/5 | 點擊「有 (Yes)」 | LINE 顯示第 4 步卡片「顧客情緒判斷」|
| 4/5 | 點擊「正向」 | LINE 顯示第 5 步卡片「備註事項」|
| 5/5 | 不用點擊（URI 按鈕）| 用戶可輸入補充備註 |

**每步完成後，伺服器日誌應顯示**：
```
[Postback] 收到事件，部門: HK
[Postback] 動作: report，詳細資料: {...}
[LINEBot 回報] {'department': 'HK', 'task_id': '...', 'step': 1, 'answer': 'yes', ...}
[Postback] [OK] 已送出回報流程第 2 步
```

---

### 步驟 6️⃣：完成最後一步 ✅

1. 第 5 步完成後，點擊任何 URI 按鈕（語音/文字輸入）或等待
2. 期望：LINE 顯示訊息「✅ 回報流程已完成！感謝您的詳細說明。」
3. **伺服器日誌**應顯示：
   ```
   [Postback] [OK] 回報流程完成
   ```

---

## 🔍 疑難排解

### ❌ 問題 1：點擊按鈕但沒有反應

**原因可能**：
- Webhook URL 未正確設定在 LINE Developers
- Webhook 簽名驗證失敗

**檢查步驟**：
1. 確認 LINE Developers 中的 Webhook URL 為：`https://ace.89.com.tw/api/linebot/webhook`
2. 檢查伺服器日誌中是否有：
   ```
   [Webhook] [ERROR] 找不到匹配的部門，簽名: ...
   ```
3. 如果看到上述訊息，表示簽名驗證失敗，檢查 Channel Secret 是否正確

---

### ❌ 問題 2：Postback 事件沒有日誌輸出

**原因可能**：
- Webhook 端點未被正確調用
- Postback 資料解析失敗

**檢查步驟**：
1. 檢查伺服器日誌中是否有：
   ```
   [Webhook] 收到統一端點請求
   ```
2. 如果沒有，表示 Webhook 未被調用（檢查 LINE Developers 設定）
3. 如果有但沒有 `[Postback]` 日誌，檢查是否為其他事件類型

---

### ❌ 問題 3：回報卡片一次性顯示所有 5 步

**原因**：代碼未更新，仍使用舊的廣播邏輯

**解決方案**：
1. 確認伺服器已重新啟動（使用最新代碼）
2. 檢查 `app/controllers/linebot_controller.py` 的 `_handle_postback_event` 方法
3. 確認回報邏輯使用 `reply_flex`（逐步回覆）而非 `broadcast_flex`（一次性廣播）

---

## 📊 成功指標

✅ **完整成功的流程**應該包括：

1. ✅ 服務器成功啟動，12 部門全部初始化
2. ✅ 任務卡片廣播到 LINE 成功（12/12 sent=true）
3. ✅ 點擊「接受任務」按鈕 → 伺服器日誌顯示 `[LINEBot 任務]` + `[任務狀態更新]`
4. ✅ 點擊「已完成任務」按鈕 → 自動顯示第 1 步回報卡片
5. ✅ 逐步點擊回報卡片按鈕 → 每步都自動顯示下一步卡片（非一次性）
6. ✅ 最後一步完成 → 收到「✅ 回報流程已完成！」訊息
7. ✅ 伺服器日誌完整記錄了所有 Postback 事件和回報流程進度

---

## 🎯 快速檢查清單

- [ ] 服務器已啟動，無 `[ERROR]` 日誌
- [ ] 12 部門已初始化 (`initialized: true`)
- [ ] 任務卡片已廣播到 LINE（檢查 LINE 應用）
- [ ] 可以點擊任務卡片上的按鈕
- [ ] 點擊按鈕後收到伺服器回覆訊息
- [ ] 伺服器日誌顯示 `[Postback]`、`[LINEBot 任務]` 或 `[LINEBot 回報]`
- [ ] 回報流程逐步進行（不是一次性）
- [ ] 最後一步顯示完成訊息

---

## 🔧 進階診斷

如需查看完整的 Webhook 請求和回應，可執行：

```powershell
# 模擬 Postback 事件 (需要已知的 task_id)
$body = @{
    "events" = @(
        @{
            "type" = "postback"
            "postback" = @{
                "data" = "action=report&step=1&id=demo-task-123&ans=yes&room=Room%201205"
            }
            "replyToken" = "test_reply_token"
        }
    )
} | ConvertTo-Json

Invoke-WebRequest -Method POST "http://localhost:8000/api/linebot/webhook" `
    -ContentType "application/json" `
    -Body $body `
    -Headers @{"X-Line-Signature" = "test_signature"}
```

此測試可用於在無實際 LINE 應用的環境中驗證 Postback 邏輯。

