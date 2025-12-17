# 🎯 Azure Speech-to-Text 快速開始指南

## ✨ 新增功能概覽

您的影片分析系統現在已升級，支持：

### 📹 自動語音轉文字
- ✅ 自動提取影片音軌
- ✅ Azure Cognitive Services 高精度識別
- ✅ 繁體/簡體中文識別（可配置）
- ✅ 說話人自動分段和識別

### 🎙️ 多說話人支持
- ✅ 自動檢測影片中有多少位說話人
- ✅ 按說話人分色彩展示對話內容
- ✅ 每段對話附帶時間戳
- ✅ 信心度指標

### 📊 完整分析結果
同時提供：
- 🧠 **情緒分析** - 逐幀情感檢測 (AWS Rekognition)
- 🎤 **對話轉錄** - 語音轉文字 (Azure Speech)
- 📈 **統計圖表** - 情緒趨勢和話題分布

---

## 🚀 快速使用

### 1️⃣ 訪問應用
```
http://127.0.0.1:8000/video-analysis
```

### 2️⃣ 上傳影片
支持的格式：MP4、WMV、AVI、MOV、MKV、WebM（最大 500MB）

### 3️⃣ 查看結果
等待分析完成後，可查看：
- 📊 情緒統計
- 📈 情緒時間線
- 🎤 說話人對話內容

---

## 📋 系統要求檢查清單

- ✅ Python 3.12+
- ✅ FFmpeg 8.0.1+ (已安裝)
- ✅ Azure Speech SDK (已安裝)
- ✅ 所有 Python 依賴 (已安裝)

### Azure 配置驗證
已在 `.env` 配置以下信息：
```
✓ AZURE_SPEECH_API_KEY
✓ AZURE_SPEECH_ENDPOINT  
✓ AZURE_SPEECH_REGION
```

---

## 🎨 前端顯示特性

### 說話人分段顯示
```
┌─────────────────────────────────────────────┐
│ 🎙️ Speaker 1            00:00 - 00:05       │
│ 你好，我是第一位說話人。     信心度: 92%    │
├─────────────────────────────────────────────┤
│ 🎙️ Speaker 2            00:05 - 00:10       │
│ 你好，我是第二位說話人。     信心度: 88%    │
└─────────────────────────────────────────────┘
```

### 顏色編碼
- 🟦 **Speaker 1**: 藍色
- 🟪 **Speaker 2**: 紫色
- 🟥 **Speaker 3+**: 其他顏色自動分配

---

## 📞 常見問題 (FAQ)

### Q: 為什麼沒有顯示轉錄結果？
**A**: 檢查以下幾點：
1. 影片是否包含音軌
2. 影片長度是否合理（< 1 小時）
3. 音軌清晰度是否足夠
4. Azure 配置是否正確 (金鑰、端點、區域)

### Q: 如何改變識別語言？
**A**: 編輯 `app/services/video_service.py` 第 208 行：
```python
language='zh-Hans'  # 改為 'zh-Hant' 為繁體中文
```

### Q: 說話人識別為什麼不準確？
**A**: 
- Azure Speech 的說話人識別準確度取決於音質
- 清晰、不混淆的多說話人音頻效果最佳
- 音樂或背景噪音可能會影響準確性

### Q: 如何進行測試？
**A**: 
```bash
python test_azure_setup.py
```

---

## 🔧 技術細節

### 音軌處理流程
```
影片 (MP4/WebM/etc)
  ↓
FFmpeg 提取
  ↓
WAV 檔案 (16kHz, 16-bit PCM)
  ↓
Azure Speech API
  ↓
轉錄文字 + 說話人分段
  ↓
資料庫儲存 + 前端展示
```

### API 回應示例
```json
{
  "id": 1,
  "transcription_text": "你好，這是一個測試。你好，我是第二位說話人。",
  "speaker_segments": {
    "speaker_count": 2,
    "segments": [
      {
        "speaker": "Speaker 1",
        "start_time": 0.0,
        "end_time": 2.5,
        "content": "你好，這是一個測試。",
        "confidence": 0.92
      },
      {
        "speaker": "Speaker 2",
        "start_time": 2.5,
        "end_time": 5.0,
        "content": "你好，我是第二位說話人。",
        "confidence": 0.88
      }
    ]
  },
  "transcription_confidence": 0.90,
  "speaker_count": 2
}
```

---

## 📚 相關文件

| 檔案 | 功能 |
|------|------|
| `app/services/azure_transcription_service.py` | Azure Speech 集成模組 |
| `app/services/video_service.py` | 影片分析協調器 |
| `app/models/video.py` | 資料庫模型 |
| `templates/video_analysis.html` | 前端頁面 |
| `AZURE_SPEECH_SETUP.md` | 詳細配置指南 |

---

## 🎓 學習資源

- [Azure Cognitive Services 官方文檔](https://docs.microsoft.com/azure/cognitive-services/)
- [Azure Speech SDK for Python](https://docs.microsoft.com/en-us/python/api/overview/azure/cognitiveservices-speech-readme)
- [FFmpeg 文檔](https://ffmpeg.org/documentation.html)
- [FastAPI 教程](https://fastapi.tiangolo.com/)

---

## ✅ 部署檢查清單

在生產環境中部署前，請確認：

- [ ] `.env` 中的 Azure 金鑰已安全存儲
- [ ] 資料庫備份已設置
- [ ] CORS 配置已根據需要調整
- [ ] 日誌系統已配置
- [ ] 錯誤監控已設置 (如 Sentry)
- [ ] 性能監控已就位 (如 New Relic)
- [ ] 安全檢查已完成 (SSL, 輸入驗證)

---

## 🐛 故障排除

### 應用無法啟動
```bash
# 檢查依賴
pip install -r requirements.txt

# 檢查資料庫
python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"

# 重新啟動
python -m uvicorn run:app --host 127.0.0.1 --port 8000
```

### 轉錄失敗
```bash
# 檢查 Azure 金鑰
python -c "from app.core.config import settings; print(f'API Key: {settings.AZURE_SPEECH_API_KEY[:10]}...')"

# 檢查 FFmpeg
ffmpeg -version

# 檢查網絡連接
ping eastus.api.cognitive.microsoft.com
```

---

## 📞 支持和反饋

如遇到問題，請：
1. 檢查應用日誌
2. 查看 `AZURE_SPEECH_SETUP.md` 詳細指南
3. 執行 `test_azure_setup.py` 進行診斷

---

**🎉 系統已準備好！立即開始使用 Azure Speech-to-Text 進行強大的語音分析吧！**

---

版本: 1.0.0  
最後更新: 2025-12-16  
狀態: ✅ 生產就緒
