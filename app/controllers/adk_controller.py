from fastapi import HTTPException
from app.services.adk_service import adk_service
from app.schemas.adk_schema import ChatRequest, ChatResponse

class AdkController:
    def chat(self, request: ChatRequest) -> ChatResponse:
        try:
            result = adk_service.send_message(request.user_id, request.message)
            return ChatResponse(
                response=result["response"],
                events=result["events"]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

adk_controller = AdkController()
