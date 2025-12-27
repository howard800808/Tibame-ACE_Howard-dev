#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試音頻提取和 Azure 語音轉文字
診斷無法提取音軌或轉錄失敗的問題
"""

import os
import sys
import tempfile
from pathlib import Path

# 檢查 FFmpeg
print("=" * 60)
print("🔍 診斷音頻提取和 Azure 語音轉文字")
print("=" * 60)

print("\n1️⃣ 檢查 FFmpeg 安裝...")
try:
    import subprocess
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
    if result.returncode == 0:
        version_line = result.stdout.decode('utf-8', errors='ignore').split('\n')[0]
        print(f"   ✅ FFmpeg 已安裝: {version_line}")
    else:
        print(f"   ❌ FFmpeg 返回錯誤碼: {result.returncode}")
except FileNotFoundError:
    print("   ❌ FFmpeg 未找到 - 請安裝 FFmpeg")
    print("      Windows: https://ffmpeg.org/download.html")
    print("      macOS: brew install ffmpeg")
    print("      Linux: sudo apt-get install ffmpeg")
    sys.exit(1)
except Exception as e:
    print(f"   ❌ 檢查失敗: {str(e)}")
    sys.exit(1)

# 檢查 Azure SDK
print("\n2️⃣ 檢查 Azure Cognitive Services 語音 SDK...")
try:
    import azure.cognitiveservices.speech as speechsdk
    print(f"   ✅ Azure Speech SDK 已安裝")
except ImportError:
    print(f"   ❌ Azure Speech SDK 未安裝")
    print("      安裝: pip install azure-cognitiveservices-speech")
    sys.exit(1)

# 檢查 ffmpeg-python
print("\n3️⃣ 檢查 ffmpeg-python...")
try:
    import ffmpeg
    print(f"   ✅ ffmpeg-python 已安裝")
except ImportError:
    print(f"   ⚠️  ffmpeg-python 未安裝 (不必需，有備用方案)")

# 檢查配置
print("\n4️⃣ 檢查 Azure 配置...")
try:
    from app.core.config import settings
    
    api_key = settings.AZURE_SPEECH_API_KEY
    endpoint = settings.AZURE_SPEECH_ENDPOINT
    region = settings.AZURE_SPEECH_REGION
    
    if api_key:
        masked_key = api_key[:10] + "..." + api_key[-10:]
        print(f"   ✅ API Key: {masked_key}")
    else:
        print(f"   ❌ API Key 未設置")
        
    if endpoint:
        print(f"   ✅ Endpoint: {endpoint}")
    else:
        print(f"   ❌ Endpoint 未設置")
        
    if region:
        print(f"   ✅ Region: {region}")
    else:
        print(f"   ❌ Region 未設置")
    
    if not (api_key and endpoint and region):
        print("\n   ⚠️ 請在 .env 中設置以下變數:")
        print("      AZURE_SPEECH_API_KEY=...")
        print("      AZURE_SPEECH_ENDPOINT=...")
        print("      AZURE_SPEECH_REGION=...")
        sys.exit(1)
        
except Exception as e:
    print(f"   ❌ 配置讀取失敗: {str(e)}")
    sys.exit(1)

# 測試 Azure 連接
print("\n5️⃣ 測試 Azure 連接...")
try:
    speech_config = speechsdk.SpeechConfig(
        subscription=settings.AZURE_SPEECH_API_KEY,
        region=settings.AZURE_SPEECH_REGION
    )
    speech_config.speech_recognition_language = "zh-Hant"
    print(f"   ✅ Azure 語音配置成功")
except Exception as e:
    print(f"   ❌ Azure 配置失敗: {str(e)}")
    sys.exit(1)

# 查找測試影片
print("\n6️⃣ 查找測試影片...")
test_video = None
for video_path in [
    "check-in-test.mp4",
    "test_video.mp4",
    "sample.mp4",
]:
    if os.path.exists(video_path):
        test_video = video_path
        print(f"   ✅ 找到: {video_path}")
        break

if not test_video:
    print(f"   ⚠️ 未找到測試影片")
    print(f"      請準備一個測試影片 (MP4 格式)")
    print(f"      或在以下位置放置:")
    print(f"      - check-in-test.mp4")
    print(f"      - test_video.mp4")
    sys.exit(1)

# 測試音頻提取
print(f"\n7️⃣ 測試音頻提取 ({test_video})...")
try:
    from app.services.azure_transcription_service import azure_transcription_service
    
    temp_dir = tempfile.gettempdir()
    temp_audio = os.path.join(temp_dir, "test_audio.wav")
    
    # 清理舊檔案
    if os.path.exists(temp_audio):
        os.remove(temp_audio)
    
    success = azure_transcription_service.extract_audio_from_video(test_video, temp_audio)
    
    if success and os.path.exists(temp_audio):
        audio_size = os.path.getsize(temp_audio)
        print(f"   ✅ 音頻提取成功: {audio_size / 1024:.1f} KB")
        
        # 測試 Azure 轉錄
        print(f"\n8️⃣ 測試 Azure 語音轉文字...")
        result = azure_transcription_service.transcribe_with_diarization(temp_audio, "zh-TW")
        success, text, segments, confidence = result
        
        if success:
            print(f"   ✅ 轉錄成功")
            print(f"      文字長度: {len(text or '')} 字符")
            print(f"      分段數: {len(segments)}")
            print(f"      信心度: {confidence:.0%}")
            if text:
                print(f"      文字預覽: {text[:100]}...")
        else:
            print(f"   ❌ 轉錄失敗")
        
        # 清理
        os.remove(temp_audio)
    else:
        print(f"   ❌ 音頻提取失敗")
        sys.exit(1)
        
except Exception as e:
    print(f"   ❌ 測試失敗: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ 所有檢查完成！系統應該可以正常工作")
print("=" * 60)
