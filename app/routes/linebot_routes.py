from fastapi import APIRouter, Request, Header, Query, HTTPException
from typing import Optional
import time

from app.controllers.linebot_controller import linebot_controller
from app.services.linebot_service import linebot_service
from templates.pull_task_linebot import hotel_task_scenarios
from templates.pull_task_linebot import scenario_seed_data
from templates.pull_task_linebot.report_templates import create_report_flow_card
from templates.pull_task_linebot.flex_templates import create_hotel_task_card


router = APIRouter(prefix="/api/linebot", tags=["LINE Bot"])


@router.post("/webhook")
async def webhook_unified(
    request: Request,
    x_line_signature: str = Header(None, alias="X-Line-Signature")
):
    """
    統一 LINE Bot Webhook 端點 (推薦使用)
    
    所有部門共享此 URL: https://你的域名/api/linebot/webhook
    系統會自動根據 X-Line-Signature 識別是哪個部門的請求
    
    在 LINE Developers 中，每個部門頻道的 Webhook URL 應設為：
    https://ace.89.com.tw/api/linebot/webhook
    
    ⚠️ 重要：此端點必須始終返回 200 OK，以防止 LINE 禁用 Webhook
    """
    import json
    from linebot.exceptions import InvalidSignatureError
    from app.models.department import Department
    
    body = await request.body()
    body_str = body.decode('utf-8')
    
    print(f"\n[Webhook] 收到統一端點請求，簽名: {x_line_signature[:20] if x_line_signature else 'None'}...")
    
    # 檢查是否為空請求（LINE 驗證或健康檢查）
    if not body_str:
        print("[Webhook] [OK] 空請求（可能是驗證請求），返回 200")
        return {"status": "ok"}
    
    # 嘗試找到匹配的部門
    # 系統會逐一檢查每個部門的 Secret，找到簽名匹配的部門
    departments = await Department.find({"is_active": True}).to_list()
    
    matched_dept = None
    for dept in departments:
        handler = linebot_service.get_webhook_handler(dept.code)
        if handler is None:
            continue
        
        try:
            # 嘗試驗證此部門的簽名
            handler.handle(body_str, x_line_signature)
            matched_dept = dept
            print(f"[Webhook] [OK] 簽名匹配部門: {dept.code} ({dept.name})")
            break
        except InvalidSignatureError:
            # 簽名不匹配，繼續檢查下一個部門
            print(f"[Webhook] 簽名不匹配: {dept.code}，繼續檢查...")
            continue
        except Exception as e:
            # 其他異常
            print(f"[Webhook] 部門 {dept.code} 驗證異常: {str(e)}")
            continue
    
    if not matched_dept:
        # ⚠️ 重要：即使找不到匹配部門，也要返回 200 OK
        # 否則 LINE 會禁用此 Webhook
        print(f"[Webhook] [WARN] 找不到匹配的部門，簽名: {x_line_signature[:20] if x_line_signature else 'None'}")
        print("[Webhook] [OK] 返回 200 OK（防止 LINE 禁用 Webhook）")
        return {"status": "ok"}
    
    # 找到匹配的部門，處理事件
    try:
        events_data = json.loads(body_str)
        event_count = len(events_data.get('events', []))
        print(f"[Webhook] 將處理 {event_count} 個事件，部門: {matched_dept.code}")
        
        for event in events_data.get('events', []):
            await linebot_controller._process_event(matched_dept.code, event)
            
        print(f"[Webhook] [OK] 部門 {matched_dept.code} 事件處理完成")
    except Exception as e:
        print(f"[Webhook] [ERROR] 事件處理失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        # ⚠️ 即使處理失敗，仍返回 200 OK
        # 目的：防止 LINE 禁用 Webhook，並記錄錯誤供診斷
    
    # 始終返回 200 OK（LINE Webhook 要求）
    return {"status": "ok"}


@router.post("/webhook/{department_code}")
async def webhook(
    department_code: str,
    request: Request,
    x_line_signature: str = Header(None, alias="X-Line-Signature")
):
    """
    LINE Bot Webhook 端點
    
    每個部門都有獨立的 webhook URL:
    - GS (客務部): /api/linebot/webhook/GS
    - HK (房務部): /api/linebot/webhook/HK
    - CON (門房諮詢): /api/linebot/webhook/CON
    - BP (烘焙點心房): /api/linebot/webhook/BP
    - FB (餐飲): /api/linebot/webhook/FB
    - CBS (會議宴會): /api/linebot/webhook/CBS
    - FS (花房): /api/linebot/webhook/FS
    - LUR (洗衣房與制服室): /api/linebot/webhook/LUR
    - GAE (總務工程): /api/linebot/webhook/GAE
    - BB (飲料酒吧): /api/linebot/webhook/BB
    - AD (美術設計): /api/linebot/webhook/AD
    - LA (休閒活動部): /api/linebot/webhook/LA
    """
    return await linebot_controller.handle_webhook(
        department_code=department_code.upper(),
        request=request,
        x_line_signature=x_line_signature
    )


@router.get("/departments/{department_code}")
async def get_department_info(department_code: str):
    """取得部門資訊和統計資料"""
    return await linebot_controller.get_department_info(department_code.upper())


@router.get("/departments/{department_code}/tasks")
async def get_department_tasks(
    department_code: str,
    status: Optional[str] = Query(None, description="任務狀態: pending, in_progress, completed, cancelled"),
    limit: int = Query(50, ge=1, le=200, description="返回數量限制")
):
    """取得部門任務列表"""
    return await linebot_controller.get_department_tasks(
        department_code=department_code.upper(),
        status=status,
        limit=limit
    )


@router.put("/tasks/{task_id}/status")
async def update_task_status(
    task_id: str,
    status: str = Query(..., description="任務狀態: pending, in_progress, completed, cancelled"),
    notes: Optional[str] = Query(None, description="備註")
):
    """更新任務狀態"""
    return await linebot_controller.update_task(
        task_id=task_id,
        status=status,
        notes=notes
    )


@router.post("/departments/{department_code}/broadcast")
async def broadcast_message(
    department_code: str,
    message: str = Query(..., description="要廣播的訊息")
):
    """向部門所有成員廣播訊息"""
    return await linebot_controller.broadcast_message(
        department_code=department_code.upper(),
        message=message
    )


@router.post("/demo/all/tasks")
async def send_demo_all_departments_tasks():
    """測試用：一次廣播 12 部門各自任務卡 (從 MySQL 資料庫)"""
    try:
        departments = ["GS", "HK", "CON", "BP", "FB", "CBS", "FS", "LUR", "GAE", "BB", "AD", "LA"]
        
        results = []
        for dept in departments:
            try:
                # 從 MySQL 取得任務
                bubbles = linebot_service.get_tasks_for_department(dept)
                
                if not bubbles:
                    results.append({
                        "department": dept,
                        "count": 0,
                        "sent": False,
                        "reason": "No tasks found in DB"
                    })
                    continue

                carousel = {"type": "carousel", "contents": bubbles}
                ok = await linebot_service.broadcast_flex_to_department(dept, alt_text=f"{dept} 測試任務", flex_contents=carousel)
                error_msg = linebot_service.get_last_error(dept) if not ok else ""
                results.append({
                    "department": dept,
                    "count": len(bubbles),
                    "sent": ok,
                    "reason": error_msg or ("" if ok else "未知錯誤")
                })
            except Exception as e:
                results.append({
                    "department": dept,
                    "count": 0,
                    "sent": False,
                    "reason": str(e)
                })

        return {"status": "success", "broadcasted": results}
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }


@router.post("/demo/seed_tasks")
async def seed_tasks_to_db():
    """將範本任務寫入資料庫，避免每次廣播都用靜態卡片"""
    from app.models.task import Task, TaskStatus, TaskPriority

    inserted = 0
    skipped = 0
    errors = []

    for entry in scenario_seed_data.SEED_TASKS:
        try:
            exists = await Task.find_one({
                "department_code": entry["department_code"],
                "title": entry["title"]
            })
            if exists:
                skipped += 1
                continue

            task = Task(
                department_code=entry["department_code"],
                department_name=entry["department_name"],
                line_user_id="demo-seed",
                line_user_name="Demo Seed",
                title=entry["title"],
                description=entry["content"],
                status=TaskStatus(scenario_seed_data.map_status(entry["status"])),
                priority=TaskPriority(scenario_seed_data.map_priority(entry["priority_code"])),
                notes=f"[SEED] 時間:{entry['time']} | 備註:{entry['remark']}",
                tags=["demo", "seed"]
            )

            await task.insert()
            inserted += 1
        except Exception as e:
            errors.append({"entry": entry.get("title"), "error": str(e)})

    return {
        "status": "success",
        "inserted": inserted,
        "skipped": skipped,
        "errors": errors
    }


@router.post("/demo/{department_code}/task")
async def send_demo_single_task(
    department_code: str,
    index: int = Query(1, ge=1, description="示範卡片索引（從 1 開始）")
):
    """測試用：廣播指定部門的一張示範任務卡到 LINE (從 MySQL 資料庫)。
    可用 query 參數 index 指定要發送的示範卡片。
    """
    dept = department_code.upper()

    # 從 MySQL 取得任務
    bubbles = linebot_service.get_tasks_for_department(dept)
    
    if not bubbles:
        return {"status": "error", "message": f"部門 {dept} 無任務資料"}

    if index > len(bubbles):
        return {"status": "error", "message": f"索引 {index} 超出範圍 (共有 {len(bubbles)} 個任務)"}

    bubble = bubbles[index - 1]

    ok = await linebot_service.broadcast_flex_to_department(
        dept, 
        alt_text=f"{dept} 測試任務 {index}", 
        flex_contents=bubble
    )
    
    if ok:
        return {"status": "success", "message": f"已發送 {dept} 任務 {index}"}
    else:
        error_msg = linebot_service.get_last_error(dept)
        return {"status": "error", "message": error_msg or "發送失敗"}

@router.post("/demo/{department_code}/tasks")
async def send_demo_tasks(department_code: str):
    """測試用：廣播 12 部門各自的 2 張任務卡到 LINE (Carousel)"""
    dept = department_code.upper()

    # 依照部門挑選兩張範例卡片
    mapping = {
        "GS": [hotel_task_scenarios.task_gs_1, hotel_task_scenarios.task_gs_2],
        "HK": [hotel_task_scenarios.task_hk_1, hotel_task_scenarios.task_hk_2],
        "CON": [hotel_task_scenarios.task_con_1, hotel_task_scenarios.task_con_2],
        "BP": [hotel_task_scenarios.task_bp_1, hotel_task_scenarios.task_bp_2],
        "FB": [hotel_task_scenarios.task_fb_1, hotel_task_scenarios.task_fb_2],
        "CBS": [hotel_task_scenarios.task_cbs_1, hotel_task_scenarios.task_cbs_2],
        "FS": [hotel_task_scenarios.task_fs_1, hotel_task_scenarios.task_fs_2],
        "LUR": [hotel_task_scenarios.task_lur_1, hotel_task_scenarios.task_lur_2],
        "GAE": [hotel_task_scenarios.task_gae_1, hotel_task_scenarios.task_gae_2],
        "BB": [hotel_task_scenarios.task_bb_1, hotel_task_scenarios.task_bb_2],
        "AD": [hotel_task_scenarios.task_ad_1, hotel_task_scenarios.task_ad_2],
        "LA": [hotel_task_scenarios.task_la_1, hotel_task_scenarios.task_la_2],
    }

    tasks = mapping.get(dept)
    if not tasks:
        return {"status": "error", "message": "未知部門代碼"}

    carousel = {"type": "carousel", "contents": tasks}
    await linebot_service.broadcast_flex_to_department(dept, alt_text=f"{dept} 測試任務", flex_contents=carousel)
    return {"status": "success", "message": f"已廣播 {dept} 2 張任務卡"}


@router.post("/demo/{department_code}/report")
async def send_demo_report_flow(department_code: str, step: int = Query(1, ge=1, le=5)):
    """測試用：廣播任務回報流程卡片 (Step 1~5)"""
    dept = department_code.upper()
    bubble = create_report_flow_card(step=step, dept=f"{dept} 部門", room="Room 000", task_id="DEMO-TASK")
    await linebot_service.broadcast_flex_to_department(dept, alt_text=f"任務回報 ({step}/5)", flex_contents=bubble)
    return {"status": "success", "message": f"{dept} 已廣播回報卡 Step {step}"}




@router.post("/departments/{department_code}/flex_tasks")
async def broadcast_department_flex_tasks(
    department_code: str,
    status: Optional[str] = Query(None, description="任務狀態: pending|in_progress|completed|cancelled"),
    limit: int = Query(10, ge=1, le=30)
):
    """從資料庫取得部門任務，轉為 Flex 卡片（carousel）後廣播"""
    dept = department_code.upper()
    from app.models.task import TaskStatus, TaskPriority

    task_status = None
    if status:
        try:
            task_status = TaskStatus(status)
        except ValueError:
            return {"status": "error", "message": "無效的狀態值"}

    tasks = await linebot_service.get_department_tasks(dept, task_status, limit)

    def safe_text(value: str, default: str = "-") -> str:
        return value if value and str(value).strip() else default

    def map_priority(p: TaskPriority) -> str:
        return "P" if p == TaskPriority.URGENT else ("E" if p == TaskPriority.HIGH else "F")

    bubbles = []
    for t in tasks:
        bubbles.append(create_hotel_task_card(
            dept=t.department_name,
            priority=map_priority(t.priority),
            room=safe_text("Room N/A"),
            guest=safe_text(t.line_user_name or "Guest"),
            title=safe_text(t.title or "未命名任務"),
            content=safe_text(t.description or ""),
            time=safe_text(t.due_date.isoformat() if t.due_date else ""),
            remark=safe_text(t.notes or ""),
            status="PROGRESS" if t.status == TaskStatus.IN_PROGRESS else ("PENDING" if t.status == TaskStatus.PENDING else "PROGRESS"),
            task_id=str(t.id)
        ))

    if not bubbles:
        return {"status": "success", "message": "無任務可廣播"}

    carousel = {"type": "carousel", "contents": bubbles}
    await linebot_service.broadcast_flex_to_department(dept, alt_text=f"{dept} 任務清單", flex_contents=carousel)
    return {"status": "success", "total": len(bubbles)}


@router.post("/departments/flex_tasks/all")
async def broadcast_all_departments_flex_tasks(
    status: Optional[str] = Query(None, description="任務狀態: pending|in_progress|completed|cancelled"),
    limit: int = Query(10, ge=1, le=30)
):
    """批次：對所有啟用部門抓取資料庫任務，轉 Flex 後逐部門廣播"""
    try:
        from app.models.department import Department
        from app.models.task import TaskStatus, TaskPriority

        task_status = None
        if status:
            try:
                task_status = TaskStatus(status)
            except ValueError:
                return {"status": "error", "message": "無效的狀態值"}

        departments = await Department.find({"is_active": True}).to_list()
        results = []

        def safe_text(value: str, default: str = "-") -> str:
            return value if value and str(value).strip() else default

        def map_priority(p: TaskPriority) -> str:
            return "P" if p == TaskPriority.URGENT else ("E" if p == TaskPriority.HIGH else "F")

        for dept in departments:
            try:
                tasks = await linebot_service.get_department_tasks(dept.code, task_status, limit)
                bubbles = []
                for t in tasks:
                    bubbles.append(create_hotel_task_card(
                        dept=t.department_name,
                        priority=map_priority(t.priority),
                        room=safe_text("Room N/A"),
                        guest=safe_text(t.line_user_name or "Guest"),
                        title=safe_text(t.title or "未命名任務"),
                        content=safe_text(t.description or ""),
                        time=safe_text(t.due_date.isoformat() if t.due_date else ""),
                        remark=safe_text(t.notes or ""),
                        status="PROGRESS" if t.status == TaskStatus.IN_PROGRESS else ("PENDING" if t.status == TaskStatus.PENDING else "PROGRESS"),
                        task_id=str(t.id)
                    ))

                sent = False
                reason = ""
                if bubbles:
                    carousel = {"type": "carousel", "contents": bubbles}
                    sent = await linebot_service.broadcast_flex_to_department(dept.code, alt_text=f"{dept.code} 任務清單", flex_contents=carousel)
                    if not sent:
                        reason = linebot_service.get_last_error(dept.code) or "未知錯誤"
                else:
                    reason = "無任務可廣播"
                
                results.append({
                    "department": dept.code,
                    "total": len(bubbles),
                    "sent": sent,
                    "reason": reason
                })
            except Exception as e:
                results.append({
                    "department": dept.code,
                    "total": 0,
                    "sent": False,
                    "reason": str(e)
                })

        return {"status": "success", "broadcasted": results}
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }


@router.get("/diagnostics")
async def diagnostics():
    """列出部門初始化與可用狀態，並提供快速文字廣播測試說明"""
    from app.models.department import Department
    departments = await Department.find({"is_active": True}).to_list()
    items = []
    for d in departments:
        bot_api = linebot_service.get_bot_api(d.code)
        items.append({
            "code": d.code,
            "name": d.name,
            "initialized": bool(bot_api),
        })
    return {"status": "success", "departments": items}


@router.post("/demo/{department_code}/ping")
async def ping_department(department_code: str, text: str = Query("Ping from API")):
    """對指定部門廣播一則純文字，驗證 Token/Secret 與廣播可用性"""
    dept = department_code.upper()
    ok = await linebot_service.broadcast_to_department(dept, text)
    if ok:
        return {"status": "success", "message": "已廣播"}
    else:
        error_detail = linebot_service.get_last_error(dept) or "未知錯誤"
        return {"status": "error", "message": f"廣播失敗: {error_detail}"}


@router.get("/departments")
async def list_all_departments():
    """列出所有部門"""
    from app.models.department import Department
    
    departments = await Department.find_all().to_list()
    return {
        "total": len(departments),
        "departments": [
            {
                "code": dept.code,
                "name": dept.name,
                "is_active": dept.is_active,
                "description": dept.description
            }
            for dept in departments
        ]
    }


@router.post("/test/postback/{department_code}")
async def test_postback(department_code: str, data: str = Query(..., description="Postback data string (e.g., action=task&op=accept&id=123&dept=HK&room=101)")):
    """測試用：模擬 postback 事件，觀看控制台輸出"""
    dept = department_code.upper()
    event = {
        "type": "postback",
        "postback": {
            "data": data
        },
        "replyToken": "test_reply_token"
    }
    await linebot_controller._handle_postback_event(dept, event)
    return {"status": "success", "message": "已模擬 postback 事件，請檢查控制台輸出"}


@router.get("/webhook/verify")
async def verify_webhook():
    """
    驗證 Webhook 配置是否正確
    
    在 LINE Developers 中，你應該看到此端點返回 200 OK
    """
    return {
        "status": "ok",
        "message": "Webhook 已配置並正常運行",
        "webhook_url": "https://ace.89.com.tw/api/linebot/webhook",
        "note": "所有部門應該共享此單一 Webhook URL"
    }


@router.get("/tasks/{task_id}/flex")
async def get_task_flex_card(task_id: str):
    """
    查詢指定任務並回傳 Flex Message 任務卡結構 (JSON)
    
    用法: GET /api/linebot/tasks/{task_id}/flex
    回傳: Flex Message bubble 結構，可直接用於 LINE Bot 發送
    """
    from beanie import PydanticObjectId
    from app.models.task import Task
    
    try:
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            raise HTTPException(status_code=404, detail=f"找不到任務 {task_id}")
        
        # 產生 Flex Message 結構
        flex_content = linebot_service.create_task_flex_card(task)
        
        return {
            "status": "success",
            "task_id": str(task.id),
            "task_title": task.title,
            "task_status": task.status.value,
            "flex_message": {
                "type": "flex",
                "altText": f"任務: {task.title}",
                "contents": flex_content
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢任務失敗: {str(e)}")


@router.get("/departments/{department_code}/tasks/{task_id}/flex")
async def get_department_task_flex(department_code: str, task_id: str):
    """
    查詢指定部門的指定任務，並回傳 Flex Message 卡片
    
    用法: GET /api/linebot/departments/GS/tasks/{task_id}/flex
    """
    from beanie import PydanticObjectId
    from app.models.task import Task
    
    try:
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            raise HTTPException(status_code=404, detail=f"找不到任務 {task_id}")
        
        if task.department_code.upper() != department_code.upper():
            raise HTTPException(status_code=400, detail=f"任務不屬於部門 {department_code}")
        
        flex_content = linebot_service.create_task_flex_card(task)
        
        return {
            "status": "success",
            "department": department_code,
            "task_id": str(task.id),
            "task_title": task.title,
            "task_status": task.status.value,
            "flex_message": flex_content
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢任務失敗: {str(e)}")


@router.get("/departments/{department_code}/pending-tasks/flex")
async def get_pending_tasks_flex(department_code: str, limit: int = Query(10, ge=1, le=100)):
    """
    查詢部門所有待處理任務，回傳 Flex Carousel (多張卡片)
    
    用法: GET /api/linebot/departments/GS/pending-tasks/flex?limit=5
    回傳: Flex Carousel 結構，包含最多 N 張任務卡片
    """
    from app.models.task import Task, TaskStatus
    from app.models.department import Department
    
    try:
        # 驗證部門存在
        dept = await Department.find_one({"code": department_code.upper()})
        if not dept:
            raise HTTPException(status_code=404, detail=f"部門 {department_code} 不存在")
        
        # 查詢待處理任務
        tasks = await Task.find({
            "department_code": department_code.upper(),
            "status": TaskStatus.PENDING
        }).sort("-created_at").limit(limit).to_list()
        
        if not tasks:
            return {
                "status": "success",
                "department": department_code,
                "total": 0,
                "message": "沒有待處理任務",
                "flex_message": None
            }
        
        # 產生多張卡片（Carousel）
        bubbles = [linebot_service.create_task_flex_card(task) for task in tasks]
        
        # 如果只有一張，回傳單個 bubble；否則回傳 carousel
        if len(bubbles) == 1:
            flex_content = bubbles[0]
        else:
            flex_content = {
                "type": "carousel",
                "contents": bubbles
            }
        
        return {
            "status": "success",
            "department": department_code,
            "total": len(tasks),
            "flex_message": {
                "type": "flex",
                "altText": f"{dept.name} 待處理任務 ({len(tasks)}件)",
                "contents": flex_content
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢待處理任務失敗: {str(e)}")


@router.post("/departments/{department_code}/send-task-flex")
async def send_task_flex(
    department_code: str,
    task_id: str = Query(..., description="任務 ID"),
    user_id: str = Query(..., description="LINE 使用者 ID")
):
    """
    向指定 LINE 使用者發送任務 Flex Message 卡片 (push)
    
    用法: POST /api/linebot/departments/GS/send-task-flex?task_id=xxx&user_id=Uxxx
    """
    from beanie import PydanticObjectId
    from app.models.task import Task
    
    try:
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            raise HTTPException(status_code=404, detail=f"找不到任務 {task_id}")
        
        if task.department_code.upper() != department_code.upper():
            raise HTTPException(status_code=400, detail=f"任務不屬於部門 {department_code}")
        
        # 發送 Flex Message
        success = await linebot_service.send_task_flex_card(
            department_code.upper(),
            user_id,
            task,
            use_push=True
        )
        
        if success:
            return {
                "status": "success",
                "message": f"已向使用者 {user_id} 發送任務卡片",
                "task_id": str(task.id),
                "task_title": task.title
            }
        else:
            raise HTTPException(status_code=500, detail="發送 Flex Message 失敗")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"發送任務失敗: {str(e)}")


@router.post("/departments/{department_code}/broadcast-task-flex")
async def broadcast_task_flex(
    department_code: str,
    task_id: str = Query(..., description="任務 ID")
):
    """
    向整個部門廣播任務 Flex Message 卡片 (broadcast)
    
    用法: POST /api/linebot/departments/GS/broadcast-task-flex?task_id=xxx
    """
    from beanie import PydanticObjectId
    from app.models.task import Task
    
    try:
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            raise HTTPException(status_code=404, detail=f"找不到任務 {task_id}")
        
        if task.department_code.upper() != department_code.upper():
            raise HTTPException(status_code=400, detail=f"任務不屬於部門 {department_code}")
        
        # 廣播 Flex Message
        success = await linebot_service.send_task_flex_card(
            department_code.upper(),
            None,  # broadcast 不需要使用者 ID
            task,
            use_push=False
        )
        
        if success:
            return {
                "status": "success",
                "message": f"已向部門 {department_code} 廣播任務卡片",
                "task_id": str(task.id),
                "task_title": task.title
            }
        else:
            raise HTTPException(status_code=500, detail="廣播 Flex Message 失敗")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"廣播任務失敗: {str(e)}")
