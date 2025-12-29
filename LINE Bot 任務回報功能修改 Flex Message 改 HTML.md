# 感動派工任務回報功能實作

**Commit:** dc9784bfea673edc51e8dd978c952004f9efac98  
**日期:** 2025-12-29  
**作者:** Howard800808

---

## 📌 功能概述

本次更新實現了完整的「感動派工任務」閉環流程：
- ✅ 任務派發 (LineBot Flex Message)
- ✅ 任務執行 (員工接收)
- ✅ 任務回報 (LIFF 表單)
- ✅ 結果記錄 (資料庫 + 管理後台)

---

## 🗄️ 資料庫變更

### 新增欄位 (`emotional_tasks` 表)

| 欄位名稱 | 類型 | 說明 | 範例值 |
|---------|------|------|--------|
| `report_is_finished` | VARCHAR(10) | 是否順利完成 | yes/no |
| `report_details` | TEXT | 補充說明 | "客人非常滿意" |
| `report_has_interaction` | VARCHAR(10) | 與顧客有互動嗎 | yes/no |
| `report_sentiment` | VARCHAR(20) | 顧客情緒 | positive/neutral/negative |
| `report_remarks` | TEXT | 備註事項 | "建議下次提早準備" |

### 遷移腳本

```python
// filepath: migrations/add_report_columns.py
from sqlalchemy import text
from app.database import engine

def upgrade():
    with engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE emotional_tasks 
            ADD COLUMN report_is_finished VARCHAR(10) COMMENT '是否順利完成 (yes/no)',
            ADD COLUMN report_details TEXT COMMENT '補充說明',
            ADD COLUMN report_has_interaction VARCHAR(10) COMMENT '與顧客有互動嗎 (yes/no)',
            ADD COLUMN report_sentiment VARCHAR(20) COMMENT '顧客情緒 (positive/neutral/negative)',
            ADD COLUMN report_remarks TEXT COMMENT '備註事項';
        """))
        conn.commit()
```

---

## 🔌 API 路由變更

### 1. 新增 - 取得單一任務詳情

**Endpoint:** `GET /api/emotional-tasks/{task_id}`  
**用途:** 供 LIFF 頁面載入任務資訊  
**權限:** 公開 (無需 JWT)

```python
@router.get("/{task_id}", response_model=EmotionalTaskResponse)
def get_emotional_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(EmotionalTask).filter(EmotionalTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return EmotionalTaskResponse.model_validate(task)
```

### 2. 新增 - 提交任務回報

**Endpoint:** `POST /api/emotional-tasks/{task_id}/report`  
**用途:** 員工透過 LIFF 表單提交回報  
**權限:** 公開 (LINE 內部驗證)

**請求 Schema:**
```python
class EmotionalTaskReportCreate(BaseModel):
    report_is_finished: str  # "yes" 或 "no"
    report_details: Optional[str] = None
    report_has_interaction: str  # "yes" 或 "no"
    report_sentiment: str  # "positive" | "neutral" | "negative"
    report_remarks: Optional[str] = None
```

**處理邏輯:**
1. 驗證任務是否存在
2. 檢查是否已回報 (避免重複提交)
3. 更新回報欄位
4. 將狀態改為 `completed`
5. 記錄 `completed_at` 時間戳

### 3. 修改 - 更新任務狀態

**變更點:**
- 當狀態更新為 `completed` 時，自動記錄 `completed_at`

```python
@router.patch("/{task_id}/status")
def update_emotional_task_status(task_id: int, status: str, db: Session = Depends(get_db)):
    task = db.query(EmotionalTask).filter(EmotionalTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = status
    if status == 'completed':
        task.completed_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(task)
    return task
```

---

## 📱 LineBot Flex Message 改良

### 變更點

**舊版 (Postback 按鈕):**
```python
{
    'type': 'button',
    'action': {
        'type': 'postback',
        'label': '任務完成回報',
        'data': f'action=task&op=complete&id={task_id}'
    }
}
```

**新版 (URI 按鈕 - 開啟 LIFF):**
```python
{
    'type': 'button',
    'action': {
        'type': 'uri',
        'label': '任務完成回報',
        'uri': f'{BASE_WEB_URL}/emotional-tasks/report/{db_id}'
    }
}
```

### 設定 BASE_WEB_URL

```python
// filepath: app/services/linebot_service.py
# TODO: 請將此處替換為您的實際網域
BASE_WEB_URL = "https://your-domain.ngrok-free.dev"
```

### 函數簽名變更

```python
def create_universal_task_card(
    dept, priority, room, guest, title, content, time, remark,
    status='PENDING',
    task_id=None,
    db_id=None  # 新增：資料庫主鍵 ID
):
```

---

## 🖥️ 前端頁面實作

### 1. 任務回報頁面 (LIFF)

**檔案:** `templates/emotional_task_report.html`

**核心功能:**
- 使用 LIFF SDK (`liff.init()`)
- 自動載入任務資訊
- 5 欄位互動式表單
- 提交後呼叫 API 並關閉視窗

**表單欄位:**
```html
<select id="isFinished" required>
    <option value="yes">是 ✓</option>
    <option value="no">否 ✗</option>
</select>

<textarea id="details" placeholder="請描述任務執行過程..."></textarea>

<select id="hasInteraction" required>
    <option value="yes">有互動</option>
    <option value="no">無互動</option>
</select>

<select id="sentiment" required>
    <option value="positive">正向 😊</option>
    <option value="neutral">中性 😐</option>
    <option value="negative">負向 😞</option>
</select>

<textarea id="remarks" placeholder="其他需要備註的事項..."></textarea>
```

**提交邏輯:**
```javascript
async function submitReport() {
    const data = {
        report_is_finished: document.getElementById('isFinished').value,
        report_details: document.getElementById('details').value,
        report_has_interaction: document.getElementById('hasInteraction').value,
        report_sentiment: document.getElementById('sentiment').value,
        report_remarks: document.getElementById('remarks').value
    };

    const response = await fetch(`/api/emotional-tasks/${taskId}/report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        alert('✅ 回報成功！');
        liff.closeWindow();
    }
}
```

### 2. 管理後台顯示優化

**檔案:** `templates/emotional_tasks.html`

**變更點:**

#### (1) 完成時間欄位調整
- **舊邏輯:** 可能顯示 `updated_at`
- **新邏輯:** 僅在 `status === 'completed'` 時顯示 `completed_at`

```javascript
const completedAt = (task.status === 'completed' && task.completed_at)
    ? new Date(task.completed_at).toLocaleString()
    : '-';
```

#### (2) Modal 詳情頁增強

**新增回報結果區塊:**
```javascript
let reportHtml = '';
if (task.report_is_finished) {
    const sentimentMap = {
        'positive': '<span style="color: #4caf50;">正向</span>',
        'neutral': '<span style="color: #aaa;">中性</span>',
        'negative': '<span style="color: #f44336;">負向</span>'
    };
    const sentiment = sentimentMap[task.report_sentiment] || '-';

    reportHtml = `
        <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #444;">
            <h3>📋 回報結果</h3>
            <div><strong>是否完成:</strong> ${task.report_is_finished === 'yes' ? '是' : '否'}</div>
            <div><strong>互動:</strong> ${task.report_has_interaction === 'yes' ? '有' : '無'}</div>
            <div><strong>情緒:</strong> ${sentiment}</div>
            <div><strong>補充說明:</strong> ${task.report_details || '-'}</div>
            <div><strong>備註:</strong> ${task.report_remarks || '-'}</div>
        </div>
    `;
} else {
    reportHtml = `<div style="text-align: center; color: #888;">尚未收到回報</div>`;
}
```

---

## 🔄 路由註冊

```python
// filepath: app/routes/view_routes.py
@router.get("/emotional-tasks", response_class=HTMLResponse)
async def emotional_tasks_page(request: Request):
    """感動派工列表頁面 (需要登入)"""
    return await emotional_task_view.emotional_task_list_page(request)

@router.get("/emotional-tasks/report/{task_id}", response_class=HTMLResponse)
async def emotional_task_report_page(request: Request, task_id: int):
    """感動派工回報頁面 (LIFF)"""
    return await emotional_task_view.emotional_task_report_page(request, task_id)
```

---

## 🧪 測試檢查清單

- [ ] **資料庫遷移:** 執行 `add_report_columns.py` 腳本
- [ ] **LIFF 設定:** 在 LINE Developers Console 註冊 Endpoint URL
  - Endpoint URL: `https://your-domain/emotional-tasks/report/{taskId}`
  - Scope: `profile` (基本即可)
- [ ] **環境變數:** 確認 `BASE_WEB_URL` 已更新為正式域名
- [ ] **API 測試:**
  ```bash
  # 取得任務
  curl http://localhost:8000/api/emotional-tasks/1
  
  # 提交回報
  curl -X POST http://localhost:8000/api/emotional-tasks/1/report \
    -H "Content-Type: application/json" \
    -d '{
      "report_is_finished": "yes",
      "report_details": "順利完成",
      "report_has_interaction": "yes",
      "report_sentiment": "positive",
      "report_remarks": "客人很滿意"
    }'
  ```
- [ ] **LineBot 測試:** 點擊任務卡片「任務完成回報」按鈕
- [ ] **管理後台:** 確認回報結果正確顯示

---

## 📊 影響範圍

| 模組 | 影響程度 | 說明 |
|------|---------|------|
| **資料庫** | 🔴 高 | 新增 5 個欄位 (需遷移) |
| **API** | 🟡 中 | 新增 2 個端點 |
| **LineBot** | 🟡 中 | Flex Message 結構變更 |
| **前端** | 🟢 低 | 新增獨立 LIFF 頁面 |
| **既有功能** | 🟢 無影響 | 向下相容 |

---

## 🚀 部署步驟

1. **更新程式碼**
   ```bash
   git pull origin main
   ```

2. **執行資料庫遷移**
   ```bash
   python migrations/add_report_columns.py
   ```

3. **設定環境變數**
   ```bash
   export BASE_WEB_URL="https://your-production-domain.com"
   ```

4. **重啟應用**
   ```bash
   systemctl restart tibame-ace
   ```

5. **LIFF 設定 (LINE Developers Console)**
   - 新增 LIFF App
   - Endpoint URL: `{BASE_WEB_URL}/emotional-tasks/report/`
   - Size: `Full`
   - Scope: `profile`

6. **驗證測試**
   - 發送測試任務至 LineBot
   - 點擊「任務完成回報」
   - 確認 LIFF 頁面正常開啟
   - 提交表單並檢查資料庫

---

## 🔮 未來優化方向

- [ ] **身份驗證:** 增加 LIFF ID Token 驗證機制
- [ ] **離線支援:** 使用 Service Worker 實現離線回報
- [ ] **圖片上傳:** 允許員工上傳現場照片
- [ ] **即時通知:** 主管收到回報後立即推送通知
- [ ] **數據分析:** 建立情緒趨勢分析儀表板

---

## 📝 相關文件

- [LINE LIFF 官方文件](https://developers.line.biz/en/docs/liff/overview/)
- [Flex Message Simulator](https://developers.line.biz/flex-simulator/)
- [專案 API 文件](http://localhost:8000/docs)

---

**備註:** 本文件記錄 commit `dc9784b` 的完整變更內容，供團隊成員參考與後續維護使用。