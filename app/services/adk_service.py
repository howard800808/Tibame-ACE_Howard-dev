import requests
import json
import asyncio
from app.core.config import settings
from typing import Dict, Any, List

class AdkService:
    def __init__(self):
        self.base_url = settings.ADK_BASE_URL
        self.app_name = settings.ADK_APP_NAME

    async def create_session(self, user_id: str) -> str:
        """建立 ADK Session"""
        session_url = f"{self.base_url}/apps/{self.app_name}/users/{user_id}/sessions"
        try:
            resp = await asyncio.to_thread(requests.post, session_url, json={})
            resp.raise_for_status()
            session_data = resp.json()
            return session_data.get("id")
        except Exception as e:
            print(f"Failed to create session: {e}")
            raise e

    async def send_message(self, user_id: str, message: str) -> Dict[str, Any]:
        """發送訊息給 ADK Agent"""
        # 1. 取得 Session ID
        # 注意：實際應用中可能需要快取 Session ID，這裡為了簡化每次都建立新的或視需求調整
        try:
            session_id = await self.create_session(user_id)
        except Exception:
            # 如果建立失敗，可能需要處理錯誤，這裡暫時拋出
            raise Exception("無法建立對話 Session")

        # 2. 準備 Payload
        run_url = f"{self.base_url}/run"
        payload = {
            "appName": self.app_name,
            "userId": user_id,
            "sessionId": session_id,
            "newMessage": {
                "role": "user",
                "parts": [{"text": message}]
            }
        }

        print(f"[{self.app_name}] Sending Payload to {run_url}: {json.dumps(payload, ensure_ascii=False, indent=2)}")

        # 3. 執行請求
        try:
            resp = await asyncio.to_thread(requests.post, run_url, json=payload)
            resp.raise_for_status()
            events = resp.json()
            
            print(f"[{self.app_name}] Received Events: {json.dumps(events, ensure_ascii=False, indent=2)}")

            # 4. 解析回應
            final_response = ""
            for event in events:
                try:
                    if 'parts' in event: # 直接內容
                        final_response += event['parts'][0]['text']
                    elif 'content' in event and 'parts' in event['content']: # Gemini 結構
                        final_response += event['content']['parts'][0]['text']
                    elif 'actions' in event and 'new_message' in event['actions']: # 事件物件
                        final_response += event['actions']['new_message']['parts'][0]['text']
                except:
                    continue
            
            print(f"[{self.app_name}] Final Response: {final_response}")

            return {
                "response": final_response,
                "events": events
            }

        except Exception as e:
            print(f"Failed to run agent: {e}")
            raise e

adk_service = AdkService()
