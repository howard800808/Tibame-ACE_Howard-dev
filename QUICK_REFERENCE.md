# ⚡ 快速参考卡片

## 🚀 快速启动

```bash
# 1. 启动应用
cd c:\Users\YuChuan\Desktop\team-project-desk
.\.venv\Scripts\python.exe -m uvicorn run:app --host 127.0.0.1 --port 8000

# 2. 打开浏览器
http://127.0.0.1:8000/login
demo / demo123

# 3. 上传视频进行分析
http://127.0.0.1:8000/video-analysis
```

---

## 📊 关键数据

### Azure 配置
```
API 密钥: 5KTW9kudEOhqlJMVXFJGUjDVZ9qq1FhqLsHIye0NlfeWsKhE05IBJQQJ99BLACYeBjFXJ3w3AAAYACOGslsW
端点: https://eastus.api.cognitive.microsoft.com/
区域: eastus
语言: zh-TW (繁體中文)
```

### 数据库
```
文件: admin.db
类型: SQLite
表: video_analysis (新增字段: transcription_json, speaker_segments, speaker_count)
```

### 应用端口
```
地址: 127.0.0.1
端口: 8000
协议: HTTP
框架: FastAPI
```

---

## 🔑 核心功能

### 1️⃣ 视频上传
```
POST /api/videos/upload
{
  "file": <video.mp4>,
  "description": "视频描述"
}
```

### 2️⃣ 获取分析结果
```
GET /api/videos/analyze/{id}

返回:
{
  "transcription_json": [...],
  "speaker_count": 1,
  "speaker_segments": "[...]",
  "emotion_analysis": {...}
}
```

### 3️⃣ 查询视频列表
```
GET /api/videos/list

返回:
[
  {
    "id": 1,
    "filename": "video.mp4",
    "status": "completed",
    ...
  }
]
```

---

## 📁 关键文件位置

### 服务
```
app/services/azure_transcription_service.py      # Azure 语音转文字 ⭐
app/services/emotion_service.py                  # 情感分析 (AWS)
app/services/video_service.py                    # 视频处理协调
```

### 控制器
```
app/controllers/video_controller.py               # 视频 API
app/controllers/auth_controller.py                # 认证 API
```

### 配置
```
.env                                             # 环境变量
app/core/config.py                               # 应用配置
```

### 数据库
```
admin.db                                         # SQLite 数据库
app/models/video.py                              # 模型定义
```

---

## 🎯 工作流程

```
用户上传视频
    ↓
视频保存 + 数据库记录 (status='processing')
    ↓
并行处理:
  ├─ 情感分析 (AWS Rekognition)
  └─ 语音转文字 (Azure Speech)
        ├─ FFmpeg 音频提取
        ├─ Azure API 转录
        └─ 说话人识别
    ↓
保存结果 (status='completed')
    ↓
前端显示分析结果
```

---

## 🧪 测试脚本

```bash
# 快速验证转录
python verify_transcription.py

# 测试 API 端点
python test_api_endpoints.py

# 测试音频提取
python test_audio_extraction.py

# 完整流程测试
python test_end_to_end.py
```

---

## ⚙️ 常用命令

### 数据库迁移
```bash
python migrate_db.py
```

### 重启应用
```bash
# 停止 Python 进程
Get-Process python | Stop-Process -Force

# 重新启动
.\.venv\Scripts\python.exe -m uvicorn run:app --host 127.0.0.1 --port 8000
```

### 查看日志
```bash
# 应用输出就是日志
# 或检查数据库
sqlite3 admin.db "SELECT * FROM video_analysis;"
```

### 清理临时文件
```bash
# FFmpeg 临时文件位置
C:\Users\YuChuan\AppData\Local\Temp\temp_audio*.wav
```

---

## 📚 文档快速链接

| 文档 | 内容 | 链接 |
|------|------|------|
| Azure 集成 | 架构和 API | [AZURE_INTEGRATION_GUIDE.md](AZURE_INTEGRATION_GUIDE.md) |
| Azure 设置 | 环境配置 | [AZURE_SPEECH_SETUP.md](AZURE_SPEECH_SETUP.md) |
| 集成报告 | 技术细节 | [INTEGRATION_REPORT.md](INTEGRATION_REPORT.md) |
| 清理报告 | 代码清理 | [CLEANUP_REPORT.md](CLEANUP_REPORT.md) |
| 项目状态 | 完整状态 | [PROJECT_STATUS.md](PROJECT_STATUS.md) |

---

## 🐛 常见问题

### Q: 如何测试 Azure 连接？
```bash
python verify_transcription.py
```

### Q: 如何上传测试视频？
访问 http://127.0.0.1:8000/video-analysis 并选择视频文件

### Q: 如何查看 API 文档？
访问 http://127.0.0.1:8000/docs

### Q: 如何查看转录结果？
```bash
# 方式 1: 前端查看 http://127.0.0.1:8000/video-analysis
# 方式 2: API 查询 GET /api/videos/analyze/{id}
# 方式 3: 数据库查询
sqlite3 admin.db "SELECT transcription_json FROM video_analysis WHERE id=1;"
```

### Q: 如何修改语言？
编辑 `app/services/azure_transcription_service.py` 第 30 行:
```python
LANGUAGE_CODE = "zh-TW"  # 改为需要的语言代码
```

---

## ✅ 状态检查

### 应用运行
```bash
# 检查应用是否运行
curl http://127.0.0.1:8000/docs
```

### 数据库连接
```bash
# 检查数据库文件
ls -la admin.db

# 查询表结构
sqlite3 admin.db ".schema video_analysis"
```

### Azure 凭证
```bash
# 检查凭证是否配置
echo $AZURE_SPEECH_API_KEY
```

---

## 📊 系统要求

- Python 3.11+
- FFmpeg 8.0.1+
- SQLite 3.0+
- Azure Cognitive Services 账户
- AWS Rekognition 账户 (可选，用于情感分析)
- 网络连接 (Azure API 调用)

---

## 🎓 学习路径

### 1️⃣ 快速了解
1. 阅读本卡片 (5 分钟)
2. 阅读 [Azure 集成指南](AZURE_INTEGRATION_GUIDE.md) (15 分钟)

### 2️⃣ 深入学习
1. 阅读 [Azure 设置指南](AZURE_SPEECH_SETUP.md) (20 分钟)
2. 阅读源代码 (30 分钟)
3. 运行测试脚本 (10 分钟)

### 3️⃣ 实践应用
1. 上传测试视频 (2 分钟)
2. 查看分析结果 (2 分钟)
3. 修改代码并测试 (变数)

---

## 🚀 一键启动清单

- [ ] 检查 Python 版本: `python --version`
- [ ] 检查虚拟环境: `source .venv/bin/activate` (Linux/Mac) 或 `.\.venv\Scripts\activate` (Windows)
- [ ] 启动应用: `.\.venv\Scripts\python.exe -m uvicorn run:app --host 127.0.0.1 --port 8000`
- [ ] 打开浏览器: `http://127.0.0.1:8000/login`
- [ ] 登录: `demo / demo123`
- [ ] 进入分析页面: `http://127.0.0.1:8000/video-analysis`
- [ ] 上传视频并分析

---

## 📞 支持和帮助

### 查看日志
- 应用日志在终端输出中显示
- 详细日志可在 `verify_transcription.py` 中查看

### 调试
```python
# 启用 DEBUG 模式
# 编辑 .env: DEBUG=True
```

### 获取更多帮助
- 查看 [Azure 集成指南](AZURE_INTEGRATION_GUIDE.md)
- 查看 [PROJECT_STATUS.md](PROJECT_STATUS.md)
- 查看应用日志和错误消息

---

## 🎉 祝贺！

您的项目已完全准备就绪！

✅ AWS Transcribe 代码已删除
✅ Azure Speech-to-Text 已集成
✅ 所有功能已验证
✅ 应用已启动运行

**开始使用吧！** 🚀

