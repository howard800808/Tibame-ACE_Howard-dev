from fastapi import Request, HTTPException, Header
from typing import Optional
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage

from app.services.linebot_service import linebot_service
from app.models.department import Department


class LineBotController:
    """LINE Bot 控制器 - 處理 Webhook 請求"""
    
    async def handle_webhook(
        self,
        department_code: str,
        request: Request,
        x_line_signature: str = Header(None)
    ):
        """處理 LINE Bot Webhook 請求"""
        
        # 取得請求內容
        body = await request.body()
        body_str = body.decode('utf-8')
        
        # 驗證部門是否存在
        department = await Department.find_one({"code": department_code, "is_active": True})
        if not department:
            raise HTTPException(status_code=404, detail=f"部門 {department_code} 不存在或未啟用")
        
        # 取得 Webhook Handler
        handler = linebot_service.get_webhook_handler(department_code)
        if not handler:
            raise HTTPException(status_code=500, detail=f"部門 {department_code} LINE Bot 未初始化")
        
        # 驗證簽名
        try:
            handler.handle(body_str, x_line_signature)
        except InvalidSignatureError:
            raise HTTPException(status_code=400, detail="無效的簽名")
        
        # 解析事件
        import json
        events_data = json.loads(body_str)
        
        for event in events_data.get('events', []):
            await self._process_event(department_code, event)
        
        return {"status": "ok"}
    
    async def _process_event(self, department_code: str, event: dict):
        """處理單個事件"""
        event_type = event.get('type')
        
        if event_type == 'message':
            await self._handle_message_event(department_code, event)
        elif event_type == 'follow':
            await self._handle_follow_event(department_code, event)
        elif event_type == 'unfollow':
            await self._handle_unfollow_event(department_code, event)
        # 可以添加更多事件類型處理
    
    async def _handle_message_event(self, department_code: str, event: dict):
        """處理訊息事件"""
        message = event.get('message', {})
        message_type = message.get('type')
        
        if message_type == 'text':
            # 取得用戶資訊
            source = event.get('source', {})
            user_id = source.get('userId')
            
            # 取得用戶名稱（需要額外 API 調用，這裡簡化處理）
            user_name = None
            bot_api = linebot_service.get_bot_api(department_code)
            if bot_api and user_id:
                try:
                    profile = bot_api.get_profile(user_id)
                    user_name = profile.display_name
                except:
                    pass
            
            # 處理文字訊息
            message_text = message.get('text')
            message_id = message.get('id')
            reply_token = event.get('replyToken')
            
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
            department = await Department.find_one({"code": department_code})
            welcome_message = f"歡迎加入 {department.name} 任務管理系統！\n\n您可以直接傳送訊息來建立新任務，我們會盡快處理。"
            
            await linebot_service.send_reply_message(
                department_code,
                reply_token,
                welcome_message
            )
    
    async def _handle_unfollow_event(self, department_code: str, event: dict):
        """處理取消好友事件"""
        source = event.get('source', {})
        user_id = source.get('userId')
        
        # 可以在這裡記錄用戶取消追蹤
        print(f"用戶 {user_id} 取消追蹤部門 {department_code}")
    
    async def get_department_info(self, department_code: str):
        """取得部門資訊"""
        department = await Department.find_one({"code": department_code})
        if not department:
            raise HTTPException(status_code=404, detail="部門不存在")
        
        # 取得統計資料
        stats = await linebot_service.get_task_statistics(department_code)
        
        return {
            "department": {
                "code": department.code,
                "name": department.name,
                "description": department.description,
                "is_active": department.is_active
            },
            "statistics": stats
        }
    
    async def get_department_tasks(
        self,
        department_code: str,
        status: Optional[str] = None,
        limit: int = 50
    ):
        """取得部門任務列表"""
        from app.models.task import TaskStatus
        
        department = await Department.find_one({"code": department_code})
        if not department:
            raise HTTPException(status_code=404, detail="部門不存在")
        
        task_status = None
        if status:
            try:
                task_status = TaskStatus(status)
            except ValueError:
                raise HTTPException(status_code=400, detail="無效的狀態值")
        
        tasks = await linebot_service.get_department_tasks(
            department_code,
            task_status,
            limit
        )
        
        return {
            "department": department.name,
            "tasks": tasks
        }
    
    async def update_task(
        self,
        task_id: str,
        status: str,
        notes: Optional[str] = None
    ):
        """更新任務狀態"""
        from app.models.task import TaskStatus
        
        try:
            task_status = TaskStatus(status)
        except ValueError:
            raise HTTPException(status_code=400, detail="無效的狀態值")
        
        task = await linebot_service.update_task_status(task_id, task_status, notes)
        if not task:
            raise HTTPException(status_code=404, detail="任務不存在")
        
        return {"status": "success", "task": task}
    
    async def broadcast_message(
        self,
        department_code: str,
        message: str
    ):
        """向部門廣播訊息"""
        department = await Department.find_one({"code": department_code, "is_active": True})
        if not department:
            raise HTTPException(status_code=404, detail="部門不存在或未啟用")
        
        await linebot_service.broadcast_to_department(department_code, message)
        
        return {"status": "success", "message": "訊息已發送"}


# 全域控制器實例
linebot_controller = LineBotController()
