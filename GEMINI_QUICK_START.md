# Gemini API 快速參考

## 🎯 5 分鐘設置

### 1. 獲取 API 金鑰
```
https://aistudio.google.com/app/apikey → 點擊 "Create API Key"
```

### 2. 設置環境變數
```bash
# .env 檔案
GEMINI_API_KEY=AIzaSyD...your-key...
```

### 3. 安裝依賴
```bash
pip install google-generativeai
```

### 4. 啟動應用
```bash
python run.py
```

### 5. 測試
```
訪問 http://localhost:8000/mbti
```

---

## 🔧 核心代碼變更

### 初始化
```python
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.0-flash")
```

### 調用 API
```python
response = model.generate_content(
    [text_prompt, image_part1, image_part2, ...],
    generation_config=genai.types.GenerationConfig(
        max_output_tokens=2000,
        temperature=0.7,
    )
)
result = response.text
```

### 影像處理
```python
image_data = base64.b64decode(base64_string)
image_part = genai.types.Part.from_data(
    data=image_data,
    mime_type="image/jpeg"
)
```

---

## 📊 API 限制

| 限制 | 值 |
|------|-----|
| 免費 RPM | 15 |
| 免費 Token/天 | 1,000,000 |
| 單個請求大小 | 20MB |
| 上下文窗口 | 1,000,000 tokens |

---

## 💡 最佳實踐

✅ 使用環境變數存儲 API 金鑰
✅ 設定 max_output_tokens 限制成本
✅ 使用 temperature 調整創意度
✅ 實施錯誤處理和重試邏輯
✅ 定期檢查 API 使用配額

---

## 🚨 常見錯誤

| 錯誤 | 解決方案 |
|------|---------|
| `ValueError: The API key is not valid` | 檢查 API 金鑰是否正確 |
| `ResourceExhausted` | 超過配額限制，稍後重試 |
| `PermissionDenied` | 金鑰無效或已過期 |
| `Response blocked by safety filters` | 內容被安全過濾，修改提示詞 |

---

## 📈 費用估計

### 每月 100 次分析
- **輸入 tokens**: ~5,000
- **輸出 tokens**: ~1,000
- **成本**: ~$0.002 (幾乎免費)

### 每月 10,000 次分析
- **輸入 tokens**: ~500,000
- **輸出 tokens**: ~100,000
- **成本**: ~$0.20 (極其便宜)

### 每月 100,000 次分析
- **輸入 tokens**: ~5,000,000
- **輸出 tokens**: ~1,000,000
- **成本**: ~$2 (仍然很便宜)

---

## 🔄 更新日誌

- ✅ **2025-12-12**: 從 OpenAI 遷移到 Gemini 2.0 Flash
- ✅ 安裝 google-generativeai
- ✅ 重寫 mbti_service.py
- ✅ 更新 requirements.txt
- ✅ 更新 config.py

---

## 📞 支持

- [Google AI Studio](https://aistudio.google.com/)
- [API 文檔](https://ai.google.dev/docs)
- [Python SDK](https://github.com/google/generative-ai-python)

---

**現在開始使用 Gemini！** 🚀
