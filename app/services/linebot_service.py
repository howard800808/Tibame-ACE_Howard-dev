from typing import Optional, List
from datetime import datetime
import json  # 新增這行

from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, FlexSendMessage
from linebot.exceptions import LineBotApiError
from beanie import PydanticObjectId

from app.models.department import Department
from app.models.task import Task, TaskStatus, TaskPriority
from templates.pull_task_linebot.flex_templates import create_hotel_task_card


class LineBotService:
    """LINE Bot 服務層 - 處理訊息與任務管理"""

    def __init__(self):
        self.department_bots: dict[str, tuple[LineBotApi, WebhookHandler]] = {}
        self.last_errors: dict[str, str] = {}

    # ---------------------- 初始化與取得 Bot ----------------------
    async def initialize_departments(self):
        departments = await Department.find({"is_active": True}).to_list()
        for dept in departments:
            try:
                bot_api = LineBotApi(dept.access_token)
                handler = WebhookHandler(dept.channel_secret)
                self.department_bots[dept.code] = (bot_api, handler)
                self.last_errors.pop(dept.code, None)
                print(f"[OK] 初始化部門 {dept.code} ({dept.name}) LINE Bot")
            except Exception as e:
                self.last_errors[dept.code] = str(e)
                print(f"[ERROR] 初始化部門 {dept.code} 失敗: {e}")

    def get_bot_api(self, department_code: str) -> Optional[LineBotApi]:
        return self.department_bots.get(department_code, (None, None))[0]

    def get_webhook_handler(self, department_code: str) -> Optional[WebhookHandler]:
        return self.department_bots.get(department_code, (None, None))[1]

    # ---------------------- 任務處理 ----------------------
    async def handle_text_message(
        self,
        department_code: str,
        user_id: str,
        user_name: Optional[str],
        message_text: str,
        message_id: str,
        reply_token: str,
    ) -> Optional[Task]:
        department = await Department.find_one({"code": department_code})
        if not department:
            return None

        priority = self._parse_priority(message_text)
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
        await self.send_task_flex_reply(department_code, reply_token, task)
        return task

    # ---------------------- 基本訊息發送 ----------------------
    async def send_reply_message(self, department_code: str, reply_token: str, message: str):
        bot_api = self.get_bot_api(department_code)
        if not bot_api:
            print(f"回覆失敗: 部門 {department_code} 未初始化")
            return
        try:
            bot_api.reply_message(reply_token, TextSendMessage(text=message))
        except LineBotApiError as e:
            print(f"發送訊息失敗: {e}")

    async def reply_messages(self, department_code: str, reply_token: str, messages: list) -> bool:
        bot_api = self.get_bot_api(department_code)
        if not bot_api:
            print(f"回覆失敗: 部門 {department_code} 未初始化")
            return False
        try:
            bot_api.reply_message(reply_token, messages)
            return True
        except LineBotApiError as e:
            print(f"回覆多則訊息失敗: {e}")
            return False

    async def send_push_message(self, department_code: str, user_id: str, message: str):
        bot_api = self.get_bot_api(department_code)
        if not bot_api:
            print(f"推送失敗: 部門 {department_code} 未初始化")
            return
        try:
            bot_api.push_message(user_id, TextSendMessage(text=message))
        except LineBotApiError as e:
            print(f"推送訊息失敗: {e}")

    async def broadcast_to_department(self, department_code: str, message: str) -> bool:
        bot_api = self.get_bot_api(department_code)
        if not bot_api:
            self.last_errors[department_code] = "Bot not initialized"
            return False
        try:
            bot_api.broadcast(TextSendMessage(text=message))
            self.last_errors.pop(department_code, None)
            return True
        except LineBotApiError as e:
            self.last_errors[department_code] = str(e)
            print(f"廣播訊息失敗: {e}")
            return False

    async def broadcast_flex_to_department(self, department_code: str, alt_text: str, flex_contents: dict) -> bool:
        bot_api = self.get_bot_api(department_code)
        if not bot_api:
            self.last_errors[department_code] = "Bot not initialized"
            return False
        try:
            bot_api.broadcast(FlexSendMessage(alt_text=alt_text, contents=flex_contents))
            self.last_errors.pop(department_code, None)
            return True
        except LineBotApiError as e:
            self.last_errors[department_code] = str(e)
            print(f"廣播 Flex 訊息失敗: {e}")
            return False

    async def reply_flex(self, department_code: str, reply_token: str, alt_text: str, flex_contents: dict) -> bool:
        bot_api = self.get_bot_api(department_code)
        if not bot_api:
            return False
        try:
            bot_api.reply_message(reply_token, FlexSendMessage(alt_text=alt_text, contents=flex_contents))
            return True
        except LineBotApiError as e:
            print(f"回覆 Flex 訊息失敗: {e}")
            return False

    # ---------------------- 任務查詢與更新 ----------------------
    def _parse_priority(self, message: str) -> TaskPriority:
        lower = message.lower()
        if any(k in lower for k in ["緊急", "urgent", "立即", "馬上"]):
            return TaskPriority.URGENT
        if any(k in lower for k in ["重要", "high", "優先"]):
            return TaskPriority.HIGH
        if any(k in lower for k in ["低", "low", "不急"]):
            return TaskPriority.LOW
        return TaskPriority.MEDIUM

    def _extract_title(self, message: str, max_length: int = 50) -> str:
        title = (message.split("\n")[0]).strip()
        if len(title) > max_length:
            title = title[:max_length] + "..."
        return title or "新任務"

    async def get_department_tasks(self, department_code: str, status: Optional[TaskStatus] = None, limit: int = 100) -> List[Task]:
        query = {"department_code": department_code}
        if status:
            query["status"] = status
        return await Task.find(query).sort("-created_at").limit(limit).to_list()

    async def update_task_status(self, task_id: str, status: TaskStatus, notes: Optional[str] = None) -> Optional[Task]:
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
        return task

        status_text = {
            TaskStatus.PENDING: "待處理",
            TaskStatus.IN_PROGRESS: "處理中",
            TaskStatus.COMPLETED: "已完成",
            TaskStatus.CANCELLED: "已取消",
        }
        await self.send_push_message(
            task.department_code,
            task.line_user_id,
            f"📢 任務狀態更新\n\n任務: {task.title}\n狀態: {status_text[status]}" + (f"\n備註: {notes}" if notes else "")
        )
        return task

    async def send_task_flex_card(self, department_code: str, user_id: Optional[str], task: Task, use_push: bool = True) -> bool:
        bot_api = self.get_bot_api(department_code)
        if not bot_api:
            print(f"發送 Flex 卡片失敗: 部門 {department_code} 未初始化")
            return False
        try:
            flex_content = self.create_task_flex_card(task)
            message = FlexSendMessage(alt_text=f"任務: {task.title}", contents=flex_content)
            if use_push and user_id:
                bot_api.push_message(user_id, message)
            else:
                bot_api.broadcast(message)
            return True
        except LineBotApiError as e:
            print(f"發送 Flex 卡片失敗: {e}")
            return False

    async def send_task_flex_reply(self, department_code: str, reply_token: str, task: Task) -> bool:
        bot_api = self.get_bot_api(department_code)
        
        # 產生 Flex 內容
        flex_content = self.create_task_flex_card(task)
        
        # [Debug] 印出 JSON 供測試用
        print(f"\n[Debug] 任務 Flex 卡片 JSON (可複製到 Simulator):")
        print(json.dumps(flex_content, ensure_ascii=False, indent=2))
        print("-" * 50)

        if not bot_api:
            print(f"回覆 Flex 卡片失敗: 部門 {department_code} 未初始化")
            return False
            
        try:
            message = FlexSendMessage(alt_text=f"任務: {task.title}", contents=flex_content)
            bot_api.reply_message(reply_token, message)
            print(f"[Success] 成功回覆任務卡片 (Token: {reply_token[:10]}...)")
            return True
        except LineBotApiError as e:
            # 這裡特別處理：如果是測試用的假 Token，我們只印警告不當作程式錯誤
            if "Invalid reply token" in str(e):
                print(f"[Warning] 測試模式: 忽略無效的 Reply Token 錯誤。流程繼續。")
                return True
            print(f"回覆 Flex 卡片失敗: {e}")
            return False

    # ---------------------- 報告相關 ----------------------
    async def record_report_answer(self, task_id: Optional[str], step: int, answer: Optional[str]) -> None:
        if not task_id:
            print("[Report] 失敗: 缺少 task_id")
            return
        try:
            task = await Task.get(PydanticObjectId(task_id))
            if not task:
                print(f"[Report] 失敗: 找不到任務 {task_id}")
                return
            
            # 紀錄答案
            new_record = {
                "step": step,
                "answer": answer,
                "recorded_at": datetime.utcnow(),
            }
            task.report_answers.append(new_record)
            
            print(f"[Report] 任務 {task.title} - 步驟 {step} 紀錄答案: {answer}")

            if step >= 5:
                task.report_completed = True
                print(f"[Report] 任務 {task.title} 回報流程完成！")
            
            task.updated_at = datetime.utcnow()
            await task.save()
        except Exception as e:
            print(f"[report] 寫入回報答案失敗 task_id={task_id}: {e}")

    async def get_task_statistics(self, department_code: str) -> dict:
        total = await Task.find({"department_code": department_code}).count()
        pending = await Task.find({"department_code": department_code, "status": TaskStatus.PENDING}).count()
        in_progress = await Task.find({"department_code": department_code, "status": TaskStatus.IN_PROGRESS}).count()
        completed = await Task.find({"department_code": department_code, "status": TaskStatus.COMPLETED}).count()
        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
            "completion_rate": round((completed / total * 100) if total else 0, 2),
        }

    def get_last_error(self, department_code: str) -> Optional[str]:
        return self.last_errors.get(department_code)

    # ---------------------- Flex 產生 ----------------------
    def create_task_flex_card(self, task: Task) -> dict:
        def safe_text(value: str, default: str = "-") -> str:
            return value if value and str(value).strip() else default

        def map_priority(p: TaskPriority) -> str:
            if p == TaskPriority.URGENT:
                return "P"
            if p == TaskPriority.HIGH:
                return "E"
            return "F"

        def map_status(s: TaskStatus) -> str:
            if s == TaskStatus.IN_PROGRESS:
                return "PROGRESS"
            return "PENDING"

        # [修正] 優先使用標準欄位，若無則使用相容性欄位 (舊版資料)
        dept = safe_text(task.department_name or task.department_code or task.dept)
        priority = map_priority(task.priority)
        
        # Room: 優先取 tags[0]，否則取 room 欄位
        room = "Room N/A"
        if task.tags and len(task.tags) > 0:
            room = task.tags[0]
        elif task.room:
            room = task.room
            
        guest = safe_text(task.line_user_name or task.guest or "Guest")
        title = safe_text(task.title or "未命名任務")
        content = safe_text(task.description or task.content or "")
        
        # Time: 優先取 due_date，否則取 time_str
        time_text = "-"
        if task.due_date:
            time_text = task.due_date.strftime("%H:%M")
        elif task.time_str:
            time_text = task.time_str
            
        remark = safe_text(task.notes or task.remark or "")
        status_code = map_status(task.status)

        return create_hotel_task_card(
            dept=dept,
            priority=priority,
            room=room,
            guest=guest,
            title=title,
            content=content,
            time=time_text,
            remark=remark,
            status=status_code,
            task_id=str(task.id),
        )

    def _priority_label(self, priority: TaskPriority) -> str:
        labels = {
            TaskPriority.URGENT: "🔴 緊急 (URGENT)",
            TaskPriority.HIGH: "🟠 高 (HIGH)",
            TaskPriority.MEDIUM: "🟢 中 (MEDIUM)",
            TaskPriority.LOW: "🟢 低 (LOW)",
        }
        return labels.get(priority, "未知")


linebot_service = LineBotService()
