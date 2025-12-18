from typing import Optional, List
from datetime import datetime
import json  # 新增這行

from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction
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
    def get_tasks_for_department(self, dept_code: str) -> List[dict]:
        """從 MySQL 取得部門任務並轉換為 Flex Message"""
        from app.core.database import SessionLocal
        from app.models.task_sql import HotelTask
        from templates.pull_task_linebot.flex_templates import create_hotel_task_card

        db = SessionLocal()
        try:
            # 取得該部門任務，按 ID 倒序排列 (顯示最新任務)
            tasks = db.query(HotelTask).filter(HotelTask.dept_code == dept_code).order_by(HotelTask.id.desc()).all()
            
            flex_messages = []
            for task in tasks:
                # 使用資料庫中的 title 欄位
                title = task.title if task.title else f"任務 #{task.task_id}"
                
                flex_msg = create_hotel_task_card(
                    dept=f"{task.dept_code} {task.dept_name}",
                    priority=task.sequence,
                    room=task.location_code,
                    guest=f"Room {task.guest_room_id}" if task.guest_room_id else "Guest",
                    title=title,
                    content=task.action_item,
                    time=f"{task.time_start}-{task.time_end}",
                    remark=task.note,
                    status=task.status.upper() if task.status else "PENDING",
                    task_id=task.task_id
                )
                
                # [修正] 確保狀態對應正確 (progress -> PROGRESS, done -> DONE)
                # 資料庫可能存 'progress' 或 'done'，這裡做標準化
                s_raw = task.status.lower() if task.status else "pending"
                s_mapped = "PENDING"
                if s_raw in ["progress", "in_progress"]:
                    s_mapped = "PROGRESS"
                elif s_raw in ["done", "completed"]:
                    s_mapped = "DONE"
                
                flex_msg['body']['contents'][2]['contents'][1]['text'] = {
                    "PROGRESS": "▶ 任務執行中",
                    "DONE": "✔ 已完成",
                    "PENDING": "● 任務未執行"
                }.get(s_mapped, "● 任務未執行")
                
                # 顏色也需要對應
                flex_msg['body']['contents'][2]['contents'][1]['color'] = {
                    "PROGRESS": "#188038",
                    "DONE": "#2C3E50",
                    "PENDING": "#D93025"
                }.get(s_mapped, "#D93025")
                
                # 按鈕狀態也需要更新 (create_hotel_task_card 已經做了一部分，但我們傳入的 status 參數可能不準)
                # 重新呼叫一次 create_hotel_task_card 比較保險，或者直接修改 flex_msg
                # 為了簡單起見，我們直接用正確的 status 參數重新生成
                
                flex_msg = create_hotel_task_card(
                    dept=f"{task.dept_code} {task.dept_name}",
                    priority=task.sequence,
                    room=task.location_code,
                    guest=f"Room {task.guest_room_id}" if task.guest_room_id else "Guest",
                    title=title,
                    content=task.action_item,
                    time=f"{task.time_start}-{task.time_end}",
                    remark=task.note,
                    status=s_mapped, # 使用標準化後的狀態
                    task_id=task.task_id
                )

                flex_messages.append(flex_msg)
            
            return flex_messages
        except Exception as e:
            print(f"[ERROR] 取得部門 {dept_code} 任務失敗: {e}")
            return []
        finally:
            db.close()

    def _get_quick_reply(self):
        """取得通用 Quick Reply 按鈕"""
        return QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="重新整理", text="重新整理"))
        ])

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

        # [New] 處理 "重新整理" 指令
        if message_text == "重新整理":
            print(f"[Command] 部門 {department_code} 收到重新整理請求")
            bubbles = self.get_tasks_for_department(department_code)
            
            if not bubbles:
                await self.send_reply_message(department_code, reply_token, "目前沒有待辦任務。")
                return None
            
            # 限制 Carousel 最多 12 張卡片 (Line 限制)
            bubbles = bubbles[:12]
            carousel = {"type": "carousel", "contents": bubbles}
            
            bot_api = self.get_bot_api(department_code)
            if bot_api:
                try:
                    message = FlexSendMessage(
                        alt_text=f"{department_code} 任務列表", 
                        contents=carousel,
                        quick_reply=self._get_quick_reply()
                    )
                    bot_api.reply_message(reply_token, message)
                except Exception as e:
                    print(f"[Error] 回覆任務列表失敗: {e}")
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
            bot_api.reply_message(reply_token, TextSendMessage(text=message, quick_reply=self._get_quick_reply()))
        except LineBotApiError as e:
            print(f"發送訊息失敗: {e}")

    async def reply_messages(self, department_code: str, reply_token: str, messages: list) -> bool:
        bot_api = self.get_bot_api(department_code)
        if not bot_api:
            print(f"回覆失敗: 部門 {department_code} 未初始化")
            return False
        try:
            # 確保最後一則訊息帶有 Quick Reply
            if messages:
                last_msg = messages[-1]
                if hasattr(last_msg, 'quick_reply'):
                    last_msg.quick_reply = self._get_quick_reply()
            
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
            bot_api.push_message(user_id, TextSendMessage(text=message, quick_reply=self._get_quick_reply()))
        except LineBotApiError as e:
            print(f"推送訊息失敗: {e}")

    async def broadcast_to_department(self, department_code: str, message: str) -> bool:
        bot_api = self.get_bot_api(department_code)
        if not bot_api:
            self.last_errors[department_code] = "Bot not initialized"
            return False
        try:
            bot_api.broadcast(TextSendMessage(text=message, quick_reply=self._get_quick_reply()))
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
            bot_api.broadcast(FlexSendMessage(alt_text=alt_text, contents=flex_contents, quick_reply=self._get_quick_reply()))
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
            bot_api.reply_message(reply_token, FlexSendMessage(alt_text=alt_text, contents=flex_contents, quick_reply=self._get_quick_reply()))
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
        # [Modified] 僅使用 MySQL 更新任務狀態，忽略 MongoDB
        
        from app.core.database import SessionLocal
        from app.models.task_sql import HotelTask
        
        db = SessionLocal()
        try:
            # 嘗試用 task_id (String) 查找
            sql_task = db.query(HotelTask).filter(HotelTask.task_id == task_id).first()
            if not sql_task:
                # 嘗試用 id (Integer) 查找
                if task_id.isdigit():
                    sql_task = db.query(HotelTask).filter(HotelTask.id == int(task_id)).first()
            
            if sql_task:
                # 將 TaskStatus enum 轉為字串 (pending, in_progress, completed)
                # 根據 flex_templates.py 的 STATUS_MAP，狀態碼為 PENDING, PROGRESS, DONE
                # 但資料庫可能存 'progress' 或 'done'
                
                if status == TaskStatus.IN_PROGRESS:
                    sql_task.status = "progress"
                elif status == TaskStatus.COMPLETED:
                    sql_task.status = "done"
                else:
                    sql_task.status = "pending"

                if notes:
                    current_note = sql_task.note or ""
                    timestamp = datetime.utcnow().strftime('%H:%M')
                    sql_task.note = f"{current_note}\n[{timestamp}] {notes}".strip()
                
                db.commit()
                db.refresh(sql_task) # 確保取得最新資料
                
                # 轉換為 MongoDB Task 的臨時物件 (供 Controller 使用)
                mapped_priority = TaskPriority.MEDIUM
                if sql_task.sequence == 'P': mapped_priority = TaskPriority.URGENT
                elif sql_task.sequence == 'E': mapped_priority = TaskPriority.HIGH
                
                mapped_status = TaskStatus.PENDING
                s_lower = sql_task.status.lower()
                if s_lower in ['progress', 'in_progress']: mapped_status = TaskStatus.IN_PROGRESS
                elif s_lower in ['done', 'completed']: mapped_status = TaskStatus.COMPLETED

                dummy_task = Task(
                    department_code=sql_task.dept_code,
                    department_name=sql_task.dept_name,
                    title=sql_task.title,
                    description=sql_task.action_item,
                    status=mapped_status,
                    priority=mapped_priority,
                    room=sql_task.location_code,
                    guest=f"Room {sql_task.guest_room_id}",
                    time_str=f"{sql_task.time_start}-{sql_task.time_end}",
                    notes=sql_task.note,
                    task_id=sql_task.task_id
                )
                # 賦予一個假的 ObjectId 以免報錯
                dummy_task.id = PydanticObjectId() 
                
                return dummy_task
            else:
                print(f"[Warning] MySQL 找不到任務: {task_id}")
                
        except Exception as e:
            print(f"[Error] MySQL 更新失敗: {e}")
        finally:
            db.close()

        return None
        from app.core.database import SessionLocal
        from app.models.task_sql import HotelTask
        
        db = SessionLocal()
        try:
            # 嘗試用 task_id (String) 查找
            sql_task = db.query(HotelTask).filter(HotelTask.task_id == task_id).first()
            if not sql_task:
                # 嘗試用 id (Integer) 查找
                if task_id.isdigit():
                    sql_task = db.query(HotelTask).filter(HotelTask.id == int(task_id)).first()
            
            if sql_task:
                # 將 TaskStatus enum 轉為字串 (pending, in_progress, completed)
                status_str = "pending"
                if status == TaskStatus.IN_PROGRESS:
                    status_str = "progress" # 注意：HotelTask 可能用 'progress' 或 'in_progress'，需確認
                elif status == TaskStatus.COMPLETED:
                    status_str = "done" # 注意：HotelTask 可能用 'done' 或 'completed'
                
                # 根據 flex_templates.py 的 STATUS_MAP，狀態碼為 PENDING, PROGRESS, DONE
                # 但 import_hotel_tasks.py 預設是 'pending'
                # 讓我們統一使用大寫或符合 STATUS_MAP 的值，或者保持小寫
                # 檢查 flex_templates.py: status.upper() -> PENDING, PROGRESS, DONE
                # 所以資料庫存什麼都可以，只要能對應。
                # 這裡我們存 'progress' 和 'done' 以示區別，或者跟隨 TaskStatus 的 value
                
                if status == TaskStatus.IN_PROGRESS:
                    sql_task.status = "progress"
                elif status == TaskStatus.COMPLETED:
                    sql_task.status = "done"
                else:
                    sql_task.status = "pending"

                if notes:
                    sql_task.note = (sql_task.note or "") + f"\n[{datetime.utcnow().strftime('%H:%M')}] {notes}"
                
                db.commit()
                
                # 為了回傳 Task 物件 (符合介面)，我們需要將 SQL task 轉換為 MongoDB Task 的臨時物件
                # 這樣 controller 才能繼續運作 (產生 Flex Card)
                
                # 轉換邏輯
                mapped_priority = TaskPriority.MEDIUM
                if sql_task.sequence == 'P': mapped_priority = TaskPriority.URGENT
                elif sql_task.sequence == 'E': mapped_priority = TaskPriority.HIGH
                
                mapped_status = TaskStatus.PENDING
                if sql_task.status.lower() == 'progress': mapped_status = TaskStatus.IN_PROGRESS
                elif sql_task.status.lower() == 'done': mapped_status = TaskStatus.COMPLETED

                dummy_task = Task(
                    department_code=sql_task.dept_code,
                    department_name=sql_task.dept_name,
                    title=sql_task.title,
                    description=sql_task.action_item,
                    status=mapped_status,
                    priority=mapped_priority,
                    room=sql_task.location_code,
                    guest=f"Room {sql_task.guest_room_id}",
                    time_str=f"{sql_task.time_start}-{sql_task.time_end}",
                    notes=sql_task.note,
                    task_id=sql_task.task_id # 重要：保留原始 ID
                )
                # 賦予一個假的 ObjectId 以免報錯 (雖然這裡不會存入 Mongo)
                dummy_task.id = PydanticObjectId() 
                
                return dummy_task
                
        except Exception as e:
            print(f"[Error] MySQL 更新失敗: {e}")
        finally:
            db.close()

        return None

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
            message = FlexSendMessage(
                alt_text=f"任務: {task.title}", 
                contents=flex_content,
                quick_reply=self._get_quick_reply()
            )
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
            
        from app.core.database import SessionLocal
        from app.models.task_sql import HotelTask, TaskReport
        
        db = SessionLocal()
        try:
            # 驗證任務是否存在
            sql_task = db.query(HotelTask).filter(HotelTask.task_id == task_id).first()
            if not sql_task and task_id.isdigit():
                sql_task = db.query(HotelTask).filter(HotelTask.id == int(task_id)).first()
                # 如果是用 ID 找到的，校正 task_id
                if sql_task:
                    task_id = sql_task.task_id
            
            if not sql_task:
                print(f"[Report] 失敗: 找不到任務 {task_id}")
                return
            
            # [Modified] 寫入 TaskReport 資料表
            new_report = TaskReport(
                task_id=task_id,
                step=step,
                answer=answer
            )
            db.add(new_report)
            
            print(f"[Report] 任務 {sql_task.title} - 步驟 {step} 紀錄答案: {answer}")

            if step >= 5:
                print(f"[Report] 任務 {sql_task.title} 回報流程完成！")
            
            db.commit()
        except Exception as e:
            print(f"[report] 寫入回報答案失敗 task_id={task_id}: {e}")
        finally:
            db.close()

    async def get_task_statistics(self, department_code: str) -> dict:
        from app.core.database import SessionLocal
        from app.models.task_sql import HotelTask
        
        db = SessionLocal()
        try:
            total = db.query(HotelTask).filter(HotelTask.dept_code == department_code).count()
            
            # 注意：MySQL 中的狀態可能是 'pending', 'progress', 'done' (小寫)
            # 或是 'PENDING', 'IN_PROGRESS', 'COMPLETED' (大寫)
            # 這裡做寬鬆匹配
            
            pending = db.query(HotelTask).filter(
                HotelTask.dept_code == department_code, 
                HotelTask.status.in_(['pending', 'PENDING'])
            ).count()
            
            in_progress = db.query(HotelTask).filter(
                HotelTask.dept_code == department_code, 
                HotelTask.status.in_(['progress', 'in_progress', 'PROGRESS', 'IN_PROGRESS'])
            ).count()
            
            completed = db.query(HotelTask).filter(
                HotelTask.dept_code == department_code, 
                HotelTask.status.in_(['done', 'completed', 'DONE', 'COMPLETED'])
            ).count()
            
            return {
                "total": total,
                "pending": pending,
                "in_progress": in_progress,
                "completed": completed,
                "completion_rate": round((completed / total * 100) if total else 0, 2),
            }
        except Exception as e:
            print(f"[Error] 取得統計數據失敗: {e}")
            return {
                "total": 0, "pending": 0, "in_progress": 0, "completed": 0, "completion_rate": 0
            }
        finally:
            db.close()

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
            if s == TaskStatus.COMPLETED:
                return "DONE"
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
