from fastapi import APIRouter, Depends
from app.controllers.adk_controller import adk_controller
from app.schemas.adk_schema import ChatRequest, ChatResponse, TouchingTaskRequest
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/adk",
    tags=["Google ADK Agent"]
)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    current_user = Depends(get_current_user)
):
    """
    與 Google ADK Agent 進行對話
    """
    # 如果請求中沒有指定 user_id，則使用當前登入使用者的 ID
    if request.user_id == "default_user":
        request.user_id = current_user.username
        
    return await adk_controller.chat(request)

@router.post("/generate-touching-task", response_model=ChatResponse)
async def generate_touching_task(
    request: TouchingTaskRequest,
    current_user = Depends(get_current_user)
):
    """
    生成感動服務任務
    """
    if request.user_id == "default_user":
        request.user_id = current_user.username
        
    return await adk_controller.generate_touching_task(request)
