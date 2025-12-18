# 本地測試指南（無需 ngrok）

## ✅ 當前狀態
- 伺服器正在運行（PID: 14992）
- 12 個部門已初始化
- Webhook 端點工作正常

---

## 🚀 立即測試步驟

### 步驟 1：廣播任務卡片到 LINE

在 PowerShell 執行：

```powershell
# 廣播任務卡片到所有 12 個部門
Invoke-WebRequest -Method POST "http://localhost:8000/api/linebot/demo/all/tasks" -UseBasicParsing
```

這會將任務卡片發送到所有已加入 Bot 的 LINE 群組。

---

### 步驟 2：在 LINE 上查看並測試

1. **打開 LINE 應用**
2. **找到您的 Bot 群組**
3. **查看任務卡片**（Flex Message）
   - 標題：客房 1205 清潔派工
   - 兩個按鈕：「接受任務」、「已完成任務」

---

### 步驟 3：測試按鈕互動

#### 測試 A：接受任務
1. 點擊「接受任務」
2. **預期效果：**
   - LINE 回覆：「✅ 您已接受此派工任務！」
3. **伺服器日誌（run.py 終端）：**
   ```
   [Webhook] 收到統一端點請求
   [Webhook] [OK] 簽名匹配部門: HK
   [Postback] 收到事件，部門: HK
   [LINEBot 任務] {'op': 'accept', ...}
   ```

#### 測試 B：完成任務（自動啟動回報流程）
1. 點擊「已完成任務」
2. **預期效果：**
   - LINE 回覆：「✅ 任務已標記為完成！現在進入 5 步驟回報流程...」
   - **自動顯示第 1 步回報卡片**
     - 標題：「任務回報 (1/5)」
     - 問題：「是否順利完成？」
     - 按鈕：「是 (Yes)」、「否 (No)」

3. **伺服器日誌：**
   ```
   [Postback] 自動啟動回報流程
   [Postback] [OK] 已送出回報流程第 1 步
   ```

---

### 步驟 4：逐步完成回報流程

點擊回報卡片的按鈕，觀察自動進展：

| 步驟 | 問題 | 選項 | 下一步 |
|------|-----|------|--------|
| 1/5 | 是否順利完成？ | 是/否 | 第 2 步：補充說明 |
| 2/5 | 補充說明 | URI 輸入 | 繼續 |
| 3/5 | 是否有特殊情況？ | 有/無 | 第 4 步 |
| 4/5 | 顧客情緒判斷 | 正向/中立/負向 | 第 5 步 |
| 5/5 | 備註事項 | URI 輸入 | 完成 |

**完成後顯示：**
「✅ 回報流程已完成！感謝您的詳細說明。」

---

## 📊 驗證清單

### ✅ LINE 客戶端
- [ ] 收到任務卡片
- [ ] 點擊「接受任務」有回應
- [ ] 點擊「已完成任務」自動顯示第 1 步回報卡片
- [ ] 回報流程逐步進行（不是一次性顯示 5 張）
- [ ] 最後收到完成訊息

### ✅ 伺服器日誌
- [ ] 看到 `[Webhook] 收到統一端點請求`
- [ ] 看到 `[Webhook] [OK] 簽名匹配部門`
- [ ] 看到 `[Postback] 收到事件`
- [ ] 看到 `[LINEBot 任務]` 或 `[LINEBot 回報]`
- [ ] 沒有 `[ERROR]` 訊息

---

## 🔧 快速命令

```powershell
# 檢查伺服器狀態
Get-Process python* | Select Id, ProcessName, StartTime

# 檢查部門初始化
$diag = Invoke-WebRequest "http://localhost:8000/api/linebot/diagnostics" -UseBasicParsing
($diag.Content | ConvertFrom-Json).departments | ft code, name, initialized

# 廣播任務卡片
Invoke-WebRequest -Method POST "http://localhost:8000/api/linebot/demo/all/tasks" -UseBasicParsing

# 本地 Postback 測試（驗證邏輯）
.\test_webhook_simple.ps1
```

---

## ❓ 疑難排解

### 問題：點擊按鈕沒反應

**檢查：**
1. 伺服器日誌是否有 `[Webhook]` 訊息？
   - 沒有 → Webhook URL 未設置或錯誤
   - 有 → 檢查是否有 `[Postback]` 訊息

2. 是否看到 `[WARN] 找不到匹配的部門`？
   - 是 → Channel Secret 錯誤

### 問題：回報卡片一次性顯示 5 張

**解決：**
- 重啟伺服器（已修復，使用逐步回覆）

---

## 🎉 成功指標

完整測試成功後：
- ✅ LINE 收到任務卡片
- ✅ 按鈕點擊有即時回應
- ✅ 回報流程逐步進行
- ✅ 伺服器日誌完整記錄
- ✅ 無錯誤訊息

**您的 LINE Bot 任務系統已就緒！**
