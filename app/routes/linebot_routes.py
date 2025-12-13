from fastapi import APIRouter, Request, Header, Query
from typing import Optional

from app.controllers.linebot_controller import linebot_controller


router = APIRouter(prefix="/api/linebot", tags=["LINE Bot"])


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
