#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的 HTTP API 测试
测试显示分析结果是否能成功返回数据而不是 HTTP 500
"""

import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

print("=" * 70)
print("[HTTP API 测试] 获取分析结果")
print("=" * 70)

try:
    # 第 1 步: 登入
    print("\n[1] 登入...")
    login_data = {"username": "demo", "password": "demo123"}
    
    try:
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login/json",
            json=login_data,
            timeout=10
        )
    except:
        # 尝试备用端点
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            timeout=10
        )
    
    if login_response.status_code != 200:
        print(f"❌ 登入失败: {login_response.status_code}")
        print(f"   响应: {login_response.text[:200]}")
        sys.exit(1)
    
    token = login_response.json().get("access_token")
    print(f"✅ 登入成功")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 第 2 步: 使用已存在的分析结果 (ID=10)
    print("\n[2] 获取已存在的分析结果 (ID=10)...")
    
    result_response = requests.get(
        f"{BASE_URL}/api/videos/analyze/10",
        headers=headers,
        timeout=10
    )
    
    print(f"   HTTP 状态码: {result_response.status_code}")
    
    if result_response.status_code == 500:
        print(f"❌ HTTP 500 错误")
        print(f"   响应: {result_response.text[:300]}")
        sys.exit(1)
    
    if result_response.status_code != 200:
        print(f"❌ 请求失败: {result_response.status_code}")
        print(f"   响应: {result_response.text[:200]}")
        sys.exit(1)
    
    result = result_response.json()
    
    # 显示成功的结果
    print("\n" + "=" * 70)
    print("[✅ 成功获取分析结果！]")
    print("=" * 70)
    
    print(f"\n📊 基本信息:")
    print(f"   分析 ID: {result.get('id')}")
    print(f"   状态: {result.get('status')}")
    print(f"   进度: {result.get('progress'):.0f}%")
    print(f"   创建时间: {result.get('created_at')}")
    
    print(f"\n🎤 转录结果:")
    text = result.get('transcription_text', '')
    confidence = result.get('transcription_confidence', 0)
    speaker_count = result.get('speaker_count', 0)
    
    if text:
        preview = text[:80] + "..." if len(text) > 80 else text
        print(f"   文字: {preview}")
        print(f"   信心度: {confidence:.0%}")
    else:
        print(f"   ⚠️ 无转录文字")
    
    print(f"   说话人数: {speaker_count}")
    
    # 显示转录 JSON
    transcription_json = result.get('transcription_json')
    if transcription_json:
        print(f"\n   转录分段数: {len(transcription_json)}")
        for i, seg in enumerate(transcription_json[:2], 1):  # 显示前 2 个
            print(f"      [{i}] {seg.get('speaker', 'Unknown')}: {seg.get('content', '')[:40]}...")
    
    print(f"\n😊 情绪分析:")
    print(f"   主要情绪: {result.get('overall_dominant_emotion')}")
    print(f"   信心度: {result.get('overall_confidence'):.0%}")
    print(f"   检测人数: {result.get('detected_people_count')}")
    
    print("\n" + "=" * 70)
    print("✅ 测试完成 - API 工作正常!")
    print("=" * 70)
    
except ConnectionError as e:
    print(f"❌ 无法连接到服务器: {str(e)}")
    print(f"   请确保服务器运行在 http://127.0.0.1:8000")
    sys.exit(1)
except Exception as e:
    print(f"❌ 出错: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
