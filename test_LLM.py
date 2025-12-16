import requests
import json
import urllib.parse

BASE_URL = "https://llm.89.com.tw"
APP_NAME = "agents"
USER_ID = "wilsonsu"  # Replace with your actual user ID

def test_adk():
    print(f"Testing connection to {BASE_URL}...")

    # 1. Create Session
    session_url = f"{BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions"
    print(f"\n[1] Creating Session: POST {session_url}")
    
    try:
        resp = requests.post(session_url, json={})
        resp.raise_for_status()
        session_data = resp.json()
        session_id = session_data.get("id")
        print(f"Success! Session ID: {session_id}")
    except Exception as e:
        print(f"Failed to create session: {e}")
        return

    # 2. Prepare Run Payload
    run_url = f"{BASE_URL}/run"
    payload = {
        "appName": APP_NAME,
        "userId": USER_ID,
        "sessionId": session_id,
        "newMessage": {
            "role": "user",
            "parts": [{"text": "你好，請幫我查詢台北的天氣"}]
        }
    }

    # 3. Generate and Print GET Mode URLs
    print(f"\n[2] Generating GET Mode URLs (for logging/testing):")
    
    # Format A: Flattened parameters (Standard query string style)
    # Note: Nested objects like newMessage need to be JSON dumped
    params_flat = {
        "appName": APP_NAME,
        "userId": USER_ID,
        "sessionId": session_id,
        "newMessage": json.dumps(payload["newMessage"])
    }
    url_flat = f"{run_url}?{urllib.parse.urlencode(params_flat)}"
    print(f"Format A (Standard Params): {url_flat}")

    # Format B: Single 'message' parameter (Proxy style from README)
    params_proxy = {
        "Content-Type": "application/json",
        "message": json.dumps(payload)
    }
    url_proxy = f"{run_url}?{urllib.parse.urlencode(params_proxy)}"
    print(f"Format B (Proxy/Message Param): {url_proxy}")

    # 4. Execute Run (Using POST as per standard ADK)
    print(f"\n[3] Executing Run: POST {run_url}")
    try:
        resp = requests.post(run_url, json=payload)
        resp.raise_for_status()
        events = resp.json()
        print(f"Success! Received {len(events)} events.")
        for event in events:
            # Try to extract text content
            try:
                # Adjust based on actual event structure
                if 'parts' in event: # Direct content
                     print(f"Response: {event['parts'][0]['text']}")
                elif 'actions' in event and 'new_message' in event['actions']: # Event object
                     print(f"Response: {event['actions']['new_message']['parts'][0]['text']}")
                else:
                     print(f"Event: {json.dumps(event, ensure_ascii=False)[:100]}...")
            except:
                print(f"Event: {json.dumps(event, ensure_ascii=False)[:100]}...")

    except Exception as e:
        print(f"Failed to run agent: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response Text: {e.response.text}")

if __name__ == "__main__":
    test_adk()
