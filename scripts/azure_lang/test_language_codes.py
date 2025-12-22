#!/usr/bin/env python3
"""測試 Azure 支援的語言代碼"""

import azure.cognitiveservices.speech as speechsdk
from app.core.config import settings

# 測試不同的語言代碼
test_languages = [
    "zh-TW",          # 台灣
    "zh-HK",          # 香港  
    "zh-CN",          # 中國
    "zh-SG",          # 新加坡
    "yue-CN",         # 粵語
    "wuu-CN",         # 吳語
]

speech_config = speechsdk.SpeechConfig(
    subscription=settings.AZURE_SPEECH_API_KEY,
    region=settings.AZURE_SPEECH_REGION
)

print("=" * 60)
print("🔤 Azure Speech-to-Text 支援的語言代碼")
print("=" * 60)

for lang in test_languages:
    print(f"\n測試: {lang}")
    try:
        speech_config.speech_recognition_language = lang
        print(f"  ✅ {lang} 可用")
    except Exception as e:
        print(f"  ❌ {lang} 錯誤: {str(e)[:50]}")

print("\n" + "=" * 60)
print("💡 推薦使用: zh-TW (繁體中文-台灣)")
print("=" * 60)
