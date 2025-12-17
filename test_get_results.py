#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试显示分析结果 (GET /api/videos/analyze/{id})
验证 HTTP 500 错误是否已修复
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

print("=" * 70)
print("[测试] 获取分析结果")
print("=" * 70)

# 第 1 步: 登入
print("\n[1] 登入...")
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"username": "demo", "password": "demo123"}
)

if login_response.status_code != 200:
    print(f"❌ 登入失败: {login_response.text}")
    sys.exit(1)

token = login_response.json().get("access_token")
print(f"✅ 登入成功")

headers = {"Authorization": f"Bearer {token}"}

# 第 2 步: 上传影片
print("\n[2] 上传影片...")
video_path = "check-in-test.mp4"

try:
    with open(video_path, 'rb') as f:
        files = {'file': (video_path, f, 'video/mp4')}
        upload_response = requests.post(
            f"{BASE_URL}/api/videos/analyze",
            files=files,
            headers=headers,
            timeout=5
        )
except FileNotFoundError:
    print(f"❌ 找不到影片: {video_path}")
    sys.exit(1)

if upload_response.status_code != 202:
    print(f"❌ 上传失败: {upload_response.status_code}")
    sys.exit(1)

analysis_id = upload_response.json().get("id")
print(f"✅ 上传成功，ID: {analysis_id}")

# 第 3 步: 等待分析完成
print("\n[3] 等待分析完成...")
import time
max_wait = 120
start_time = time.time()

while time.time() - start_time < max_wait:
    progress_response = requests.get(
        f"{BASE_URL}/api/videos/analyze/{analysis_id}/progress",
        headers=headers,
        timeout=5
    )
    
    if progress_response.status_code != 200:
        print(f"❌ 查询失败: {progress_response.status_code}")
        break
    
    data = progress_response.json()
    status = data.get("status")
    progress = data.get("progress", 0)
    
    print(f"   进度: {progress:.0f}% [状态: {status}]", end='\r')
    
    if status in ["success", "failed"]:
        print(f"   进度: {progress:.0f}% [状态: {status}]     ")
        break
    
    time.sleep(2)

# 第 4 步: 获取详细结果 (测试 HTTP 500)
print("\n[4] 获取详细结果...")
result_response = requests.get(
    f"{BASE_URL}/api/videos/analyze/{analysis_id}",
    headers=headers,
    timeout=5
)

print(f"   HTTP 状态码: {result_response.status_code}")

if result_response.status_code == 500:
    print(f"❌ HTTP 500 错误")
    print(f"   响应: {result_response.text[:200]}")
    sys.exit(1)
elif result_response.status_code != 200:
    print(f"❌ 请求失败: {result_response.status_code}")
    print(f"   响应: {result_response.text[:200]}")
    sys.exit(1)

result = result_response.json()

# 显示结果摘要
print("\n" + "=" * 70)
print("[✅ 结果成功显示]")
print("=" * 70)

print(f"\n📊 分析信息:")
print(f"   ID: {result.get('id')}")
print(f"   状态: {result.get('status')}")
print(f"   进度: {result.get('progress'):.0f}%")

print(f"\n🎤 转录结果:")
text = result.get('transcription_text', '')
confidence = result.get('transcription_confidence', 0)
speaker_count = result.get('speaker_count', 0)

if text:
    print(f"   文字: {text[:80]}...")
    print(f"   信心度: {confidence:.0%}")
else:
    print(f"   ⚠️ 无转录文字")

print(f"   说话人数: {speaker_count}")

print(f"\n😊 情绪分析:")
print(f"   主要情绪: {result.get('overall_dominant_emotion')}")
print(f"   信心度: {result.get('overall_confidence'):.0%}")

print("\n" + "=" * 70)
print("✅ 测试完成 - 显示结果功能正常!")
print("=" * 70)
