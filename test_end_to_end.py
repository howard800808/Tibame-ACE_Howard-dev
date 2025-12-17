#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的端到端測試：上傳影片 → 轉錄 → 查看結果
"""

import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

print("=" * 70)
print("[端到端測試] 影片上傳和轉錄")
print("=" * 70)

# 第 1 步: 登入
print("\n[1/4] 登入...")
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"username": "demo", "password": "demo123"}
)

if login_response.status_code != 200:
    print(f"❌ 登入失敗: {login_response.text}")
    sys.exit(1)

token = login_response.json().get("access_token")
print(f"✅ 登入成功，Token: {token[:20]}...")

headers = {"Authorization": f"Bearer {token}"}

# 第 2 步: 上傳影片
print("\n[2/4] 上傳影片...")
video_path = "check-in-test.mp4"

try:
    with open(video_path, 'rb') as f:
        files = {'file': (video_path, f, 'video/mp4')}
        upload_response = requests.post(
            f"{BASE_URL}/api/videos/analyze",
            files=files,
            headers=headers
        )
except FileNotFoundError:
    print(f"❌ 找不到影片檔案: {video_path}")
    sys.exit(1)

if upload_response.status_code != 202:
    print(f"❌ 上傳失敗 (狀態碼 {upload_response.status_code})")
    print(f"   響應: {upload_response.text}")
    sys.exit(1)

analysis_id = upload_response.json().get("id")
print(f"✅ 上傳成功，分析 ID: {analysis_id}")

# 第 3 步: 等待分析完成
print("\n[3/4] 等待分析完成...")
max_wait = 60  # 最多等待 60 秒
start_time = time.time()

while time.time() - start_time < max_wait:
    progress_response = requests.get(
        f"{BASE_URL}/api/videos/analyze/{analysis_id}/progress",
        headers=headers
    )
    
    if progress_response.status_code != 200:
        print(f"❌ 查詢進度失敗: {progress_response.text}")
        break
    
    data = progress_response.json()
    status = data.get("status")
    progress = data.get("progress", 0)
    
    print(f"   進度: {progress:.0f}% [狀態: {status}]", end='\r')
    
    if status == "success":
        print(f"   進度: 100% [狀態: success]     ")
        break
    elif status == "failed":
        print(f"   進度: {progress:.0f}% [狀態: failed]")
        error_msg = data.get("error_message", "未知錯誤")
        print(f"❌ 分析失敗: {error_msg}")
        break
    
    time.sleep(2)
else:
    print(f"\n⏱️ 等待超時")

# 第 4 步: 獲取完整結果
print("\n[4/4] 獲取分析結果...")
result_response = requests.get(
    f"{BASE_URL}/api/videos/analyze/{analysis_id}",
    headers=headers
)

if result_response.status_code != 200:
    print(f"❌ 獲取結果失敗: {result_response.text}")
    sys.exit(1)

result = result_response.json()

# 顯示結果
print("\n" + "=" * 70)
print("[分析結果]")
print("=" * 70)

print(f"\n📊 基本信息:")
print(f"   分析狀態: {result.get('status')}")
print(f"   進度: {result.get('progress'):.0f}%")

# 轉錄結果
transcription_text = result.get('transcription_text', '')
transcription_confidence = result.get('transcription_confidence', 0)
speaker_count = result.get('speaker_count', 0)

print(f"\n🎤 語音轉文字:")
print(f"   轉錄信心度: {transcription_confidence:.0%}")
print(f"   偵測到的說話人: {speaker_count}")

if transcription_text:
    print(f"\n📝 轉錄文字:")
    print(f"   {transcription_text[:200]}..." if len(transcription_text) > 200 else f"   {transcription_text}")
else:
    print(f"\n❌ 無轉錄文字")

# 說話人分段
speaker_segments = result.get('speaker_segments')
if speaker_segments:
    try:
        if isinstance(speaker_segments, str):
            segments_data = json.loads(speaker_segments)
        else:
            segments_data = speaker_segments
        
        print(f"\n👥 說話人分段:")
        segments_list = segments_data.get('segments', [])
        print(f"   分段數: {len(segments_list)}")
        
        for i, seg in enumerate(segments_list[:3], 1):  # 顯示前 3 個
            speaker = seg.get('speaker', 'Unknown')
            content = seg.get('content', '')[:60]
            confidence = seg.get('confidence', 0)
            print(f"   [{i}] {speaker} ({confidence:.0%}): {content}...")
    except Exception as e:
        print(f"   ⚠️ 解析分段失敗: {str(e)}")
else:
    print(f"\n⚠️ 沒有說話人分段信息")

# 情緒分析
emotion = result.get('overall_dominant_emotion')
emotion_conf = result.get('overall_confidence')

print(f"\n😊 情緒分析:")
print(f"   主要情緒: {emotion}")
print(f"   信心度: {emotion_conf:.0%}")

print("\n" + "=" * 70)
print("✅ 測試完成！")
print("=" * 70)
