import os
import sys
from fastapi.testclient import TestClient

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from run import app

client = TestClient(app)

# Configuration
USERNAME = "admin"
PASSWORD = "admin123"
VIDEO_FILE_PATH = os.path.join(os.path.dirname(__file__), "azure_lang", "test_video.mp4")
IMAGE_FILE_PATH = os.path.join(os.path.dirname(__file__), "aws_emotion", "test_face.jpg")

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def print_pass(message):
    print(f"{GREEN}[PASS] {message}{RESET}")

def print_fail(message, error=None):
    print(f"{RED}[FAIL] {message}{RESET}")
    if error:
        print(f"{RED}Error: {error}{RESET}")

def test_health():
    print("\n--- Testing System Health ---")
    try:
        response = client.get("/api/health")
        if response.status_code == 200:
            print_pass("Health check successful")
            return True
        else:
            print_fail(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_fail("Health check exception", e)
        return False

def test_login():
    print("\n--- Testing Authentication ---")
    try:
        response = client.post(
            "/api/auth/login",
            data={"username": USERNAME, "password": PASSWORD}
        )
        if response.status_code == 200:
            token = response.json().get("access_token")
            print_pass("Login successful")
            return token
        else:
            print_fail(f"Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print_fail("Login exception", e)
        return None

def test_user_routes(token):
    print("\n--- Testing User Routes ---")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = client.get("/api/users/me", headers=headers)
        if response.status_code == 200:
            print_pass("Get Current User successful")
        else:
            print_fail(f"Get Current User failed: {response.status_code}")
    except Exception as e:
        print_fail("Get Current User exception", e)

    try:
        response = client.get("/api/users/", headers=headers)
        if response.status_code == 200:
            print_pass(f"Get Users List successful (Count: {len(response.json())})")
        else:
            print_fail(f"Get Users List failed: {response.status_code}")
    except Exception as e:
        print_fail("Get Users List exception", e)

def test_task_routes(token):
    print("\n--- Testing Task Routes ---")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = client.get("/api/tasks/", headers=headers)
        if response.status_code == 200:
            print_pass(f"Get All Tasks successful (Count: {len(response.json())})")
        else:
            print_fail(f"Get All Tasks failed: {response.status_code}")
    except Exception as e:
        print_fail("Get All Tasks exception", e)

    try:
        response = client.get("/api/tasks/emergency", headers=headers)
        if response.status_code == 200:
            print_pass(f"Get Emergency Tasks successful (Count: {len(response.json())})")
        else:
            print_fail(f"Get Emergency Tasks failed: {response.status_code}")
    except Exception as e:
        print_fail("Get Emergency Tasks exception", e)

def test_emotion_routes(token):
    print("\n--- Testing Emotion Routes ---")
    headers = {"Authorization": f"Bearer {token}"}
    
    if os.path.exists(IMAGE_FILE_PATH):
        try:
            with open(IMAGE_FILE_PATH, "rb") as f:
                files = {"file": ("test_face.jpg", f, "image/jpeg")}
                response = client.post(
                    "/api/emotions/analyze-image-emotion",
                    headers=headers,
                    files=files
                )
            
            if response.status_code == 201:
                print_pass("Analyze Image Emotion successful")
                data = response.json()
                print(f"   Dominant Emotion: {data.get('dominant_emotion')}")
            else:
                print_fail(f"Analyze Image Emotion failed: {response.status_code} - {response.text}")
        except Exception as e:
            print_fail("Analyze Image Emotion exception", e)
    else:
        print_fail(f"Image file not found at {IMAGE_FILE_PATH}")

    try:
        response = client.get("/api/emotions/history", headers=headers)
        if response.status_code == 200:
            print_pass("Get Emotion History successful")
        else:
            print_fail(f"Get Emotion History failed: {response.status_code}")
    except Exception as e:
        print_fail("Get Emotion History exception", e)

def test_video_routes(token):
    print("\n--- Testing Video Routes ---")
    headers = {"Authorization": f"Bearer {token}"}
    
    if os.path.exists(VIDEO_FILE_PATH):
        try:
            with open(VIDEO_FILE_PATH, "rb") as f:
                files = {"file": ("test_video.mp4", f, "video/mp4")}
                print("   Uploading video for analysis...")
                response = client.post(
                    "/api/videos/analyze-video-emotion",
                    headers=headers,
                    files=files
                )
            
            if response.status_code == 202:
                print_pass("Analyze Video Emotion accepted (Async)")
                data = response.json()
                print(f"   Analysis ID: {data.get('analysis_id')}")
            else:
                print_fail(f"Analyze Video Emotion failed: {response.status_code} - {response.text}")
        except Exception as e:
            print_fail("Analyze Video Emotion exception", e)
    else:
        print_fail(f"Video file not found at {VIDEO_FILE_PATH}")

def test_mbti_routes(token):
    print("\n--- Testing MBTI Routes ---")
    
    if os.path.exists(VIDEO_FILE_PATH):
        try:
            with open(VIDEO_FILE_PATH, "rb") as f:
                files = {"file": ("test_video.mp4", f, "video/mp4")}
                response = client.post(
                    "/api/mbti/test-upload",
                    files=files
                )
            
            if response.status_code == 200:
                print_pass("MBTI Test Upload successful")
            else:
                print_fail(f"MBTI Test Upload failed: {response.status_code}")
        except Exception as e:
            print_fail("MBTI Test Upload exception", e)
    else:
        print_fail(f"Video file not found at {VIDEO_FILE_PATH}")

def test_adk_routes(token):
    print("\n--- Testing ADK Routes ---")
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "message": "Hello, are you there?",
        "user_id": "default_user"
    }
    
    try:
        response = client.post(
            "/api/adk/chat",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            print_pass("ADK Chat successful")
            print(f"   Response: {response.json().get('response')}")
        else:
            print_fail(f"ADK Chat failed: {response.status_code} - {response.text}")
    except Exception as e:
        print_fail("ADK Chat exception", e)

def main():
    print("=== Starting Comprehensive API Test (Internal) ===")
    
    if not test_health():
        print("System is not healthy. Aborting.")
        return

    token = test_login()
    if not token:
        print("Authentication failed. Aborting.")
        return

    test_user_routes(token)
    test_task_routes(token)
    test_emotion_routes(token)
    test_video_routes(token)
    test_mbti_routes(token)
    test_adk_routes(token)
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
