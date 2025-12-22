#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""API 測試腳本"""

import requests
import json
import sys
from pathlib import Path

# 設定編碼
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000"

print("\n" + "=" * 70)
print("[TEST] API 功能測試")
print("=" * 70)

# 1. 測試健康檢查
print("\n[1] 測試健康檢查端點...")
try:
    response = requests.get(f"{BASE_URL}/api/health", timeout=5)
    print(f"   [OK] 狀態碼: {response.status_code}")
    print(f"   [DATA] 回應: {response.json()}")
except Exception as e:
    print(f"   [ERROR] {e}")

# 2. 測試登入 (註冊新使用者)
print("\n[2] 測試使用者註冊...")
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "test123456",
            "full_name": "Test User"
        },
        timeout=5
    )
    print(f"   [OK] 狀態碼: {response.status_code}")
    if response.status_code in [200, 201]:
        print(f"   [OK] 使用者已建立")
    else:
        print(f"   [WARN] 回應: {response.text[:200]}")
except Exception as e:
    print(f"   [ERROR] {e}")

# 3. 測試登入 (JSON 格式)
print("\n[3] 測試使用者登入 (JSON)...")
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login/json",
        json={
            "username": "testuser",
            "password": "test123456"
        },
        timeout=5
    )
    print(f"   [OK] 狀態碼: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"   [OK] Token 獲得成功")
        print(f"   [TOKEN] 前 50 字: {token[:50]}...")
    else:
        print(f"   [WARN] 回應: {response.text[:200]}")
except Exception as e:
    print(f"   [ERROR] {e}")

# 4. 測試獲取當前使用者 (需要 Token)
print("\n[4] 測試獲取當前使用者資訊...")
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login/json",
        json={
            "username": "testuser",
            "password": "test123456"
        },
        timeout=5
    )
    if response.status_code == 200:
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        user_response = requests.get(
            f"{BASE_URL}/api/users/me",
            headers=headers,
            timeout=5
        )
        print(f"   [OK] 狀態碼: {user_response.status_code}")
        if user_response.status_code == 200:
            user = user_response.json()
            print(f"   [USER] 名稱: {user.get('username')}")
            print(f"   [EMAIL] {user.get('email')}")
            print(f"   [ROLE] {user.get('role')}")
        else:
            print(f"   [WARN] 回應: {user_response.text[:200]}")
except Exception as e:
    print(f"   [ERROR] {e}")

# 5. 測試情緒辨識路由是否已註冊
print("\n[5] 測試情緒辨識 API 是否可訪問...")
try:
    # 先取得 Token
    response = requests.post(
        f"{BASE_URL}/api/auth/login/json",
        json={
            "username": "testuser",
            "password": "test123456"
        },
        timeout=5
    )
    if response.status_code == 200:
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # 測試取得情緒分析歷史
        emotion_response = requests.get(
            f"{BASE_URL}/api/emotions/history",
            headers=headers,
            timeout=5
        )
        print(f"   [OK] 狀態碼: {emotion_response.status_code}")
        if emotion_response.status_code == 200:
            data = emotion_response.json()
            print(f"   [OK] 情緒辨識 API 可訪問")
            print(f"   [STAT] 總分析次數: {data.get('total_count', 0)}")
            print(f"   [STAT] 情緒統計: {data.get('emotions_summary', {})}")
        else:
            print(f"   [WARN] 回應: {emotion_response.text[:200]}")
except Exception as e:
    print(f"   [ERROR] {e}")

# 6. 測試 Swagger 文檔
print("\n[6] 測試 Swagger API 文檔...")
try:
    response = requests.get(f"{BASE_URL}/docs", timeout=5)
    print(f"   [OK] 狀態碼: {response.status_code}")
    if response.status_code == 200:
        print(f"   [OK] Swagger 文檔可訪問")
        print(f"   [URL] http://localhost:8000/docs")
    else:
        print(f"   [WARN] 文檔不可用")
except Exception as e:
    print(f"   [ERROR] {e}")

print("\n" + "=" * 70)
print("[OK] API 測試完成！")
print("=" * 70)
print("\n[INFO] 可用的 API 端點:")
print("   - POST   /api/auth/register         - 使用者註冊")
print("   - POST   /api/auth/login/json       - 使用者登入")
print("   - GET    /api/users/me              - 取得當前使用者")
print("   - GET    /api/health                - 健康檢查")
print("   - POST   /api/emotions/analyze      - 分析情緒（上傳影像）")
print("   - GET    /api/emotions/history      - 取得分析歷史")
print("   - GET    /api/emotions/statistics   - 取得統計資訊")
print("\n[DOCS] Swagger: http://localhost:8000/docs")
print("[DOCS] ReDoc: http://localhost:8000/redoc")
print("\n")
