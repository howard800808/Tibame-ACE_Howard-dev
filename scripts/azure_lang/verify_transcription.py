#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
驗證轉錄功能的完整測試
不需要啟動 Web 服務器
"""

import json
from app.services.azure_transcription_service import azure_transcription_service

print("=" * 70)
print("✅ [驗證測試] Azure 轉錄和說話人分段")
print("=" * 70)

# 測試音頻提取和轉錄
video_path = "check-in-test.mp4"

print(f"\n[1] 轉錄影片: {video_path}")
print("-" * 70)

success, text, segments, confidence = azure_transcription_service.transcribe_video(
    video_path,
    language='zh-TW'
)

if not success:
    print("❌ 轉錄失敗")
    exit(1)

print(f"\n[2] 轉錄結果")
print("-" * 70)
print(f"✅ 轉錄成功")
print(f"   文字長度: {len(text)} 字符")
print(f"   信心度: {confidence:.0%}")
print(f"   文字: {text}")

print(f"\n[3] 說話人分段")
print("-" * 70)
print(f"   分段數: {len(segments)}")

for i, seg in enumerate(segments, 1):
    speaker = seg.get('speaker', 'Unknown')
    content = seg.get('content', '')
    start_time = seg.get('start_time', 0)
    end_time = seg.get('end_time', 0)
    seg_confidence = seg.get('confidence', 0)
    
    print(f"\n   [{i}] {speaker}")
    print(f"       時間: {start_time:.2f}s - {end_time:.2f}s")
    print(f"       信心度: {seg_confidence:.0%}")
    print(f"       內容: {content[:80]}..." if len(content) > 80 else f"       內容: {content}")

# 構建與資料庫相同的數據結構
print(f"\n[4] 資料庫存儲格式")
print("-" * 70)

speaker_data = {
    'speaker_count': len(set(seg.get('speaker', 'Unknown') for seg in segments)),
    'segments': segments,
    'full_text': text
}

print(f"   speaker_count: {speaker_data['speaker_count']}")
print(f"   segments: {json.dumps(segments, ensure_ascii=False, indent=6)}")
print(f"   full_text: {speaker_data['full_text'][:100]}...")

print("\n" + "=" * 70)
print("✅ 所有驗證完成！")
print("=" * 70)
print("\n📌 摘要:")
print(f"   ✓ 音頻提取成功")
print(f"   ✓ Azure 語音轉文字成功")
print(f"   ✓ 轉錄了 {len(text)} 字符的中文文本")
print(f"   ✓ 信心度 {confidence:.0%}")
print(f"   ✓ 說話人數量: {speaker_data['speaker_count']}")
