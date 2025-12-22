from fastapi import Request, HTTPException, Header
from typing import Optional
import json

# LINE Bot SDK v3 Imports
from linebot.v3.messaging import (
    TextMessage,
    FlexMessage,
    FlexContainer
)

from app.services.linebot_service import linebot_service, create_report_flow_card

class LineBotController:
    """LINE Bot 控制器 - 處理 Webhook 請求 (v3 SDK)"""
    
    def __init__(self):
        self.user_input_state = {}

    async def handle_webhook(
        self,
        department_code: str,
        request: Request,
        x_line_signature: str = Header(None)
    ):
        """處理 LINE Bot Webhook 請求"""
        
        # 讀取請求內容
        body = await request.body()
        body_str = body.decode('utf-8')
        
        # 驗證部門是否存在
        from app.core.database import SessionLocal
        from app.models.department import Department
        
        db = SessionLocal()
        try:
            department = db.query(Department).filter(Department.code == department_code, Department.is_active == True).first()
            if not department:
                raise HTTPException(status_code=404, detail=f"部門 {department_code} 不存在或未啟用")
        finally:
            db.close()
        
        # 驗證簽名 (使用 Service 封裝的 v3 驗證)
        if not linebot_service.validate_signature(department_code, body_str, x_line_signature):
            raise HTTPException(status_code=400, detail="無效的簽名")
        
        # 處理事件 (手動解析 JSON)
        try:
            events_data = json.loads(body_str)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="無效的 JSON 格式")
        
        for event in events_data.get('events', []):
            await self._process_event(department_code, event)
        
        return {"status": "ok"}
    
    async def _process_event(self, department_code: str, event: dict):
        """處理單個事件"""
        event_type = event.get('type')
        
        if event_type == 'message':
            await self._handle_message_event(department_code, event)
        elif event_type == 'postback':
            await self._handle_postback_event(department_code, event)
        elif event_type == 'follow':
            await self._handle_follow_event(department_code, event)
        elif event_type == 'unfollow':
            await self._handle_unfollow_event(department_code, event)
        # 可以添加其他事件類型處理
    
    async def _handle_message_event(self, department_code: str, event: dict):
        """處理訊息事件"""
        message = event.get('message', {})
        message_type = message.get('type')
        source = event.get('source', {})
        user_id = source.get('userId')
        reply_token = event.get('replyToken')
        
        # [New Logic] Check if user is in input state (Step 2 Report)
        if user_id and user_id in self.user_input_state:
            state = self.user_input_state[user_id]
            task_id = state['task_id']
            step = state['step']
            expected_type = state['type']
            room_info = state['room']
            
            print(f"[Message] 收到用戶輸入 (State: {expected_type})")

            # Validate input type
            if expected_type == 'text' and message_type != 'text':
                await linebot_service.send_reply_message(department_code, reply_token, "格式錯誤，請發送文字訊息")
                return
            if expected_type == 'voice' and message_type not in ['audio']:
                 await linebot_service.send_reply_message(department_code, reply_token, "格式錯誤，請發送語音訊息")
                 return

            # Process Input
            answer_content = ""
            if message_type == 'text':
                answer_content = message.get('text')
            elif message_type == 'audio':
                msg_id = message.get('id')
                answer_content = f"[Voice Message] ID: {msg_id}"
                # TODO: Download audio logic here

            # Record Answer
            try:
                await linebot_service.record_report_answer(task_id, step, answer_content)
            except Exception as e:
                print(f"[Error] 寫入答案失敗: {e}")
            
            # Clear state
            del self.user_input_state[user_id]
            
            # Move to Step 3
            next_step = step + 1
            bubble = create_report_flow_card(
                step=next_step, 
                dept=f"{department_code} 測試", 
                room=room_info, 
                task_id=task_id or "N/A"
            )
            if reply_token:
                await linebot_service.reply_flex(
                    department_code, 
                    reply_token, 
                    alt_text=f"任務回報 ({next_step}/5)", 
                    flex_contents=bubble
                )
            return

        # Normal Text Message Handling
        if message_type == 'text':
            # 取得用戶名稱（需要額外 API 調用，這裡簡單處理，v3 暫時略過 profile 獲取以免複雜化）
            user_name = "User" 
            
            # 處理文字訊息
            message_text = message.get('text')
            message_id = message.get('id')
            
            if message_text and user_id:
                await linebot_service.handle_text_message(
                    department_code=department_code,
                    user_id=user_id,
                    user_name=user_name,
                    message_text=message_text,
                    message_id=message_id,
                    reply_token=reply_token
                )
    
    async def _handle_follow_event(self, department_code: str, event: dict):
        """處理加入好友事件"""
        source = event.get('source', {})
        user_id = source.get('userId')
        reply_token = event.get('replyToken')
        
        if user_id and reply_token:
            from app.core.database import SessionLocal
            from app.models.department import Department
            
            db = SessionLocal()
            try:
                department = db.query(Department).filter(Department.code == department_code).first()
                if department:
                    welcome_message = f"歡迎加入 {department.name} 任務管理系統！\n\n您可以直接傳送訊息建立新任務，我們會盡快處理。"
                    
                    await linebot_service.send_reply_message(
                        department_code,
                        reply_token,
                        welcome_message
                    )
            finally:
                db.close()
    
    async def _handle_unfollow_event(self, department_code: str, event: dict):
        """處理取消好友事件"""
        source = event.get('source', {})
        user_id = source.get('userId')
        
        # 可以在這裡記錄用戶取消追蹤
        print(f"用戶 {user_id} 取消追蹤部門 {department_code}")

    async def _handle_postback_event(self, department_code: str, event: dict):
        """處理 Postback 事件：解析資料流程並做出回應"""
        print(f"\n[Postback] 收到事件，部門: {department_code}")
        
        data = event.get('postback', {}).get('data', '')
        reply_token = event.get('replyToken')

        # 範例格式：action=report&step=2&id=TASK123&ans=yes 或 action=task&op=accept&task_id=TASK123&dept=HK
        parsed = {}
        try:
            for pair in data.split('&'):
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    parsed[k] = v
        except Exception as e:
            print(f"[Postback] [ERROR] 解析 Postback 資料失敗: {str(e)}")
            return

        action = parsed.get('action')
        print(f"[Postback] 動作: {action}，詳細資訊 {parsed}")

        # 處理任務操作 (接受/完成)
        if action == 'task':
            task_id = parsed.get('task_id') or parsed.get('id')
            op = parsed.get('op')  # accept/complete/archive/view_cancel
            dept = parsed.get('dept')
            
            print("[LINEBot 任務]", {
                "department": department_code,
                "task_id": task_id,
                "op": op,
                "dept": dept,
                "raw": data
            })
            
            # 更新資料庫任務狀態（根據 task_id）
            if task_id:
                from app.models.task import TaskStatus
                
                try:
                    # 根據操作決定狀態
                    status_map = {
                        'accept': TaskStatus.IN_PROGRESS,
                        'complete': TaskStatus.COMPLETED,
                        'archive': TaskStatus.COMPLETED,  # 歸檔也是標記為完成
                    }
                    new_status = status_map.get(op)
                    
                    if new_status:
                        # 更新任務狀態
                        updated = await linebot_service.update_task_status(
                            task_id, 
                            new_status, 
                            notes=f"LINEBot {op}"
                        )
                        
                        print("[任務狀態更新]", {"task_id": task_id, "status": new_status.value, "ok": bool(updated)})
                        
                        # 產生更新後的 Flex Message 任務卡
                        if updated and reply_token:
                            # [修正] 如果是完成任務 (complete)，需要同時發送「更新後的任務卡」與「回報流程第一步」
                            if op == 'complete':
                                # 1. 更新後的任務卡
                                task_flex_dict = linebot_service.create_task_flex_card(updated)
                                task_container = FlexContainer.from_dict(task_flex_dict)
                                messages = [FlexMessage(alt_text=f"任務: {updated.title}", contents=task_container)]
                                
                                # 2. 回報流程第一步
                                print(f"[Postback] 觸發回報流程，任務ID: {task_id}")
                                report_bubble_dict = create_report_flow_card(
                                    step=1, 
                                    dept=f"{department_code} 測試", 
                                    room=updated.location or "Room N/A", 
                                    task_id=task_id
                                )
                                report_container = FlexContainer.from_dict(report_bubble_dict)
                                messages.append(FlexMessage(alt_text="任務回報 (1/5)", contents=report_container))
                                
                                # 一次發送多則訊息
                                await linebot_service.reply_messages(department_code, reply_token, messages)
                            else:
                                # 其他操作 (如 accept)，只發送更新後的任務卡
                                await linebot_service.send_task_flex_reply(
                                    department_code,
                                    reply_token,
                                    updated
                                )
                            return
                    else:
                        print(f"[任務狀態更新] 未知操作: {op}")
                        
                except Exception as e:
                    print("[任務狀態更新失敗]", {"task_id": task_id, "error": str(e)})

            # 如果沒有任務 ID，發送文字訊息
            if reply_token:
                response_msg = f"✅ 任務狀態已更新：{op}"
                if op == 'accept':
                    response_msg = "🙆‍♂️ 您已接受此派工任務！"
                elif op == 'complete':
                    response_msg = "✅ 任務已標記為完成！現在進入 5 步驟回報流程..."

                messages = [TextMessage(text=response_msg)]

                # 如果是完成操作，額外送出回報流程第 1 步
                if op == 'complete':
                    print(f"[Postback] 觸發回報流程，任務ID: {task_id}")
                    bubble_dict = create_report_flow_card(
                        step=1, 
                        dept=f"{department_code} 測試", 
                        room="Room N/A", 
                        task_id=task_id or "N/A"
                    )
                    bubble_container = FlexContainer.from_dict(bubble_dict)
                    messages.append(FlexMessage(alt_text="任務回報 (1/5)", contents=bubble_container))

                await linebot_service.reply_messages(
                    department_code,
                    reply_token,
                    messages
                )
        
        # 處理回報流程 (Report Flow)
        elif action == 'report':
            step = int(parsed.get('step', 1))
            task_id = parsed.get('id')
            ans = parsed.get('ans')  # yes/no/skip/camera/voice/text
            
            print(f"[Report] Step {step}, Task {task_id}, Ans {ans}")
            
            # 記錄答案 (如果是按鈕直接回傳的答案)
            if ans and ans not in ['camera', 'voice', 'text']:
                await linebot_service.record_report_answer(task_id, step, ans)
            
            # 決定下一步
            next_step = step + 1
            
            # 特殊處理：如果是需要使用者輸入的類型 (camera/voice/text)
            if ans in ['camera', 'voice', 'text']:
                user_id = event.get('source', {}).get('userId')
                if user_id:
                    self.user_input_state[user_id] = {
                        "task_id": task_id,
                        "step": step,
                        "type": ans,
                        "room": "Room N/A" 
                    }
                    
                    prompt_msg = "請拍攝照片上傳" if ans == 'camera' else \
                                 "請錄製語音說明" if ans == 'voice' else \
                                 "請輸入文字說明"
                    
                    await linebot_service.send_reply_message(department_code, reply_token, prompt_msg)
                return

            # 如果是最後一步 (Step 5 完成)
            if step >= 5:
                await linebot_service.send_reply_message(department_code, reply_token, "🎉 感謝！任務回報已完成。")
                return

            # 顯示下一步驟的卡片
            bubble = create_report_flow_card(
                step=next_step, 
                dept=f"{department_code} 測試", 
                room="Room N/A", 
                task_id=task_id
            )
            await linebot_service.reply_flex(
                department_code, 
                reply_token, 
                alt_text=f"任務回報 ({next_step}/5)", 
                flex_contents=bubble
            )

    # ----------------------------------------------------------------
    # 以下為 API 呼叫的介面 (由 linebot_routes.py 呼叫)
    # ----------------------------------------------------------------

    async def get_department_info(self, department_code: str):
        """API: 獲取部門資訊"""
        from app.core.database import SessionLocal
        from app.models.department import Department
        
        db = SessionLocal()
        try:
            dept = db.query(Department).filter(Department.code == department_code).first()
            if not dept:
                raise HTTPException(status_code=404, detail="部門不存在")
            
            stats = await linebot_service.get_task_statistics(department_code)
            
            return {
                "code": dept.code,
                "name": dept.name,
                "status": "active" if dept.is_active else "inactive",
                "statistics": stats
            }
        finally:
            db.close()

    async def get_department_tasks(self, department_code: str, status: Optional[str] = None, limit: int = 50):
        """API: 獲取部門任務"""
        from app.models.task import TaskStatus
        
        task_status = None
        if status:
            try:
                task_status = TaskStatus(status)
            except ValueError:
                pass
                
        tasks = await linebot_service.get_department_tasks(department_code, task_status, limit)
        return tasks

    async def update_task(self, task_id: str, status: str, notes: Optional[str] = None):
        """API: 更新任務"""
        from app.models.task import TaskStatus
        
        try:
            task_status = TaskStatus(status)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"無效的狀態: {status}")
            
        updated_task = await linebot_service.update_task_status(task_id, task_status, notes)
        
        if not updated_task:
            raise HTTPException(status_code=404, detail="任務不存在或更新失敗")
            
        return {"status": "success", "task": updated_task}

    async def broadcast_message(self, department_code: str, message: str):
        """API: 廣播訊息"""
        success = await linebot_service.broadcast_to_department(department_code, message)
        if success:
            return {"status": "success", "message": "廣播已發送"}
        else:
            raise HTTPException(status_code=500, detail="廣播失敗，請檢查 Bot 設定")


linebot_controller = LineBotController()
