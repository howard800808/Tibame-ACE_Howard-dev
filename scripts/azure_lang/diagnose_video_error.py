#!/usr/bin/env python3
"""
测试视频分析 API 的脚本
用于诊断 HTTP 500 错误
"""

import requests
import json
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

def test_video_upload():
    """测试视频上传和分析启动"""
    
    print("="*60)
    print("🔍 诊断: 视频分析 API 错误")
    print("="*60)
    
    # 第 1 步: 登录
    print("\n1️⃣  正在登录...")
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login/json",
        json={"username": "demo", "password": "demo123"}
    )
    
    if login_response.status_code != 200:
        print(f"❌ 登录失败: {login_response.status_code}")
        print(f"   响应: {login_response.text}")
        return
    
    token = login_response.json().get("access_token")
    print(f"✅ 登录成功，获得 Token")
    
    # 第 2 步: 创建一个最小的测试视频文件
    print("\n2️⃣  创建测试视频文件...")
    
    # 创建一个最小的 MP4 文件（只是头部，不是真实视频）
    # 这是一个有效的 MP4 文件头
    test_video_data = b'\x00\x00\x00\x20ftypisom\x00\x00\x00\x00isomiso2mp41'
    test_video_data += b'\x00' * 1000  # 添加一些填充
    
    print(f"✅ 测试视频文件大小: {len(test_video_data)} 字节")
    
    # 第 3 步: 尝试上传视频
    print("\n3️⃣  尝试上传视频...")
    
    files = {
        'file': ('test_video.mp4', test_video_data, 'video/mp4')
    }
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    upload_response = requests.post(
        f"{BASE_URL}/api/videos/analyze",
        files=files,
        headers=headers
    )
    
    print(f"📡 响应状态码: {upload_response.status_code}")
    
    if upload_response.status_code == 202:
        print("✅ 上传成功 (202 Accepted)")
        result = upload_response.json()
        print(f"   分析 ID: {result.get('analysis_id')}")
        print(f"   消息: {result.get('message')}")
        print(f"   状态: {result.get('status')}")
    else:
        print(f"❌ 上传失败 (状态码: {upload_response.status_code})")
        print(f"\n📋 响应内容:")
        print(upload_response.text[:500])
        
        # 尝试解析 JSON 响应
        try:
            error_data = upload_response.json()
            print(f"\n📊 错误详情:")
            print(json.dumps(error_data, indent=2, ensure_ascii=False))
        except:
            pass

if __name__ == "__main__":
    test_video_upload()
