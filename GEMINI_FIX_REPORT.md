# Gemini API 修復報告

## ❌ 問題診斷

**錯誤訊息**: 
```
MBTI 預測失敗: module 'google.generativeai.types' has no attribute 'Part'
```

**根本原因**:
- `google.generativeai.types.Part.from_data()` 不是正確的 API 調用方式
- `genai.types.GenerationConfig()` 在某些版本中無法正確使用

---

## ✅ 解決方案

### 1️⃣ 修復影像處理格式

**之前 (錯誤)**:
```python
content_parts.append(
    genai.types.Part.from_data(
        data=image_data,
        mime_type="image/jpeg"
    )
)
```

**之後 (正確)**:
```python
content_parts.append({
    "mime_type": "image/jpeg",
    "data": base64_string,
})
```

### 2️⃣ 修復 generation_config 格式

**之前 (錯誤)**:
```python
generation_config=genai.types.GenerationConfig(
    temperature=0.7,
    max_output_tokens=2000,
)
```

**之後 (正確)**:
```python
generation_config={
    "temperature": 0.7,
    "max_output_tokens": 2000,
}
```

### 3️⃣ 添加 API 金鑰驗證

**新增**:
```python
def __init__(self):
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY 未設置，請在 .env 檔案中設置")
    genai.configure(api_key=settings.GEMINI_API_KEY)
    self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
```

---

## 📋 更新的檔案

### [app/services/mbti_service.py](app/services/mbti_service.py)

**變更內容**:
- ✅ 修復了影像處理的 API 調用方式
- ✅ 修復了 generation_config 的格式
- ✅ 添加了 API 金鑰驗證
- ✅ 簡化了 content 結構

---

## 🧪 驗證步驟

### 步驟 1: 確保 API 金鑰已設置

```env
# .env 檔案
GEMINI_API_KEY=AIzaSyD...your-api-key...
```

### 步驟 2: 重新啟動應用

```bash
python run.py
```

### 步驟 3: 測試 MBTI 分析

訪問 http://localhost:8000/mbti 並上傳影片

### 步驟 4: 檢查結果

如果看到 MBTI 類型和分析結果，則修復成功！

---

## 🔍 技術細節

### Gemini API 正確使用方式

```python
# 初始化
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.0-flash")

# 調用 API
content = [
    "This is text",
    {
        "mime_type": "image/jpeg",
        "data": base64_encoded_image_string,
    }
]

response = model.generate_content(
    content,
    generation_config={
        "temperature": 0.7,
        "max_output_tokens": 2000,
    }
)

result = response.text
```

### 關鍵區別

| 項目 | 錯誤方式 | 正確方式 |
|------|---------|---------|
| **影像格式** | `Part.from_data()` | Dict with mime_type |
| **Config** | `genai.types.GenerationConfig()` | 字典 |
| **驗證** | 無 | 在 __init__ 驗證 |

---

## 📊 修復前後對比

### 修復前
```
上傳影片 → 分析 → ❌ 錯誤: Part 不存在
```

### 修復後
```
上傳影片 → 驗證 API 金鑰 → 提取幀 → 調用 Gemini API → ✅ 返回結果
```

---

## 🚀 下一步

1. ✅ 確保 `.env` 中有 `GEMINI_API_KEY`
2. ✅ 運行應用: `python run.py`
3. ✅ 訪問 http://localhost:8000/mbti
4. ✅ 上傳影片進行測試

---

## 💡 常見問題

**Q: 還是收到錯誤？**
A: 檢查以下項目：
- [ ] GEMINI_API_KEY 已在 .env 中設置
- [ ] google-generativeai 已安裝: `pip install google-generativeai`
- [ ] 檔案已保存並應用更改
- [ ] 應用已重新啟動

**Q: 如何獲取 Gemini API 金鑰？**
A: 訪問 https://aistudio.google.com/app/apikey

**Q: 需要安裝額外依賴嗎？**
A: 僅需要 `google-generativeai` (已在 requirements.txt 中)

---

## ✨ 修復完成

所有修復已應用！系統現在應該能正常分析影片並預測 MBTI 了。

祝使用愉快！🎉
