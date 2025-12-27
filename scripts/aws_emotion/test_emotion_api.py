import requests
import os
import sys
import json

# 設定基礎 URL
# BASE_URL = "https://ace.89.com.tw"
BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
ANALYZE_URL = f"{BASE_URL}/api/emotions/analyze-image-emotion"

# 測試帳號
USERNAME = "admin"
PASSWORD = "admin123"

# 測試圖片路徑
IMAGE_PATH = os.path.join(os.path.dirname(__file__), "test_face.jpg")

def get_access_token():
    """獲取 Access Token"""
    print(f"正在登入... ({USERNAME})")
    try:
        response = requests.post(
            LOGIN_URL,
            data={"username": USERNAME, "password": PASSWORD},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            print("登入成功!")
            return token_data["access_token"]
        else:
            print(f"登入失敗: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"連線錯誤: {str(e)}")
        return None

def test_emotion_analysis(token):
    """測試情緒分析 API"""
    if not os.path.exists(IMAGE_PATH):
        print(f"錯誤: 找不到測試圖片 '{IMAGE_PATH}'")
        print("請準備一張包含人臉的圖片，命名為 'test_face.jpg' 並放在此腳本同一目錄下。")
        return

    print(f"\n正在分析圖片: {IMAGE_PATH}")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        with open(IMAGE_PATH, "rb") as f:
            files = {"file": ("test_face.jpg", f, "image/jpeg")}
            response = requests.post(ANALYZE_URL, headers=headers, files=files)
            
        if response.status_code == 201:
            result = response.json()
            print("\n=== 分析成功 ===")
            print(f"主要情緒: {result.get('dominant_emotion')} (信心度: {result.get('dominant_emotion_confidence'):.2f}%)")
            print(f"偵測到人臉數: {result.get('face_count')}")
            
            print("\n情緒分佈:")
            emotions = result.get('emotions_breakdown', {})
            for emotion, confidence in emotions.items():
                print(f"  - {emotion}: {confidence:.2f}%")
                
            print("\n完整回應已儲存至 'analysis_result.json'")
            with open("analysis_result.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        else:
            print(f"\n分析失敗: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"發生錯誤: {str(e)}")

if __name__ == "__main__":
    print("=== AWS Rekognition 情緒分析測試 ===")
    
    # 1. 檢查伺服器是否運行
    try:
        requests.get(f"{BASE_URL}/docs", timeout=2)
    except requests.exceptions.ConnectionError:
        print(f"錯誤: 無法連線到伺服器 ({BASE_URL})")
        print("請確保後端伺服器正在運行 (python run.py)")
        sys.exit(1)

    # 2. 登入
    token = get_access_token()
    
    # 3. 執行測試
    if token:
        test_emotion_analysis(token)
