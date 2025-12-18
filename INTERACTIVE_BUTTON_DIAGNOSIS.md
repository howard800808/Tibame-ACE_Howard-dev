# LINE Bot 互動問題診斷檢查表

## 🔍 診斷步驟

### 關鍵問題 1️⃣：Webhook URL 設定

**現象**：按鈕無法互動

**最可能原因**：Webhook URL 在 LINE Developers 中設定**錯誤**

---

## 🎯 請檢查 LINE Developers 中的設定

### 第一步：進入 LINE Developers

1. 打開 https://developers.line.biz/zh-hant/
2. 登入您的帳戶
3. 進入「Channels」
4. 選擇其中一個部門（例如：HK 房務部）

### 第二步：檢查 Webhook URL

在 Channel 設定頁面找到「Webhook settings」

**應該看到的設定**（正確 ✅）：
```
Webhook URL: https://ace.89.com.tw/api/linebot/webhook
```

**可能看到的錯誤設定**（❌）：

| 錯誤範例 | 問題 |
|---------|------|
| `https://ace.89.com.tw/api/line/callback/LA` | ❌ 舊路由（已廢棄） |
| `https://ace.89.com.tw/api/linebot/webhook/HK` | ❌ 每個部門不同 URL |
| `https://ace.89.com.tw/api/linebot/webhook/` | ❌ 多了一個 `/` |
| `http://ace.89.com.tw/api/linebot/webhook` | ❌ 用 HTTP 而非 HTTPS |
| `https://localhost:8000/api/linebot/webhook` | ❌ 本地地址，無法從 LINE 訪問 |

---

## ✅ 正確的設定步驟

### 步驟 1：編輯 Webhook URL

1. 在「Webhook settings」找到「Edit」按鈕
2. 清空現有的 URL
3. 輸入新的 URL：
   ```
   https://ace.89.com.tw/api/linebot/webhook
   ```
4. 點擊「Save」或「確定」

### 步驟 2：驗證 Webhook

1. 點擊「Verify」按鈕
2. **應該看到** ✅ 「Webhook URL is valid」（綠色勾選）
3. 如果看到 ❌ 404 錯誤，表示：
   - URL 格式錯誤
   - 伺服器沒有運行
   - 伺服器沒有正確返回 200 OK

### 步驟 3：確保 Webhook 已啟用

1. 找到「Use webhook」開關
2. 確保已**打開**（綠色）

### 步驟 4：重複所有 12 個部門

需要對所有部門都執行上述步驟：
- [ ] GS (客務部)
- [ ] HK (房務部)
- [ ] CON (門房諮詢)
- [ ] BP (烘焙點心房)
- [ ] FB (餐飲)
- [ ] CBS (會議宴會)
- [ ] FS (花房)
- [ ] LUR (洗衣房與制服室)
- [ ] GAE (總務工程)
- [ ] BB (飲料酒吧)
- [ ] AD (美術設計)
- [ ] LA (休閒活動部)

---

## 🔴 常見錯誤設定

### 錯誤 1：使用舊的路由

```
❌ https://ace.89.com.tw/api/line/callback/{department_code}
❌ https://ace.89.com.tw/api/linebot/webhook/{department_code}
```

**為什麼不行**：
- 我們改成了統一路由
- 舊的路由已刪除
- 每個部門應該用相同的 URL

### 錯誤 2：每個部門用不同的 URL

```
GS:  ❌ https://ace.89.com.tw/api/linebot/webhook/GS
HK:  ❌ https://ace.89.com.tw/api/linebot/webhook/HK
CON: ❌ https://ace.89.com.tw/api/linebot/webhook/CON
```

**為什麼不行**：
- 系統無法在這些 URL 上自動識別部門
- 簽名驗證失敗

---

## 📝 現在的系統架構

```
LINE 用戶點擊按鈕
        ↓
LINE 平台發送 Postback 到：
https://ace.89.com.tw/api/linebot/webhook
        ↓
我們的伺服器收到請求
        ↓
根據 X-Line-Signature（加密簽名）
自動判斷是哪個部門
        ↓
轉發給該部門的 LINE Bot 處理
```

---

## 🚨 診斷方式

### 如果修改 URL 後仍然無法互動

請檢查以下項目：

1. **Webhook 驗證是否通過？**
   - 在 LINE Developers 中點擊「Verify」
   - 應該看到 ✅（綠色勾選），不是 ❌ 404 錯誤

2. **伺服器是否在運行？**
   ```powershell
   netstat -ano | Select-String "8000"
   ```
   應該看到埠 8000 在 LISTENING（監聽中）

3. **伺服器日誌中有沒有錯誤？**
   - 查看伺服器終端是否有 `[ERROR]` 訊息

4. **Channel Secret 是否正確？**
   - 在 LINE Developers 中檢查 Channel Secret
   - 確認與資料庫中的相符

---

## 📊 檢查清單

完成以下所有項目才能解決問題：

- [ ] **確認 Webhook URL 正確**
  - 所有 12 個部門都設定為：`https://ace.89.com.tw/api/linebot/webhook`
  - （不是每個部門不同的 URL）

- [ ] **驗證每個部門的 Webhook**
  - 在 LINE Developers 中點擊「Verify」
  - 12 個部門都應該顯示 ✅（綠色勾選）

- [ ] **確認 Webhook 已啟用**
  - 「Use webhook」開關已打開（綠色）
  - 所有 12 個部門都已啟用

- [ ] **確認伺服器在運行**
  - 伺服器進程已啟動
  - 埠 8000 在監聽

- [ ] **測試互動**
  - 在 LINE 上點擊任務按鈕
  - 觀察是否有反應

---

## 💡 如何確認互動成功

當您點擊 LINE 上的按鈕時，應該看到：

1. **LINE 上**：立即顯示回覆訊息（例如：✅ 您已接受此派工任務！）
2. **伺服器日誌**：自動打印類似以下內容：
   ```
   [Webhook] 收到統一端點請求
   [Webhook] [OK] 簽名匹配部門: HK (房務部)
   [Postback] 收到事件，部門: HK
   [LINEBot 任務] {'department': 'HK', 'op': 'accept', ...}
   ```

---

## 🎯 立即行動

1. **打開 LINE Developers**
2. **逐個檢查所有 12 個部門的 Webhook URL**
3. **確保所有部門都使用相同的 URL**：`https://ace.89.com.tw/api/linebot/webhook`
4. **點擊 Verify 驗證每個部門**（應該全部通過）
5. **在 LINE 上測試點擊按鈕**

這應該能解決問題。如果仍然有問題，請告訴我：
- Webhook URL 目前設定為什麼？
- Verify 是否通過（顯示 ✅ 或 ❌）？
- 伺服器日誌中有沒有看到 `[Webhook]` 或 `[Postback]` 的訊息？

