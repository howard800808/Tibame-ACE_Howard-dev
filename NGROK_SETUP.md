# 使用 ngrok 進行本地 LINE Bot 測試指南

## 📋 步驟

### 1. 下載並安裝 ngrok
訪問：https://ngrok.com/download
或使用 Chocolatey：
```powershell
choco install ngrok
```

### 2. 啟動 ngrok 隧道
在新的 PowerShell 終端執行：
```powershell
ngrok http 8000
```

您會看到類似這樣的輸出：
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

### 3. 複製 ngrok URL
記下 `https://abc123.ngrok.io` 這個 URL（每次重啟 ngrok 都會變化）

### 4. 在 LINE Developers 中設置 Webhook
1. 登入 https://developers.line.biz/console/
2. 選擇您的 Messaging API Channel
3. 在 Webhook settings 中，將 Webhook URL 設為：
   ```
   https://abc123.ngrok.io/api/linebot/webhook
   ```
4. 點擊 "Verify" - 應該顯示 Success ✅
5. 開啟 "Use webhook" 開關

### 5. 測試實際 LINE 互動
1. 使用 LINE 應用掃描您的 Bot QR Code
2. 在本地執行廣播命令：
   ```powershell
   Invoke-WebRequest -Method POST "http://localhost:8000/api/linebot/demo/all/tasks" -UseBasicParsing
   ```
3. 您應該會在 LINE 上收到任務卡片
4. 點擊卡片上的按鈕測試互動功能

### 6. 觀察伺服器日誌
當您點擊 LINE 上的按鈕時，應該會看到：
```
[Webhook] 收到統一端點請求，簽名: ...
[Webhook] [OK] 簽名匹配部門: HK (房務部)
[Webhook] 將處理 1 個事件，部門: HK
[Postback] 收到事件，部門: HK
[Postback] 動作: task，詳細資料: {...}
[LINEBot 任務] {'department': 'HK', 'op': 'accept', ...}
```

## ⚠️ 注意事項
- ngrok 免費版會話限制為 8 小時
- 每次重啟 ngrok，URL 都會變化，需要重新設置 Webhook
- ngrok 付費版可以使用固定域名

## 🔄 方案 B：直接部署到生產環境
如果不想使用 ngrok，可以直接部署到 ace.89.com.tw 伺服器
