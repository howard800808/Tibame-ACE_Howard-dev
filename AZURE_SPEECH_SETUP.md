# Azure Speech-to-Text 集成指南

## ✅ 完成的功能

### 1. Azure Speech-to-Text 集成
- ✅ 從影片中提取音軌（WAV 格式，16kHz 單聲道）
- ✅ 使用 Azure Cognitive Services 進行語音轉文字
- ✅ 支持說話人識別（Speaker Diarization）
- ✅ 分段顯示不同說話人的對話

### 2. 後端實現
已安裝並配置的服務：
- **azure-cognitiveservices-speech** (v1.47.0) - Azure Speech SDK
- **ffmpeg-python** - 音軌提取
- **系統 FFmpeg** - 音頻處理

### 3. 資料庫更新
VideoAnalysis 模型新增字段：
```python
speaker_segments = Column(Text, nullable=True, comment="說話人分段結果 (JSON)")
speaker_count = Column(Integer, default=0, comment="檢測到的說話人數量")
```

### 4. 前端更新
- ✅ 顯示說話人數量
- ✅ 按說話人分色彩顯示對話內容
- ✅ 顯示每段對話的時間戳和信心度
- ✅ 完整轉錄文字展示

---

## 📋 配置信息

### 環境變數 (.env)
```
AZURE_SPEECH_API_KEY=5KTW9kudEOhqlJMVXFJGUjDVZ9qq1FhqLsHIye0NlfeWsKhE05IBJQQJ99BLACYeBjFXJ3w3AAAYACOGslsW
AZURE_SPEECH_ENDPOINT=https://eastus.api.cognitive.microsoft.com/
AZURE_SPEECH_REGION=eastus
```

### 新增文件
- **app/services/azure_transcription_service.py** - Azure Speech-to-Text 服務模組

### 修改文件
1. **app/core/config.py** - 添加 Azure 配置
2. **app/models/video.py** - 添加說話人字段
3. **app/services/video_service.py** - 集成 Azure 服務
4. **templates/video_analysis.html** - 更新前端顯示
5. **requirements.txt** - 添加依賴

---

## 🚀 工作流程

### 1. 影片上傳
用戶上傳影片檔案 → FastAPI 驗證格式和大小

### 2. 背景分析
```
並行執行：
├─ 幀分析 (情緒分析)
│  ├─ 提取每 5 幀
│  ├─ 調用 AWS Rekognition
│  └─ 保存情緒數據
│
└─ 音軌提取和轉錄
   ├─ FFmpeg 提取音軌 (WAV, 16kHz)
   ├─ Azure Speech 識別
   ├─ 說話人分段
   └─ 保存轉錄結果
```

### 3. 結果展示
- **情緒分析**：情緒統計、時間線、視覺化圖表
- **語音轉文字**：
  - 完整對話文字
  - 按說話人分色彩展示
  - 時間戳和信心度

---

## 📊 API 響應格式

### 說話人分段結構
```json
{
  "speaker_segments": {
    "speaker_count": 2,
    "segments": [
      {
        "speaker": "Speaker 1",
        "start_time": 0.0,
        "end_time": 2.5,
        "content": "你好，這是第一句話。",
        "confidence": 0.92
      },
      {
        "speaker": "Speaker 2",
        "start_time": 2.5,
        "end_time": 5.0,
        "content": "你好，我是第二位說話人。",
        "confidence": 0.88
      }
    ],
    "full_text": "你好，這是第一句話。你好，我是第二位說話人。"
  }
}
```

---

## ⚙️ 技術堆棧

| 組件 | 版本 | 用途 |
|------|------|------|
| FastAPI | ≥0.109.0 | Web 框架 |
| OpenCV | ≥4.8.0.0 | 影片處理 |
| FFmpeg | 8.0.1 | 音軌提取 |
| Azure Speech SDK | 1.47.0 | 語音轉文字 |
| SQLAlchemy | ≥2.0.0 | 數據持久化 |
| Boto3 | ≥1.28.0 | AWS 服務 |

---

## 🔧 故障排除

### 1. "FFmpeg 未安裝"
**解決方案**：
```powershell
choco install ffmpeg  # Windows (Chocolatey)
brew install ffmpeg   # macOS
sudo apt-get install ffmpeg  # Linux
```

### 2. "Azure Speech SDK 未安裝"
**解決方案**：
```bash
pip install azure-cognitiveservices-speech
```

### 3. Azure API 認證失敗
**檢查**：
- `.env` 中 `AZURE_SPEECH_API_KEY` 是否正確
- `AZURE_SPEECH_REGION` 是否有效（例如：eastus, westus2）
- Azure 帳戶是否有足夠配額

### 4. 轉錄不顯示或為空
**檢查**：
- 影片是否包含音軌
- 音軌語言是否與 `language='zh-Hans'` 配置匹配
- 影片時長是否超過 1 小時（Azure 限制）

---

## 📱 前端顯示功能

### 說話人分段色彩編碼
- **Speaker 1**: 藍色 (#667eea)
- **Speaker 2**: 紫色 (#764ba2)
- **Speaker 3**: 粉色 (#f093fb)
- **Speaker 4**: 淺藍 (#4facfe)
- **Speaker 5**: 綠色 (#43e97b)
- **Speaker 6**: 紅粉 (#fa709a)

### 信息顯示
- ✓ 說話人數量
- ✓ 對話內容
- ✓ 時間戳 (HH:MM:SS)
- ✓ 信心度百分比

---

## 🔮 未來增強計劃

1. **實時轉錄**：使用 WebSocket 進行實時語音轉文字
2. **情感傾向分析**：分析每位說話人的情感傾向
3. **話題提取**：自動提取對話主題和關鍵詞
4. **多語言支持**：支持自動語言檢測和翻譯
5. **說話人識別**：更精確的說話人身份識別

---

## 📝 使用示例

### Python 調用
```python
from app.services.azure_transcription_service import azure_transcription_service

# 轉錄視頻
success, text, segments, confidence = azure_transcription_service.transcribe_video(
    video_path="/path/to/video.mp4",
    language="zh-Hans"  # 簡體中文
)

if success:
    print(f"轉錄成功: {text}")
    print(f"說話人數: {len(set(s['speaker'] for s in segments))}")
    for seg in segments:
        print(f"{seg['speaker']}: {seg['content']}")
```

### JavaScript 調用
```javascript
// 獲取分析結果
const response = await fetch('/api/video-analysis/1');
const data = await response.json();

// 說話人分段
const speakerData = JSON.parse(data.speaker_segments);
console.log(`檢測到 ${speakerData.speaker_count} 位說話人`);

speakerData.segments.forEach(seg => {
    console.log(`${seg.speaker} (${seg.start_time}s): ${seg.content}`);
});
```

---

## 📞 支持

如有問題，請檢查：
1. 應用日誌輸出
2. 網絡連接（能否訪問 Azure 端點）
3. API 金鑰和區域配置
4. FFmpeg 安裝狀態

---

**版本**: 1.0.0  
**最後更新**: 2025-12-16  
**狀態**: ✅ 已完成
