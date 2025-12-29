from typing import Optional, List, Dict, Tuple, Any
from datetime import datetime
import json
import uuid

# LINE Bot SDK v3 Imports
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    PushMessageRequest,
    BroadcastRequest,
    TextMessage,
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyItem,
    MessageAction,
    ApiException
)
from linebot.v3.webhook import SignatureValidator

from app.models.task import Task, TaskStatus, TaskPriority

# TODO: 請將此處替換為您的實際網域 (例如 ngrok 網址或正式站台)
BASE_WEB_URL = "https://interinhibitive-unexceptional-lino.ngrok-free.dev"

# ==========================================
# Flex Message Templates (Merged from line_service.py)
# ==========================================

def create_universal_task_card(dept, priority, room, guest, title, content, time, remark, status='PENDING', task_id=None, db_id=None):
    # 生成五星級飯店通用派工卡片 (萬用模板)
    
    # 優先級色碼表 (P=紅, E=黃, F=綠)
    PRIORITY_MAP = {
        'P': {'color': '#D93025'},  # Red
        'E': {'color': '#F59E0B'},  # Amber Yellow
        'F': {'color': '#188038'}   # Green
    }

    # 狀態與按鈕邏輯表
    STATUS_MAP = {
        'PENDING': {
            'label': '● 任務未執行',
            'color': '#D93025',       # 紅色文字
            'btn_text': '接受任務 (Accept)',
            'btn_color': '#1A3B5D',   # 藍色按鈕
            'op': 'accept'
        },
        'PROGRESS': {
            'label': '▶ 任務執行中',
            'color': '#188038',       # 綠色文字
            'btn_text': '任務完成回報 (Report)',
            'btn_color': '#188038',   # 綠色按鈕
            'op': 'complete',
            'action_type': 'uri'
        },
        'DONE': {
            'label': '✔ 已完成',
            'color': '#2C3E50',       # 灰色文字
            'btn_text': '查看歸檔 (Archived)',
            'btn_color': '#B4B4B4',   # 灰色按鈕
            'op': 'archive'
        }
    }

    # 防呆機制
    p_code = str(priority).upper() if priority else 'F'
    p_style = PRIORITY_MAP.get(p_code, PRIORITY_MAP['F'])
    
    s_code = str(status).upper() if status else 'PENDING'
    s_style = STATUS_MAP.get(s_code, STATUS_MAP['PENDING'])

    return {
      'type': 'bubble',
      'size': 'mega',
      'header': {
        'type': 'box',
        'layout': 'vertical',
        'contents': [
          {
            'type': 'box',
            'layout': 'horizontal',
            'contents': [
              {
                'type': 'text',
                'text': str(dept),
                'color': '#B4B4B4',
                'weight': 'bold',
                'size': 'xs',
                'gravity': 'center',
                'flex': 1
              },
              {
                'type': 'box',
                'layout': 'vertical',
                'contents': [
                  {
                    'type': 'text',
                    'text': p_code,
                    'color': '#FFFFFF',
                    'size': 'xs',
                    'weight': 'bold',
                    'align': 'center'
                  }
                ],
                'backgroundColor': p_style['color'],
                'cornerRadius': '10px',
                'width': '30px',
                'height': '20px',
                'justifyContent': 'center'
              }
            ]
          },
          {
            'type': 'text',
            'text': str(room),
            'weight': 'bold',
            'size': '3xl',
            'color': '#FFFFFF',
            'margin': 'md'
          },
          {
            'type': 'text',
            'text': f'Guest: {guest}',
            'color': '#C5A065',
            'size': 'sm',
            'margin': 'sm',
            'weight': 'bold'
          }
        ],
        'backgroundColor': '#1A3B5D',
        'paddingAll': '20px'
      },
      'body': {
        'type': 'box',
        'layout': 'vertical',
        'contents': [
          {
            'type': 'text',
            'text': str(title),
            'weight': 'bold',
            'size': 'xl',
            'color': '#1A3B5D'
          },
          {
            'type': 'separator',
            'margin': 'lg',
            'color': '#E5E5E5'
          },
          {
            'type': 'box',
            'layout': 'horizontal',
            'contents': [
              {
                'type': 'box', 'layout': 'vertical',
                'contents': [{'type': 'text', 'text': '目前狀態', 'size': 'sm', 'color': '#aaaaaa'}],
                'width': '85px', 'flex': 0
              },
              {
                'type': 'text',
                'text': s_style['label'],
                'size': 'sm',
                'color': s_style['color'],
                'flex': 1, 'weight': 'bold', 'wrap': True
              }
            ],
            'margin': 'lg'
          },
          {
            'type': 'box',
            'layout': 'horizontal',
            'contents': [
              {
                'type': 'box', 'layout': 'vertical',
                'contents': [{'type': 'text', 'text': '預定時間', 'size': 'sm', 'color': '#aaaaaa'}],
                'width': '85px', 'flex': 0
              },
              {
                'type': 'text',
                'text': str(time) if time and str(time).strip() and str(time) != 'None' else '-',
                'size': 'sm',
                'color': '#333333',
                'flex': 1, 'wrap': True, 'weight': 'bold'
              }
            ],
            'margin': 'md'
          },
          {
            'type': 'box',
            'layout': 'horizontal',
            'contents': [
              {
                'type': 'box', 'layout': 'vertical',
                'contents': [{'type': 'text', 'text': '任務內容', 'size': 'sm', 'color': '#aaaaaa'}],
                'width': '85px', 'flex': 0
              },
              {
                'type': 'text',
                'text': str(content) if content and str(content).strip() and str(content) != 'None' else '-',
                'size': 'sm',
                'color': '#555555',
                'flex': 1, 'wrap': True
              }
            ],
            'margin': 'md'
          },
          {
            'type': 'box',
            'layout': 'horizontal',
            'contents': [
              {
                'type': 'box', 'layout': 'vertical',
                'contents': [{'type': 'text', 'text': '備註', 'size': 'sm', 'color': '#aaaaaa'}],
                'width': '85px', 'flex': 0
              },
              {
                'type': 'text',
                'text': str(remark) if remark and str(remark).strip() and str(remark) != 'None' else '-',
                'size': 'sm',
                'color': p_style['color'],
                'flex': 1, 'wrap': True, 'weight': 'bold'
              }
            ],
            'margin': 'md'
          }
        ],
        'paddingAll': '20px'
      },
      'footer': {
        'type': 'box',
        'layout': 'vertical',
        'contents': [
          {
            'type': 'button',
            'action': {
                'type': 'uri',
                'label': s_style['btn_text'],
                'uri': f'{BASE_WEB_URL}/emotional-tasks/report/{db_id if db_id else task_id}'
            } if s_style.get('action_type') == 'uri' else {
              'type': 'postback',
              'label': s_style['btn_text'],
              'data': f'action=task&op={s_style["op"]}&id={task_id}&dept={str(dept).split(" ")[0]}' if task_id else 'action=none'
            },
            'style': 'primary',
            'color': s_style['btn_color'],
            'height': 'sm'
          }
        ],
        'paddingAll': '20px'
      }
    }

# Alias for backward compatibility
create_hotel_task_card = create_universal_task_card

def create_report_flow_card(step, dept, room, task_id):
    # 生成任務回報流程卡片 (Step 1 ~ 5)
    
    STEPS_CONFIG = {
        1: {
            'title': '任務回報 (1/5)',
            'question': '是否順利完成？',
            'desc': '請確認現場狀況是否符合驗收標準。',
            'buttons': [
                {'label': '是 (Yes)', 'color': '#188038', 'style': 'primary', 'data': f'action=report&step=1&id={task_id}&ans=yes&room={room}'},
                {'label': '否 (No)',  'color': '#D93025', 'style': 'primary', 'data': f'action=report&step=1&id={task_id}&ans=no&room={room}'}
            ]
        },
        2: {
            'title': '任務回報 (2/5)',
            'question': '補充說明 / 微調查',
            'desc': '請簡述現場執行狀況或特殊備註。',
          'buttons': [
            {'label': '🎤 語音輸入', 'color': '#1A3B5D', 'style': 'primary', 'data': f'action=report&step=2&id={task_id}&ans=voice&room={room}'},
            {'label': '⌨️ 文字輸入', 'color': '#B4B4B4', 'style': 'secondary', 'data': f'action=report&step=2&id={task_id}&ans=text&room={room}'}
            ]
        },
        3: {
            'title': '任務回報 (3/5)',
            'question': '與顧客有互動嗎？',
            'desc': '若有遇見客人，後續請簡述互動內容。',
            'buttons': [
                {'label': '有 (Yes)', 'color': '#1A3B5D', 'style': 'primary',   'data': f'action=report&step=3&id={task_id}&ans=yes&room={room}'},
                {'label': '無 (No)',  'color': '#B4B4B4', 'style': 'secondary', 'data': f'action=report&step=3&id={task_id}&ans=no&room={room}'}
            ]
        },
        4: {
            'title': '任務回報 (4/5)',
            'question': '顧客情緒判斷',
            'desc': '請依照觀察，記錄客人當下的情緒反應。',
            'buttons': [
                {'label': '正向', 'color': '#188038', 'style': 'primary', 'data': f'action=report&step=4&id={task_id}&ans=positive&room={room}'},
                {'label': '中性', 'color': '#5A6A7B', 'style': 'primary', 'data': f'action=report&step=4&id={task_id}&ans=neutral&room={room}'},
                {'label': '負向', 'color': '#D93025', 'style': 'primary', 'data': f'action=report&step=4&id={task_id}&ans=negative&room={room}'}
            ]
        },
        5: {
            'title': '任務回報 (5/5)',
            'question': '備註事項',
            'desc': '請補充其他重要事項，若無可直接略過。',
          'buttons': [
            {'label': '✅ 完成', 'color': '#188038', 'style': 'primary', 'data': f'action=report&step=5&id={task_id}&ans=done&room={room}'},
            {'label': '略過', 'color': '#B4B4B4', 'style': 'secondary', 'data': f'action=report&step=5&id={task_id}&ans=skip&room={room}'}
            ]
        }
    }

    current_config = STEPS_CONFIG.get(step, STEPS_CONFIG[1])

    footer_contents = []
    for idx, btn in enumerate(current_config['buttons']):
        if idx > 0:
            footer_contents.append({'type': 'separator', 'margin': 'md'})
            
        button_obj = {
            'type': 'button',
            'style': btn['style'],
            'color': btn['color'],
            'height': 'sm',
            'flex': 1
        }
        
        if btn.get('type') == 'uri':
            button_obj['action'] = {'type': 'uri', 'label': btn['label'], 'uri': btn['uri']}
        else:
            button_obj['action'] = {'type': 'postback', 'label': btn['label'], 'data': btn.get('data', 'no_data')}
            
        footer_contents.append(button_obj)

    return {
      'type': 'bubble',
      'size': 'mega',
      'header': {
        'type': 'box',
        'layout': 'vertical',
        'contents': [
          {
            'type': 'box',
            'layout': 'horizontal',
            'contents': [
              {
                'type': 'text', 'text': str(dept),
                'color': '#B4B4B4', 'weight': 'bold', 'size': 'xs', 'gravity': 'center', 'flex': 1
              },
              {
                'type': 'text', 'text': str(room),
                'weight': 'bold', 'size': 'lg', 'color': '#FFFFFF', 'gravity': 'center', 'align': 'end', 'flex': 1
              }
            ]
          }
        ],
        'backgroundColor': '#1A3B5D', 'paddingAll': '20px'
      },
      'body': {
        'type': 'box',
        'layout': 'vertical',
        'contents': [
          {
            'type': 'text', 'text': current_config['title'],
            'weight': 'bold', 'size': 'xs', 'color': '#C5A065'
          },
          {
            'type': 'text', 'text': current_config['question'],
            'weight': 'bold', 'size': 'xl', 'color': '#1A3B5D', 'margin': 'md'
          },
          {
            'type': 'text', 'text': current_config['desc'],
            'size': 'sm', 'color': '#aaaaaa', 'margin': 'sm', 'wrap': True
          }
        ],
        'paddingAll': '20px'
      },
      'footer': {
        'type': 'box',
        'layout': 'horizontal',
        'contents': footer_contents,
        'paddingAll': '20px'
      }
    }


class LineBotService:
    # LINE Bot 服務層 - 處理訊息與任務管理 (v3 SDK)

    def __init__(self):
        # Store (access_token, channel_secret)
        self.department_creds: Dict[str, Tuple[str, str]] = {}
        self.last_errors: Dict[str, str] = {}

    # ---------------------- 初始化與取得 Bot ----------------------
    async def initialize_departments(self):
        from app.core.database import SessionLocal
        from app.models.department import Department

        db = SessionLocal()
        try:
            departments = db.query(Department).all()
            print(f'\n[初始化] 從資料庫載入 {len(departments)} 個部門')
            
            for dept in departments:
                if dept.channel_access_token and dept.channel_secret:
                    self.department_creds[dept.code] = (dept.channel_access_token, dept.channel_secret)
                    self.last_errors.pop(dept.code, None)
                    print(f'[OK] 初始化部門 {dept.code} ({dept.name_zh})')
                    print(f'     Token: {dept.channel_access_token[:20]}...')
                    print(f'     Secret: {dept.channel_secret[:10]}...')
                else:
                    print(f'[WARN] 部門 {dept.code} 缺少 Token 或 Secret')
            
            print(f'[初始化] 完成，共 {len(self.department_creds)} 個部門可用\n')
        except Exception as e:
            print(f'[ERROR] 初始化部門失敗: {e}')
            import traceback
            traceback.print_exc()
        finally:
            db.close()

    def validate_signature(self, department_code: str, body: str, signature: str) -> bool:
        """驗證 LINE Webhook 簽名
        
        Args:
            department_code: 部門代碼
            body: 請求內容 (str)
            signature: X-Line-Signature 標頭值 (str)
        
        Returns:
            bool: 驗證是否成功
        """
        creds = self.department_creds.get(department_code)
        if not creds:
            return False
        
        _, secret = creds
        try:
            validator = SignatureValidator(secret)
            # LINE SDK v3 的 validate 方法需要 str 參數，不是 bytes
            result = validator.validate(body, signature)
            return result
        except Exception as e:
            print(f"[Signature] ❌ 部門 {department_code} 驗證異常: {e}")
            return False

    def _get_quick_reply(self):
        # 取得通用 Quick Reply 按鈕
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label='重新整理', text='重新整理'))
        ])

    # ---------------------- 任務處理 ----------------------
    def get_tasks_for_department(self, dept_code: str) -> List[dict]:
        """從資料庫取得部門任務，若一般任務為空則回退使用感動任務"""
        from app.core.database import SessionLocal
        from app.models.task import Task
        from app.models.emotional_task import EmotionalTask
        from app.models.department import Department

        def map_status(raw: Optional[str]) -> str:
            val = (raw or '').lower()
            if val in ['progress', 'in_progress', 'assigned']:
                return 'PROGRESS'
            if val in ['done', 'completed']:
                return 'DONE'
            return 'PENDING'

        def map_priority(code: Optional[str]) -> str:
            if not code:
                return 'F'
            val = str(code).upper()
            return val[0] if val[0] in ['P', 'E', 'F'] else 'F'

        def format_time_range(start_time, end_time) -> str:
            start_text = start_time.strftime('%H:%M') if start_time else ''
            end_text = end_time.strftime('%H:%M') if end_time else ''
            if start_text and end_text:
                return f'{start_text}~{end_text}'
            return start_text or end_text or '-'

        db = SessionLocal()
        try:
            dept_display = dept_code
            dept_info = db.query(Department).filter(Department.code == dept_code).first()
            if dept_info:
                dept_display = f"{dept_info.code} {dept_info.name_zh}"

            # [Modified] 只顯示感動派工任務，忽略一般任務
            # tasks = db.query(Task).filter(Task.department == dept_code).order_by(Task.id.desc()).all()
            flex_messages: List[dict] = []

            # for task in tasks:
            #     title = task.title if task.title else f'任務 #{task.task_uid}'
            #     flex_messages.append(create_hotel_task_card(
            #         dept=dept_display,
            #         priority=map_priority(task.priority),
            #         room=task.location,
            #         guest='Guest',
            #         title=title,
            #         content=task.description,
            #         time=task.due_at.strftime('%H:%M') if task.due_at else '-',
            #         remark='',
            #         status=map_status(task.status),
            #         task_id=task.task_uid
            #     ))

            # 感動派工任務
            emo_tasks = (
                db.query(EmotionalTask)
                .filter(EmotionalTask.dept_code == dept_code)
                .filter(EmotionalTask.status.in_(['pending', 'assigned', 'in_progress']))
                .order_by(EmotionalTask.task_date.desc(), EmotionalTask.time_start.asc())
                .limit(20)
                .all()
            )

            for emo in emo_tasks:
                flex_messages.append(create_hotel_task_card(
                    dept=dept_display,
                    priority=map_priority(emo.sequence_stage),
                    room=emo.location_code or 'N/A',
                    guest=emo.project_code or 'Guest',
                    title=emo.task_title or f'任務 {emo.task_id}',
                    content=emo.action_item or '-',
                    time=format_time_range(emo.time_start, emo.time_end) or '-',
                    remark=emo.note or '-',
                    status=map_status(emo.status),
                    task_id=emo.task_id,
                    db_id=emo.id
                ))

            return flex_messages
        except Exception as e:
            print(f'[ERROR] 取得部門 {dept_code} 任務失敗: {e}')
            return []
        finally:
            db.close()

    async def handle_text_message(
        self,
        department_code: str,
        user_id: str,
        user_name: Optional[str],
        message_text: str,
        message_id: str,
        reply_token: str,
    ) -> Optional[Task]:
        from app.core.database import SessionLocal
        from app.models.department import Department
        from app.models.task import Task
        import uuid

        db = SessionLocal()
        try:
            department = db.query(Department).filter(Department.code == department_code).first()
            if not department:
                return None

            if message_text == '重新整理':
                print(f'[Command] 部門 {department_code} 收到重新整理請求')
                bubbles = self.get_tasks_for_department(department_code)
                
                if not bubbles:
                    await self.send_reply_message(department_code, reply_token, '目前沒有待辦任務。')
                    return None
                
                bubbles = bubbles[:12]
                # Carousel
                carousel = {'type': 'carousel', 'contents': bubbles}
                
                await self.reply_flex(department_code, reply_token, f'{department_code} 任務列表', carousel)
                return None

            priority = self._parse_priority(message_text)
            
            new_task = Task(
                task_uid=str(uuid.uuid4()),
                department=department_code,
                title=self._extract_title(message_text),
                description=message_text,
                status=TaskStatus.PENDING.value,
                priority=priority.value if hasattr(priority, 'value') else priority,
                line_message_id=message_id,
            )
            
            db.add(new_task)
            db.commit()
            db.refresh(new_task)
            
            await self.send_task_flex_reply(department_code, reply_token, new_task)
            return new_task
        except Exception as e:
            print(f'[ERROR] 處理文字訊息失敗: {e}')
            return None
        finally:
            db.close()

    # ---------------------- 基本訊息發送 (v3) ----------------------
    async def send_reply_message(self, department_code: str, reply_token: str, message: str):
        creds = self.department_creds.get(department_code)
        if not creds:
            print(f'回覆失敗: 部門 {department_code} 未初始化')
            return
        token, _ = creds
        
        try:
            configuration = Configuration(access_token=token)
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(text=message, quick_reply=self._get_quick_reply())]
                    )
                )
        except ApiException as e:
            print(f'發送訊息失敗: {e}')

    async def reply_messages(self, department_code: str, reply_token: str, messages: list) -> bool:
        creds = self.department_creds.get(department_code)
        if not creds:
            return False
        token, _ = creds
        
        try:
            configuration = Configuration(access_token=token)
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=messages
                    )
                )
            return True
        except ApiException as e:
            print(f'回覆多則訊息失敗: {e}')
            return False

    async def send_push_message(self, department_code: str, user_id: str, message: str):
        creds = self.department_creds.get(department_code)
        if not creds:
            return
        token, _ = creds
        
        try:
            configuration = Configuration(access_token=token)
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.push_message(
                    PushMessageRequest(
                        to=user_id,
                        messages=[TextMessage(text=message, quick_reply=self._get_quick_reply())]
                    )
                )
        except ApiException as e:
            print(f'推送訊息失敗: {e}')

    async def broadcast_to_department(self, department_code: str, message: str) -> bool:
        creds = self.department_creds.get(department_code)
        if not creds:
            self.last_errors[department_code] = 'Bot not initialized'
            return False
        token, _ = creds
        
        try:
            configuration = Configuration(access_token=token)
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.broadcast(
                    BroadcastRequest(
                        messages=[TextMessage(text=message, quick_reply=self._get_quick_reply())]
                    )
                )
            self.last_errors.pop(department_code, None)
            return True
        except ApiException as e:
            self.last_errors[department_code] = str(e)
            print(f'廣播訊息失敗: {e}')
            return False

    async def broadcast_flex_to_department(self, department_code: str, alt_text: str, flex_contents: dict) -> bool:
        creds = self.department_creds.get(department_code)
        if not creds:
            return False
        token, _ = creds
        
        try:
            container = FlexContainer.from_dict(flex_contents)
            configuration = Configuration(access_token=token)
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.broadcast(
                    BroadcastRequest(
                        messages=[FlexMessage(alt_text=alt_text, contents=container, quick_reply=self._get_quick_reply())]
                    )
                )
            return True
        except ApiException as e:
            print(f'廣播 Flex 訊息失敗: {e}')
            return False

    async def reply_flex(self, department_code: str, reply_token: str, alt_text: str, flex_contents: dict) -> bool:
        creds = self.department_creds.get(department_code)
        if not creds:
            return False
        token, _ = creds
        
        try:
            container = FlexContainer.from_dict(flex_contents)
            configuration = Configuration(access_token=token)
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[FlexMessage(alt_text=alt_text, contents=container, quick_reply=self._get_quick_reply())]
                    )
                )
            return True
        except ApiException as e:
            print(f'回覆 Flex 訊息失敗: {e}')
            return False

    # ---------------------- 任務查詢與更新 ----------------------
    def _parse_priority(self, message: str) -> TaskPriority:
        lower = message.lower()
        if any(k in lower for k in ['緊急', 'urgent', '立即', '馬上']):
            return TaskPriority.URGENT
        if any(k in lower for k in ['重要', 'high', '優先']):
            return TaskPriority.HIGH
        if any(k in lower for k in ['低', 'low', '不急']):
            return TaskPriority.LOW
        return TaskPriority.MEDIUM

    def _extract_title(self, message: str, max_length: int = 50) -> str:
        title = (message.split('\n')[0]).strip()
        if len(title) > max_length:
            title = title[:max_length] + '...'
        return title or '新任務'

    async def get_department_tasks(self, department_code: str, status: Optional[TaskStatus] = None, limit: int = 100) -> List[Task]:
        from app.core.database import SessionLocal
        from app.models.task import Task
        
        db = SessionLocal()
        try:
            query = db.query(Task).filter(Task.department == department_code)
            if status:
                query = query.filter(Task.status == (status.value if hasattr(status, 'value') else status))
            return query.order_by(Task.created_at.desc()).limit(limit).all()
        finally:
            db.close()

    async def update_task_status(self, task_id: str, status: TaskStatus, notes: Optional[str] = None):
        """更新任務狀態，若一般任務不存在則嘗試更新感動任務"""
        from app.core.database import SessionLocal
        from app.models.task import Task
        from app.models.emotional_task import EmotionalTask
        
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.task_uid == task_id).first()
            if not task and task_id.isdigit():
                task = db.query(Task).filter(Task.id == int(task_id)).first()
            
            if task:
                task.status = status.value if hasattr(status, 'value') else str(status)
                if status == TaskStatus.COMPLETED:
                    task.completed_at = datetime.utcnow()
                db.commit()
                db.refresh(task)
                return (task, 'task')

            emo = db.query(EmotionalTask).filter(EmotionalTask.task_id == task_id).first()
            if emo:
                emo.status = status.value if hasattr(status, 'value') else str(status)
                if status == TaskStatus.COMPLETED:
                    emo.completed_at = datetime.utcnow()
                db.commit()
                db.refresh(emo)
                return (emo, 'emotional')

            return None
        except Exception as e:
            print(f'[Error] MySQL 更新失敗: {e}')
            return None
        finally:
            db.close()

    async def send_task_flex_card(self, department_code: str, user_id: Optional[str], task: Task, use_push: bool = True) -> bool:
        creds = self.department_creds.get(department_code)
        if not creds:
            return False
        token, _ = creds
        
        try:
            flex_content = self.create_task_flex_card(task)
            container = FlexContainer.from_dict(flex_content)
            message = FlexMessage(alt_text=f'任務: {task.title}', contents=container)
            
            configuration = Configuration(access_token=token)
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                if use_push and user_id:
                    line_bot_api.push_message(
                        PushMessageRequest(to=user_id, messages=[message])
                    )
                else:
                    line_bot_api.broadcast(
                        BroadcastRequest(messages=[message])
                    )
            return True
        except ApiException as e:
            print(f'發送 Flex 卡片失敗: {e}')
            return False

    async def send_task_flex_reply(self, department_code: str, reply_token: str, task: Task) -> bool:
        creds = self.department_creds.get(department_code)
        if not creds:
            return False
        token, _ = creds
        
        flex_content = self.create_task_flex_card(task)
        
        try:
            container = FlexContainer.from_dict(flex_content)
            configuration = Configuration(access_token=token)
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[FlexMessage(alt_text=f'任務: {task.title}', contents=container, quick_reply=self._get_quick_reply())]
                    )
                )
            return True
        except ApiException as e:
            if 'Invalid reply token' in str(e):
                print(f'[Warning] 測試模式: 忽略無效的 Reply Token 錯誤。')
                return True
            print(f'回覆 Flex 卡片失敗: {e}')
            return False

    # ---------------------- 報告相關 ----------------------
    async def record_report_answer(self, task_id: Optional[str], step: int, answer: Optional[str]) -> None:
        if not task_id:
            return
            
        from app.core.database import SessionLocal
        from app.models.task import Task, TaskReport
        
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.task_uid == task_id).first()
            if not task and task_id.isdigit():
                task = db.query(Task).filter(Task.id == int(task_id)).first()
                if task:
                    task_id = task.task_uid
            
            if not task:
                return
            
            new_report = TaskReport(
                task_id=task_id,
                step=step,
                answer=answer
            )
            db.add(new_report)
            db.commit()
        except Exception as e:
            print(f'[report] 寫入回報答案失敗 task_id={task_id}: {e}')
        finally:
            db.close()

    async def get_task_statistics(self, department_code: str) -> dict:
        from app.core.database import SessionLocal
        from app.models.task import Task, TaskStatus
        from app.models.emotional_task import EmotionalTask
        
        db = SessionLocal()
        try:
            # 部門代碼對照表 (Dashboard Code -> Task Table Value)
            dept_mapping = {
                'GS': 'front_office',
                'HK': 'housekeeping',
                'CON': 'concierge',
                'FB': 'fb',
                'FS': 'florist',
                'LUR': 'laundry',
                'GAE': 'engineering',
                'LA': 'recreation',
                'BP': 'bakery',
                'CBS': 'banquet',
                'BB': 'bar',
                'AD': 'art_design'
            }
            query_dept = dept_mapping.get(department_code, department_code)

            # 1. 一般任務 (General Tasks)
            gen_query = db.query(Task).filter(Task.department == query_dept)
            gen_total = gen_query.count()
            gen_pending = gen_query.filter(Task.status == TaskStatus.PENDING.value).count()
            gen_in_progress = gen_query.filter(Task.status == TaskStatus.IN_PROGRESS.value).count()
            gen_completed = gen_query.filter(Task.status == TaskStatus.COMPLETED.value).count()

            general_stats = {
                'total': gen_total,
                'pending': gen_pending,
                'in_progress': gen_in_progress,
                'completed': gen_completed
            }

            # 2. 感動派工任務 (Emotional Tasks)
            emo_query = db.query(EmotionalTask).filter(EmotionalTask.dept_code == department_code)
            emo_total = emo_query.count()
            emo_pending = emo_query.filter(EmotionalTask.status.in_(['pending', 'assigned'])).count()
            emo_in_progress = emo_query.filter(EmotionalTask.status == 'in_progress').count()
            emo_completed = emo_query.filter(EmotionalTask.status == 'completed').count()

            emotional_stats = {
                'total': emo_total,
                'pending': emo_pending,
                'in_progress': emo_in_progress,
                'completed': emo_completed
            }
            
            return {
                'general': general_stats,
                'emotional': emotional_stats
            }
        except Exception as e:
            print(f"Error getting stats for {department_code}: {e}")
            empty_stats = {'total': 0, 'pending': 0, 'in_progress': 0, 'completed': 0}
            return {'general': empty_stats, 'emotional': empty_stats}
        finally:
            db.close()

    def get_last_error(self, department_code: str) -> Optional[str]:
        return self.last_errors.get(department_code)

    # ---------------------- Flex 產生 ----------------------
    def create_task_flex_card(self, task: Task) -> dict:
        def safe_text(value: str, default: str = '-') -> str:
            return str(value) if value and str(value).strip() else default

        def map_priority(p) -> str:
            val = p.value if hasattr(p, 'value') else str(p).lower()
            if val in ['urgent', 'p']: return 'P'
            if val in ['high', 'e']: return 'E'
            return 'F'

        def map_status(s) -> str:
            val = s.value if hasattr(s, 'value') else str(s).lower()
            if val in ['in_progress', 'progress']: return 'PROGRESS'
            if val in ['completed', 'done']: return 'DONE'
            return 'PENDING'

        dept = safe_text(task.department)
        priority = map_priority(task.priority)
        room = safe_text(task.location, 'Room N/A')
        title = safe_text(task.title, '未命名任務')
        content = safe_text(task.description, '')
        time_text = task.due_at.strftime('%H:%M') if hasattr(task, 'due_at') and task.due_at else '-'
        status_code = map_status(task.status)

        return create_hotel_task_card(
            dept=dept,
            priority=priority,
            room=room,
            guest='Guest',
            title=title,
            content=content,
            time=time_text,
            remark='',
            status=status_code,
            task_id=str(task.task_uid) if hasattr(task, 'task_uid') else str(task.id),
        )

linebot_service = LineBotService()
