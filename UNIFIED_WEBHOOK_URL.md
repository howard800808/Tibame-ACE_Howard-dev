# 統一 Webhook URL 設計說明

## 🎯 核心概念

**是的，所有 12 個部門應該使用相同的 Webhook URL。**

### 架構圖

```
┌──────────────────────────────────────────────────────────┐
│           LINE Developers（12 個頻道）                    │
│                                                           │
│  GS 頻道  HK 頻道  CON 頻道  ...  LA 頻道                │
│     │        │        │              │                   │
│     └────────┴────────┴──────────────┘                   │
│            全部指向同一個 Webhook URL                     │
│                                                           │
│  https://ace.89.com.tw/api/linebot/webhook              │
└──────────────────────────────────────────────────────────┘
                         ↓
                   ┌─────────────┐
                   │  我們的伺服器  │
                   │  Webhook    │
                   │  統一端點    │
                   └──────┬──────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ↓                 ↓                 ↓
    簽名驗證          提取 Channel Secret   自動路由到
    找出部門          並識別請求來自哪個   正確部門
                      部門的頻道
```

---

## 🔑 工作原理

### 當 LINE 發送 Postback 事件時：

```
1. 用戶在 LINE 上點擊任務按鈕
   ↓
2. LINE 平台發送 POST 請求到：
   https://ace.89.com.tw/api/linebot/webhook
   
   - Header: X-Line-Signature = <加密簽名>
   - Body: { "events": [{...}] }
   
   ↓
3. 伺服器接收請求
   ↓
4. 驗證 X-Line-Signature：
   ✅ 嘗試用 GS 的 Channel Secret 驗證 → 失敗
   ✅ 嘗試用 HK 的 Channel Secret 驗證 → ✅ 成功！
   
   ↓
5. 知道這個請求來自 HK 部門
   ↓
6. 將請求轉發給 HK 部門的處理器
   ↓
7. HK 部門的 LINE Bot 回覆
```

---

## ✅ 優點

| 優點 | 說明 |
|------|------|
| **簡化部署** | 所有 12 個部門共享 1 個 URL，而非 12 個 |
| **自動路由** | 系統自動根據簽名識別部門，無需手動配置 |
| **易於維護** | 只需維護 1 個 Webhook URL，而非 12 個 |
| **彈性擴展** | 未來新增部門時，無需修改 Webhook 設定 |

---

## ⚠️ 關鍵要求

### 在 LINE Developers 中

所有 12 個部門的 Channel 都必須設定**相同的 Webhook URL**：

```
所有部門的 Webhook URL：
https://ace.89.com.tw/api/linebot/webhook
```

### 不是這樣（❌ 錯誤）：
```
GS 部門:  https://ace.89.com.tw/api/linebot/webhook/GS
HK 部門:  https://ace.89.com.tw/api/linebot/webhook/HK
CON 部門: https://ace.89.com.tw/api/linebot/webhook/CON
...
```

### 應該是這樣（✅ 正確）：
```
GS 部門:  https://ace.89.com.tw/api/linebot/webhook
HK 部門:  https://ace.89.com.tw/api/linebot/webhook
CON 部門: https://ace.89.com.tw/api/linebot/webhook
...（所有 12 個都相同）
```

---

## 🔍 如何驗證

### 方法 1：查看 LINE Developers

1. 打開 LINE Developers
2. 進入每個 Channel（GS、HK、CON 等）
3. 找到「Webhook settings」
4. 檢查 Webhook URL

**預期結果**：所有 12 個頻道的 Webhook URL 都是：
```
https://ace.89.com.tw/api/linebot/webhook
```

### 方法 2：查詢資料庫

由於我們的設計中，部門 model 沒有儲存 Webhook URL（因為是統一的），所以無法從資料庫查詢。

只有 `access_token` 和 `channel_secret` 是每個部門獨有的：
```python
# 部門資料庫中的字段
- code: "HK"  # 部門代碼
- name: "房務部"  # 部門名稱
- access_token: "..." # 每個部門獨有
- channel_secret: "..."  # 每個部門獨有（用於簽名驗證）
```

---

## 📝 檢查清單

- [ ] 已進入 LINE Developers
- [ ] 檢查了 GS 部門的 Webhook URL
- [ ] 檢查了 HK 部門的 Webhook URL
- [ ] 檢查了 CON 部門的 Webhook URL
- [ ] ... 檢查了其他 9 個部門的 Webhook URL
- [ ] **確認所有 12 個都是：`https://ace.89.com.tw/api/linebot/webhook`**

---

## 🚨 常見問題

### Q1：如果不同部門設定了不同的 Webhook URL 會怎樣？

❌ **會導致以下問題**：
- 部門 A 的 Webhook 會收不到部門 B 的事件
- Postback 事件無法被正確路由
- 按鈕互動可能部分工作、部分不工作

### Q2：如果某個部門的 Webhook URL 不同，該怎麼修改？

1. 打開 LINE Developers
2. 進入該部門的 Channel
3. 找到「Webhook settings」
4. 點擊「Edit」
5. 改為：`https://ace.89.com.tw/api/linebot/webhook`
6. 保存

### Q3：修改後需要重新驗證嗎？

是的，建議執行以下步驟：
1. 修改 Webhook URL
2. 點擊「Verify」按鈕，確保伺服器能響應
3. 確認顯示 ✅ 驗證成功

---

## 📊 理想狀態

| 部門代碼 | 部門名稱 | Webhook URL | 狀態 |
|---------|---------|------------|------|
| GS | 客務部 | https://ace.89.com.tw/api/linebot/webhook | ✅ |
| HK | 房務部 | https://ace.89.com.tw/api/linebot/webhook | ✅ |
| CON | 門房諮詢 | https://ace.89.com.tw/api/linebot/webhook | ✅ |
| BP | 烘焙點心房 | https://ace.89.com.tw/api/linebot/webhook | ✅ |
| FB | 餐飲 | https://ace.89.com.tw/api/linebot/webhook | ✅ |
| CBS | 會議宴會 | https://ace.89.com.tw/api/linebot/webhook | ✅ |
| FS | 花房 | https://ace.89.com.tw/api/linebot/webhook | ✅ |
| LUR | 洗衣房與制服室 | https://ace.89.com.tw/api/linebot/webhook | ✅ |
| GAE | 總務工程 | https://ace.89.com.tw/api/linebot/webhook | ✅ |
| BB | 飲料酒吧 | https://ace.89.com.tw/api/linebot/webhook | ✅ |
| AD | 美術設計 | https://ace.89.com.tw/api/linebot/webhook | ✅ |
| LA | 休閒活動部 | https://ace.89.com.tw/api/linebot/webhook | ✅ |

---

## 🎯 行動項目

1. **檢查所有 12 個部門的 Webhook URL** → 確認都相同
2. **如果發現不同的 URL** → 全部改為 `https://ace.89.com.tw/api/linebot/webhook`
3. **逐個驗證** → 點擊「Verify」按鈕，確保所有部門都通過驗證
4. **測試** → 在 LINE 上點擊按鈕，確認 Postback 事件被正確處理

