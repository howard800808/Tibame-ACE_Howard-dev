from fastapi import APIRouter, Request, Header, Query, HTTPException
from typing import Optional
import time
import json
import uuid
from datetime import datetime

from app.controllers.linebot_controller import linebot_controller
from app.services.linebot_service import linebot_service
from app.services import hotel_task_scenarios
from app.services.linebot_service import create_report_flow_card, create_hotel_task_card

from app.core.database import SessionLocal
from app.models.department import Department
from app.models.task import Task, TaskStatus, TaskPriority

router = APIRouter(prefix="/api/linebot", tags=["LINE Bot"])


@router.post("/webhook")
async def webhook_unified(
    request: Request,
    x_line_signature: str = Header(None, alias="X-Line-Signature")
):
    """
    統一 LINE Bot Webhook 端點 (推薦使用)
    
    各部門共享此URL: https://你的網域/api/linebot/webhook
    系統會自動根據 X-Line-Signature 識別是哪個部門。    
    在 LINE Developers 中的每個部門設定此 Webhook URL。
    https://ace.89.com.tw/api/linebot/webhook
    
    注意：此端點必須始終返回 200 OK，以防止 LINE 禁用 Webhook
    """
    body = await request.body()
    body_str = body.decode('utf-8')
    
    signature_prefix = x_line_signature[:15] if x_line_signature else 'None'
    print(f"\n[Webhook] 收到統一端點請求，簽名: {signature_prefix}...")
    
    # 檢查是否為空請求（LINE 驗證或健康檢查）
    if not body_str:
        print("[Webhook] [OK] 空請求（可能是驗證請求），返回 200")
        return {"status": "ok"}
    
    # 嘗試找到對應部門
    # 系統會逐一檢查每個部門的 Secret，找到簽名匹配的那個
    db = SessionLocal()
    try:
        # 不過濾 is_active，因為 DB 中沒有此欄位
        departments = db.query(Department).all()
        # print(f"[Webhook] 從資料庫載入 {len(departments)} 個部門")  # 減少日誌
    finally:
        db.close()
        
    matched_dept = None

    for dept in departments:
        # 使用 v3 驗證簽名
        if linebot_service.validate_signature(dept.code, body_str, x_line_signature):
            matched_dept = dept
            print(f"[Webhook] ✅ 簽名匹配成功: {dept.code} ({dept.name_zh})")
            break
    
    if not matched_dept:
        # 重要：即使找不到對應部門，也要返回 200 OK
        # 否則 LINE 會禁用此 Webhook
        print(f"[Webhook] [WARN] 無法匹配部門，簽名: {x_line_signature[:20] if x_line_signature else 'None'}")
        print("[Webhook] [OK] 返回 200 OK（防止 LINE 禁用 Webhook）")
        return {"status": "ok"}
    
    # 找到對應部門，處理事件
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
        # 注意：即使處理失敗，仍返回 200 OK
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
    LINE Bot Webhook 端點 (單一部門)
    
    每個部門專屬的 webhook URL:
    - GS (客務部): /api/linebot/webhook/GS
    - HK (房務部): /api/linebot/webhook/HK
    - CON (禮賓司): /api/linebot/webhook/CON
    - BP (行李部): /api/linebot/webhook/BP
    - FB (餐飲): /api/linebot/webhook/FB
    - CBS (會議宴會): /api/linebot/webhook/CBS
    - FS (廚房): /api/linebot/webhook/FS
    - LUR (洗衣房/制服): /api/linebot/webhook/LUR
    - GAE (總務/工程): /api/linebot/webhook/GAE
    - BB (飲料/酒吧): /api/linebot/webhook/BB
    - AD (美工設計): /api/linebot/webhook/AD
    - LA (休閒活動): /api/linebot/webhook/LA
    """
    return await linebot_controller.handle_webhook(
        department_code=department_code.upper(),
        request=request,
        x_line_signature=x_line_signature
    )


@router.get("/departments/{department_code}")
async def get_department_info(department_code: str):
    """獲取部門資訊與統計數據"""
    return await linebot_controller.get_department_info(department_code.upper())


@router.get("/departments/{department_code}/tasks")
async def get_department_tasks(
    department_code: str,
    status: Optional[str] = Query(None, description="任務狀態: pending, in_progress, completed, cancelled"),
    limit: int = Query(50, ge=1, le=200, description="返回數量限制")
):
    """獲取部門任務列表"""
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
    """向部門全員廣播訊息"""
    return await linebot_controller.broadcast_message(
        department_code=department_code.upper(),
        message=message
    )


@router.post("/demo/all/tasks")
async def send_demo_all_departments_tasks():
    """測試：向一次廣播 12 個部門各自的任務卡 (從 MySQL 資料)"""
    try:
        departments = ["GS", "HK", "CON", "BP", "FB", "CBS", "FS", "LUR", "GAE", "BB", "AD", "LA"]
        
        results = []
        for dept in departments:
            try:
                # 從 MySQL 獲取任務
                bubbles = await linebot_service.get_tasks_for_department(dept)
                
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
    """將種子任務寫入資料庫，避免每次廣播都沒資料卡住"""
    
    db = SessionLocal()
    inserted = 0
    skipped = 0
    errors = []

    try:
        # for entry in scenario_seed_data.SEED_TASKS:
        #     try:
        #         # 檢查是否存在 (根據部門和標題)
        #         exists = db.query(Task).filter(
        #             Task.department == entry["department_code"],
        #             Task.title == entry["title"]
        #         ).first()
                
        #         if exists:
        #             skipped += 1
        #             continue

        #         # 映射狀態與優先級
        #         status_val = scenario_seed_data.map_status(entry["status"])
        #         priority_val = scenario_seed_data.map_priority(entry["priority_code"])
                
        #         # 建立新任務
        #         task = Task(
        #             task_uid=str(uuid.uuid4()),
        #             department=entry["department_code"],
        #             # department_name=entry["department_name"], # SQL Model 無此欄位
        #             # line_user_id="demo-seed", # SQL Model 無此欄位
        #             # line_user_name="Demo Seed", # SQL Model 無此欄位
        #             title=entry["title"],
        #             description=f"{entry['content']}\n\n[SEED] 時間:{entry['time']} | 備註:{entry['remark']}",
        #             status=status_val,
        #             priority=priority_val,
        #             # notes=..., # SQL Model 無此欄位，已合併至 description
        #             # tags=["demo", "seed"] # SQL Model 無此欄位
        #             created_at=datetime.now(),
        #             updated_at=datetime.now()
        #         )

        #         db.add(task)
        #         inserted += 1
        #     except Exception as e:
        #         errors.append({"entry": entry.get("title"), "error": str(e)})
        
        # db.commit()
        pass
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

    return {
        "status": "success",
        "inserted": inserted,
        "skipped": skipped,
        "errors": errors
    }


@router.post("/demo/{department_code}/task")
async def send_demo_single_task(
    department_code: str,
    index: int = Query(1, ge=1, description="示範卡索引（從 1 開始）")
):
    """測試：向部門發送單張示範任務卡到 LINE (從 MySQL 資料)"""
    dept = department_code.upper()

    # 從 MySQL 獲取任務
    bubbles = linebot_service.get_tasks_for_department(dept)
    
    if not bubbles:
        return {"status": "error", "message": f"部門 {dept} 無任務資料"}

    if index > len(bubbles):
        return {"status": "error", "message": f"索引 {index} 超出範圍 (共有 {len(bubbles)} 筆任務)"}

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
    """測試：向 12 部門自動發 2 張任務卡到 LINE (Carousel)"""
    dept = department_code.upper()

    # 依照部門選擇 2 張範例卡
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
        return {"status": "error", "message": "未知部門"}

    carousel = {"type": "carousel", "contents": tasks}
    await linebot_service.broadcast_flex_to_department(dept, alt_text=f"{dept} 測試任務", flex_contents=carousel)
    return {"status": "success", "message": f"已廣播 {dept} 2 張任務卡"}


@router.post("/demo/{department_code}/report")
async def send_demo_report_flow(department_code: str, step: int = Query(1, ge=1, le=5)):
    """測試：發送任務回報流程卡 (Step 1~5)"""
    dept = department_code.upper()
    bubble = create_report_flow_card(step=step, dept=f"{dept} 測試", room="Room 000", task_id="DEMO-TASK")
    await linebot_service.broadcast_flex_to_department(dept, alt_text=f"任務回報 ({step}/5)", flex_contents=bubble)
    return {"status": "success", "message": f"{dept} 已廣播卡片 Step {step}"}


@router.post("/departments/{department_code}/flex_tasks")
async def broadcast_department_flex_tasks(
    department_code: str,
    status: Optional[str] = Query(None, description="任務狀態: pending|in_progress|completed|cancelled"),
    limit: int = Query(10, ge=1, le=30)
):
    """從資料庫讀取任務，發送 Flex 訊息（carousel）"""
    dept = department_code.upper()

    task_status = None
    if status:
        try:
            task_status = TaskStatus(status)
        except ValueError:
            return {"status": "error", "message": "無效的狀態"}

    # 注意：這裡需要 await
    tasks = await linebot_service.get_department_tasks(dept, task_status, limit)

    def safe_text(value: str, default: str = "-") -> str:
        return value if value and str(value).strip() else default

    def map_priority(p) -> str:
        # 處理 Enum 或字串
        val = p.value if hasattr(p, 'value') else str(p)
        if val in ["urgent", "P"]: return "P"
        if val in ["high", "E"]: return "E"
        return "F"

    bubbles = []
    for t in tasks:
        bubbles.append(create_hotel_task_card(
            dept=t.department, # SQL Model 欄位是 department
            priority=map_priority(t.priority),
            room=safe_text(t.location, "Room N/A"),
            guest="Guest", # SQL Model 無此欄位
            title=safe_text(t.title, "未命名任務"),
            content=safe_text(t.description, ""),
            time=safe_text(t.due_at.isoformat() if t.due_at else ""),
            remark="", # SQL Model 無此欄位
            status="PROGRESS" if t.status == TaskStatus.IN_PROGRESS.value else ("PENDING" if t.status == TaskStatus.PENDING.value else "PROGRESS"),
            task_id=str(t.task_uid)
        ))

    if not bubbles:
        return {"status": "success", "message": "無任務可發送"}

    carousel = {"type": "carousel", "contents": bubbles}
    await linebot_service.broadcast_flex_to_department(dept, alt_text=f"{dept} 任務清單", flex_contents=carousel)
    return {"status": "success", "total": len(bubbles)}


@router.post("/departments/flex_tasks/all")
async def broadcast_all_departments_flex_tasks(
    status: Optional[str] = Query(None, description="任務狀態: pending|in_progress|completed|cancelled"),
    limit: int = Query(10, ge=1, le=30)
):
    """批次：讀取所有部門的資料庫任務並發送 Flex 後逐部門廣播"""
    try:
        task_status = None
        if status:
            try:
                task_status = TaskStatus(status)
            except ValueError:
                return {"status": "error", "message": "無效的狀態"}

        db = SessionLocal()
        try:
            departments = db.query(Department).filter(Department.is_active == True).all()
        finally:
            db.close()
            
        results = []

        def safe_text(value: str, default: str = "-") -> str:
            return value if value and str(value).strip() else default

        def map_priority(p) -> str:
            val = p.value if hasattr(p, 'value') else str(p)
            if val in ["urgent", "P"]: return "P"
            if val in ["high", "E"]: return "E"
            return "F"

        for dept in departments:
            try:
                tasks = await linebot_service.get_department_tasks(dept.code, task_status, limit)
                bubbles = []
                for t in tasks:
                    bubbles.append(create_hotel_task_card(
                        dept=t.department,
                        priority=map_priority(t.priority),
                        room=safe_text(t.location, "Room N/A"),
                        guest="Guest",
                        title=safe_text(t.title, "未命名任務"),
                        content=safe_text(t.description, ""),
                        time=safe_text(t.due_at.isoformat() if t.due_at else ""),
                        remark="",
                        status="PROGRESS" if t.status == TaskStatus.IN_PROGRESS.value else ("PENDING" if t.status == TaskStatus.PENDING.value else "PROGRESS"),
                        task_id=str(t.task_uid)
                    ))

                sent = False
                reason = ""
                if bubbles:
                    carousel = {"type": "carousel", "contents": bubbles}
                    sent = await linebot_service.broadcast_flex_to_department(dept.code, alt_text=f"{dept.code} 任務清單", flex_contents=carousel)
                    if not sent:
                        reason = linebot_service.get_last_error(dept.code) or "未知錯誤"
                else:
                    reason = "無任務可發送"
                
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
    """列出所有部門的 Bot 啟用狀態，並提供快速關鍵字廣播測試說明"""
    
    db = SessionLocal()
    try:
        departments = db.query(Department).filter(Department.is_active == True).all()
    finally:
        db.close()
        
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
    """對指定部門發送一則文字訊息，驗證 Token/Secret 與廣播功能"""
    dept = department_code.upper()
    ok = await linebot_service.broadcast_to_department(dept, text)
    if ok:
        return {"status": "success", "message": "已廣播"}
    else:
        error_detail = linebot_service.get_last_error(dept) or "未知錯誤"
        return {"status": "error", "message": f"發送失敗: {error_detail}"}


@router.get("/departments")
async def list_all_departments():
    """列出所有部門"""
    
    db = SessionLocal()
    try:
        departments = db.query(Department).all()
    finally:
        db.close()
        
    return {
        "total": len(departments),
        "departments": [
            {
                "code": dept.code,
                "name": dept.name,
                "is_active": dept.is_active,
                # "description": dept.description # DB schema 中沒有此欄位
            }
            for dept in departments
        ]
    }


@router.post("/test/postback/{department_code}")
async def test_postback(department_code: str, data: str = Query(..., description="Postback data string (e.g., action=task&op=accept&id=123&dept=HK&room=101)")):
    """測試：模擬 postback 事件，請看控制台輸出"""
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
    驗證 Webhook 設置是否正確
    
    在 LINE Developers 中你應該能讓此端點返回 200 OK
    """
    return {
        "status": "ok",
        "message": "Webhook 已設置並正常運作",
        "webhook_url": "https://ace.89.com.tw/api/linebot/webhook",
        "note": "所有部門應該共享此單一 Webhook URL"
    }


@router.get("/tasks/{task_id}/flex")
async def get_task_flex_card(task_id: str):
    """
    查詢單一任務並返回 Flex Message 任務卡片(JSON)
    
    範例: GET /api/linebot/tasks/{task_id}/flex
    回傳: Flex Message bubble 結構，可直接用於 LINE Bot 發送
    """
    
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.task_uid == task_id).first()
        if not task and task_id.isdigit():
            task = db.query(Task).filter(Task.id == int(task_id)).first()
            
        if not task:
            raise HTTPException(status_code=404, detail=f"找不到任務 {task_id}")
        
        # 這裡需要 department_code 和 user_id，但這個 endpoint 似乎只是預覽
        # 假設是預覽，我們只返回 JSON
        
        flex_content = linebot_service.create_task_flex_card(task)
        
        return {
            "status": "success",
            "task_id": str(task.task_uid),
            "task_title": task.title,
            "flex_message": flex_content
        }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢任務失敗: {str(e)}")
    finally:
        db.close()


@router.get("/departments/{department_code}/tasks/{task_id}/flex")
async def get_department_task_flex(department_code: str, task_id: str):
    """
    查詢部門內指定任務，並返回 Flex Message 結構
    
    範例: GET /api/linebot/departments/GS/tasks/{task_id}/flex
    """
    
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.task_uid == task_id).first()
        if not task and task_id.isdigit():
            task = db.query(Task).filter(Task.id == int(task_id)).first()
            
        if not task:
            raise HTTPException(status_code=404, detail=f"找不到任務 {task_id}")
        
        if task.department.upper() != department_code.upper():
            raise HTTPException(status_code=400, detail=f"任務不屬於部門 {department_code}")
        
        flex_content = linebot_service.create_task_flex_card(task)
        
        return {
            "status": "success",
            "department": department_code,
            "task_id": str(task.task_uid),
            "task_title": task.title,
            "task_status": task.status,
            "flex_message": flex_content
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢任務失敗: {str(e)}")
    finally:
        db.close()


@router.get("/departments/{department_code}/pending-tasks/flex")
async def get_pending_tasks_flex(department_code: str, limit: int = Query(10, ge=1, le=100)):
    """
    查詢部門內所有待處理任務，返回 Flex Carousel (多張卡片)
    
    範例: GET /api/linebot/departments/GS/pending-tasks/flex?limit=5
    回傳: Flex Carousel 結構，包含 N 張任務卡片
    """
    
    db = SessionLocal()
    try:
        # 驗證部門存在
        dept = db.query(Department).filter(Department.code == department_code.upper()).first()
        if not dept:
            raise HTTPException(status_code=404, detail=f"部門 {department_code} 不存在")
        
        # 查詢待處理任務
        tasks = db.query(Task).filter(
            Task.department == department_code.upper(),
            Task.status == TaskStatus.PENDING.value
        ).order_by(Task.created_at.desc()).limit(limit).all()
        
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
        
        # 如果只有一張，傳回 bubble；否則傳回 carousel
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
                "altText": f"{dept.name} 待處理任務 ({len(tasks)})",
                "contents": flex_content
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢任務失敗: {str(e)}")
    finally:
        db.close()


@router.post("/departments/{department_code}/send-task-flex")
async def send_task_flex(
    department_code: str,
    task_id: str = Query(..., description="任務 ID"),
    user_id: str = Query(..., description="LINE 使用者 ID")
):
    """
    向指定 LINE 使用者發送任務 Flex Message 卡片 (push)
    
    範例: POST /api/linebot/departments/GS/send-task-flex?task_id=xxx&user_id=Uxxx
    """
    
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.task_uid == task_id).first()
        if not task and task_id.isdigit():
            task = db.query(Task).filter(Task.id == int(task_id)).first()
            
        if not task:
            raise HTTPException(status_code=404, detail=f"找不到任務 {task_id}")
        
        if task.department.upper() != department_code.upper():
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
                "task_id": str(task.task_uid),
                "task_title": task.title
            }
        else:
            raise HTTPException(status_code=500, detail="發送 Flex Message 失敗")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"發送任務失敗: {str(e)}")
    finally:
        db.close()


@router.post("/departments/{department_code}/broadcast-task-flex")
async def broadcast_task_flex(
    department_code: str,
    task_id: str = Query(..., description="任務 ID")
):
    """
    向整個部門廣播任務 Flex Message 卡片 (broadcast)
    
    範例: POST /api/linebot/departments/GS/broadcast-task-flex?task_id=xxx
    """
    
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.task_uid == task_id).first()
        if not task and task_id.isdigit():
            task = db.query(Task).filter(Task.id == int(task_id)).first()
            
        if not task:
            raise HTTPException(status_code=404, detail=f"找不到任務 {task_id}")
        
        if task.department.upper() != department_code.upper():
            raise HTTPException(status_code=400, detail=f"任務不屬於部門 {department_code}")
        
        # 廣播 Flex Message
        success = await linebot_service.send_task_flex_card(
            department_code.upper(),
            None,  # broadcast 不需要使用者ID
            task,
            use_push=False
        )
        
        if success:
            return {
                "status": "success",
                "message": f"已向部門 {department_code} 廣播任務卡片",
                "task_id": str(task.task_uid),
                "task_title": task.title
            }
        else:
            raise HTTPException(status_code=500, detail="廣播 Flex Message 失敗")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"廣播任務失敗: {str(e)}")
    finally:
        db.close()
