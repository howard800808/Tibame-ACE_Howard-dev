from typing import Optional, List
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from datetime import datetime
from beanie import PydanticObjectId

from app.models.department import Department
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.linebot_schema import TaskCreate


class LineBotService:
    """LINE Bot 服務層 - 處理訊息與任務管理"""
    
    def __init__(self):
        self.department_bots: dict[str, tuple[LineBotApi, WebhookHandler]] = {}
        
    async def initialize_departments(self):
        """初始化所有部門的 LINE Bot"""
        departments = await Department.find({"is_active": True}).to_list()
        
        for dept in departments:
            try:
                bot_api = LineBotApi(dept.access_token)
                handler = WebhookHandler(dept.channel_secret)
                self.department_bots[dept.code] = (bot_api, handler)
                print(f"✓ 初始化部門 {dept.code} ({dept.name}) LINE Bot")
            except Exception as e:
                print(f"✗ 初始化部門 {dept.code} 失敗: {str(e)}")
    
    def get_bot_api(self, department_code: str) -> Optional[LineBotApi]:
        """取得指定部門的 LINE Bot API"""
        if department_code in self.department_bots:
            return self.department_bots[department_code][0]
        return None
    
    def get_webhook_handler(self, department_code: str) -> Optional[WebhookHandler]:
        """取得指定部門的 Webhook Handler"""
        if department_code in self.department_bots:
            return self.department_bots[department_code][1]
        return None
    
    async def handle_text_message(
        self,
        department_code: str,
        user_id: str,
        user_name: Optional[str],
        message_text: str,
        message_id: str,
        reply_token: str
    ) -> Optional[Task]:
        """處理文字訊息並建立任務"""
        
        # 取得部門資訊
        department = await Department.find_one({"code": department_code})
        if not department:
            return None
        
        # 解析訊息內容，判斷優先級
        priority = self._parse_priority(message_text)
        
        # 建立任務
        task = Task(
            department_code=department_code,
            department_name=department.name,
            line_user_id=user_id,
            line_user_name=user_name,
            title=self._extract_title(message_text),
            description=message_text,
            status=TaskStatus.PENDING,
            priority=priority,
            message_id=message_id,
            message_type="text",
            original_message=message_text,
        )
        
        await task.insert()
        
        # 發送確認訊息
        await self.send_reply_message(
            department_code,
            reply_token,
            f"✅ 任務已收到！\n\n📋 任務編號: {str(task.id)}\n🏢 部門: {department.name}\n📝 標題: {task.title}\n⚡ 優先級: {priority.value}\n\n我們會盡快處理您的請求。"
        )
        
        return task
    
    async def send_reply_message(
        self,
        department_code: str,
        reply_token: str,
        message: str
    ):
        """發送回覆訊息"""
        bot_api = self.get_bot_api(department_code)
        if bot_api:
            try:
                bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text=message)
                )
            except LineBotApiError as e:
                print(f"發送訊息失敗: {str(e)}")
    
    async def send_push_message(
        self,
        department_code: str,
        user_id: str,
        message: str
    ):
        """發送推送訊息"""
        bot_api = self.get_bot_api(department_code)
        if bot_api:
            try:
                bot_api.push_message(
                    user_id,
                    TextSendMessage(text=message)
                )
            except LineBotApiError as e:
                print(f"發送訊息失敗: {str(e)}")
    
    async def broadcast_to_department(
        self,
        department_code: str,
        message: str
    ):
        """向部門所有成員廣播訊息"""
        bot_api = self.get_bot_api(department_code)
        if bot_api:
            try:
                bot_api.broadcast(TextSendMessage(text=message))
            except LineBotApiError as e:
                print(f"廣播訊息失敗: {str(e)}")
    
    def _parse_priority(self, message: str) -> TaskPriority:
        """從訊息中解析優先級"""
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in ["緊急", "urgent", "立即", "馬上"]):
            return TaskPriority.URGENT
        elif any(keyword in message_lower for keyword in ["重要", "high", "優先"]):
            return TaskPriority.HIGH
        elif any(keyword in message_lower for keyword in ["低", "low", "不急"]):
            return TaskPriority.LOW
        else:
            return TaskPriority.MEDIUM
    
    def _extract_title(self, message: str, max_length: int = 50) -> str:
        """從訊息中提取標題"""
        # 取第一行或前 50 個字作為標題
        lines = message.split('\n')
        title = lines[0].strip()
        
        if len(title) > max_length:
            title = title[:max_length] + "..."
        
        return title if title else "新任務"
    
    async def get_department_tasks(
        self,
        department_code: str,
        status: Optional[TaskStatus] = None,
        limit: int = 100
    ) -> List[Task]:
        """取得部門的任務列表"""
        query = {"department_code": department_code}
        if status:
            query["status"] = status
        
        tasks = await Task.find(query).sort("-created_at").limit(limit).to_list()
        return tasks
    
    async def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        notes: Optional[str] = None
    ) -> Optional[Task]:
        """更新任務狀態"""
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            return None
        
        task.status = status
        task.updated_at = datetime.utcnow()
        
        if status == TaskStatus.COMPLETED:
            task.completed_at = datetime.utcnow()
        
        if notes:
            task.notes = notes
        
        await task.save()
        
        # 通知用戶狀態更新
        status_text = {
            TaskStatus.PENDING: "待處理",
            TaskStatus.IN_PROGRESS: "處理中",
            TaskStatus.COMPLETED: "已完成",
            TaskStatus.CANCELLED: "已取消"
        }
        
        await self.send_push_message(
            task.department_code,
            task.line_user_id,
            f"📢 任務狀態更新\n\n任務: {task.title}\n狀態: {status_text[status]}\n" + (f"備註: {notes}" if notes else "")
        )
        
        return task
    
    async def get_task_statistics(self, department_code: str) -> dict:
        """取得部門任務統計"""
        total = await Task.find({"department_code": department_code}).count()
        pending = await Task.find({
            "department_code": department_code,
            "status": TaskStatus.PENDING
        }).count()
        in_progress = await Task.find({
            "department_code": department_code,
            "status": TaskStatus.IN_PROGRESS
        }).count()
        completed = await Task.find({
            "department_code": department_code,
            "status": TaskStatus.COMPLETED
        }).count()
        
        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
            "completion_rate": round((completed / total * 100) if total > 0 else 0, 2)
        }


# 全域服務實例
linebot_service = LineBotService()
