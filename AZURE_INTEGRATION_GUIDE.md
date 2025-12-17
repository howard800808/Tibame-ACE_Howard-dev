# 📚 Azure 语音转文字集成 - 快速参考

## 🏗️ 架构概览

```
视频上传
   ↓
┌─────────────────────────┐
│ VideoController         │  (app/controllers/video_controller.py)
│ - 处理上传请求          │
│ - 管理数据库记录        │
└──────────────┬──────────┘
               ↓
┌─────────────────────────┐
│ VideoService            │  (app/services/video_service.py)
│ - 协调处理流程          │
│ - 并行处理情感+转录      │
└──────────────┬──────────┘
               ↓
       ┌───────┴────────┐
       ↓                ↓
┌─────────────┐  ┌──────────────────────┐
│ Emotion     │  │ Azure Transcription  │
│ Service     │  │ Service              │
│ (AWS)       │  │ (Azure)              │
└─────────────┘  └──────────┬───────────┘
                            ↓
                  ┌─────────────────────┐
                  │ FFmpeg Audio Extract│
                  │ ↓ Azure Speech API  │
                  │ ↓ Speaker Detection │
                  │ ↓ Confidence Score  │
                  └─────────────────────┘
                            ↓
                  ┌─────────────────────┐
                  │ 保存到数据库        │
                  │ - transcription_json│
                  │ - speaker_segments  │
                  │ - speaker_count     │
                  └─────────────────────┘
```

---

## 🔑 核心文件

### 1️⃣ Azure 转录服务 (app/services/azure_transcription_service.py)

**主要方法:**

```python
# 端到端转录
transcribe_video(video_path) 
  ↓ 返回: {
    'success': True,
    'text': '转录文本',
    'speaker_count': 1,
    'segments': [
      {
        'speaker': 'Speaker 1',
        'start_time': 0.0,
        'end_time': 10.5,
        'content': '...',
        'confidence': 0.85
      }
    ],
    'full_text': '...'
  }

# 音频提取 (FFmpeg)
extract_audio_from_video(video_path)
  ↓ 返回: /tmp/audio.wav

# Azure 转录 + 说话人识别
transcribe_with_diarization(audio_path)
  ↓ 返回: Azure SpeechRecognitionResult (带说话人信息)
```

**关键配置:**
```python
LANGUAGE_CODE = "zh-TW"  # 繁體中文
SPEECH_RECOGNITION_LANGUAGE = "zh-TW"
```

---

### 2️⃣ 视频服务 (app/services/video_service.py)

**集成点:**
```python
# 第 201 行
result = azure_transcription_service.transcribe_video(
    str(video_path)
)

# 结果处理
if result['success']:
    # 保存转录数据
    db_video.transcription_json = json.dumps(result)
    db_video.speaker_count = result['speaker_count']
    # ... 等等
```

---

### 3️⃣ 视频控制器 (app/controllers/video_controller.py)

**获取分析详情 (行 160-206):**
```python
@router.get("/analyze/{video_id}", response_model=VideoAnalysisDetailResponse)
async def get_analysis_detail(video_id: int, db: Session = Depends(get_db)):
    # 获取数据库记录
    db_video = db.query(Video).filter(Video.id == video_id).first()
    
    # 解析 transcription_json（从字符串转为对象）
    transcription_json = None
    if db_video.transcription_json:
        try:
            transcription_json = json.loads(db_video.transcription_json)
            if not isinstance(transcription_json, list):
                transcription_json = [transcription_json] if transcription_json else None
        except:
            transcription_json = None
    
    # 返回完整响应
    return VideoAnalysisDetailResponse(
        id=db_video.id,
        transcription_json=transcription_json,
        speaker_segments=db_video.speaker_segments,
        speaker_count=db_video.speaker_count,
        # ... 其他字段
    )
```

---

## 🗄️ 数据库字段

### video_analysis 表新增列

```sql
-- 转录数据（JSON 格式）
transcription_json TEXT

-- 说话人分段数据（JSON 格式）
speaker_segments TEXT

-- 说话人数量
speaker_count INTEGER DEFAULT 0
```

**数据格式示例:**
```json
{
  "speaker_count": 1,
  "segments": [
    {
      "speaker": "Speaker 1",
      "start_time": 0.0,
      "end_time": 10.5,
      "content": "请问今天是否有空的双人房间？",
      "confidence": 0.85
    }
  ],
  "full_text": "请问今天是否有空的双人房间？我们需要借一间双人房..."
}
```

---

## ⚙️ 环境配置

### .env 文件
```dotenv
# Azure Speech-to-Text 配置
AZURE_SPEECH_API_KEY=5KTW9kudEOhqlJMVXFJGUjDVZ9qq1FhqLsHIye0NlfeWsKhE05IBJQQJ99BLACYeBjFXJ3w3AAAYACOGslsW
AZURE_SPEECH_ENDPOINT=https://eastus.api.cognitive.microsoft.com/
AZURE_SPEECH_REGION=eastus
```

### 应用配置 (app/core/config.py)
```python
AZURE_SPEECH_API_KEY: Optional[str] = None
AZURE_SPEECH_ENDPOINT: Optional[str] = None
AZURE_SPEECH_REGION: str = "eastus"
```

---

## 🎯 使用示例

### 1. 上传视频进行分析

```bash
curl -X POST http://127.0.0.1:8000/api/videos/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@video.mp4" \
  -F "description=测试视频"
```

**响应:**
```json
{
  "id": 1,
  "filename": "video.mp4",
  "status": "processing"
}
```

### 2. 获取分析结果

```bash
curl -X GET http://127.0.0.1:8000/api/videos/analyze/1 \
  -H "Authorization: Bearer <token>"
```

**响应:**
```json
{
  "id": 1,
  "filename": "video.mp4",
  "status": "completed",
  "transcription_json": [
    {
      "speaker": "Speaker 1",
      "start_time": 0.0,
      "end_time": 10.5,
      "content": "...",
      "confidence": 0.85
    }
  ],
  "speaker_count": 1,
  "speaker_segments": "[...]",
  "emotion_analysis": {...},
  "created_at": "2024-01-01T00:00:00"
}
```

---

## 🔄 处理流程详解

### 步骤 1: 接收上传
```
POST /api/videos/upload
  ↓ 验证文件格式 (MP4, MOV, AVI 等)
  ↓ 保存到本地存储
  ↓ 创建数据库记录 (status='processing')
  ↓ 返回 video_id
```

### 步骤 2: 异步处理
```
后台任务 (video_service.analyze_video)
  ├─ 并行处理 1: 情感分析 (AWS Rekognition)
  └─ 并行处理 2: 语音转文字 (Azure)
       ├─ FFmpeg 提取音频
       ├─ Azure Speech API 转录
       ├─ 提取说话人信息
       └─ 计算信心度
```

### 步骤 3: 保存结果
```
数据库更新
  ├─ transcription_json (完整转录数据)
  ├─ speaker_segments (说话人分段数据)
  ├─ speaker_count (说话人总数)
  ├─ emotion_labels (情感标签)
  └─ status='completed'
```

### 步骤 4: 返回结果
```
GET /api/videos/analyze/{id}
  ↓ 从数据库读取记录
  ↓ 解析 JSON 字段
  ↓ 格式化响应
  ↓ 返回前端显示
```

---

## 🧪 验证和测试

### 快速验证脚本

```bash
# 运行完整验证
python verify_transcription.py

# 运行 API 端点测试
python test_api_endpoints.py

# 运行音频提取测试
python test_audio_extraction.py
```

### 测试预期输出

```
✅ 音频提取成功
   输入: check-in-test.mp4 (2.2 MB)
   输出: temp_audio.wav (250.1 KB)
   时间: ~1-2 秒

✅ 语音转文字成功
   文本长度: 67 字符
   信心度: 85%
   语言: 繁體中文 (zh-TW)

✅ 说话人识别成功
   说话人数: 1
   分段数: 1
   时间范围: 0.00s - 10.5s
```

---

## 🚨 常见问题

### Q: 转录失败？
**A:** 检查:
1. Azure 凭证是否正确 (AZURE_SPEECH_API_KEY, AZURE_SPEECH_ENDPOINT)
2. 网络连接是否正常
3. 音频格式是否正确 (16kHz, 16-bit, mono WAV)
4. 日志文件查看详细错误

### Q: 说话人数量为 0？
**A:** 原因可能:
1. 音频质量太差或无声
2. 音量太小 (调整 threshold)
3. 方言或口音无法识别 (增加 zh-TW 数据)

### Q: API 返回 HTTP 500？
**A:** 检查:
1. 数据库字段是否存在 (transcription_json, speaker_segments, speaker_count)
2. JSON 解析是否正确
3. 运行迁移脚本: `python migrate_db.py`

---

## 📊 性能指标

| 指标 | 值 | 备注 |
|-----|----|----|
| 音频提取时间 | 1-2 秒 | 取决于视频大小 |
| 转录时间 | 2-5 秒 | 取决于音频长度 |
| 情感分析时间 | 1-3 秒 | 并行处理 |
| 总处理时间 | 3-8 秒 | 并行，主要由转录决定 |
| 支持最长音频 | 60 分钟 | Azure 限制 |
| 支持最长视频 | 5 GB | 系统依赖 |

---

## 🔗 相关资源

- **Azure Speech-to-Text 文档**: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/
- **FFmpeg 文档**: https://ffmpeg.org/documentation.html
- **FastAPI 文档**: https://fastapi.tiangolo.com/
- **SQLAlchemy 文档**: https://docs.sqlalchemy.org/

---

## ✨ 项目状态

✅ **代码清理**: AWS Transcribe 已删除
✅ **Azure 集成**: 完全集成且验证通过
✅ **数据库**: 已迁移新增字段
✅ **API 文档**: http://127.0.0.1:8000/docs
✅ **应用状态**: 运行中，生产就绪

