from fastapi import HTTPException
import json
from app.services.adk_service import adk_service
from app.schemas.adk_schema import ChatRequest, ChatResponse, TouchingTaskRequest

class AdkController:
    async def chat(self, request: ChatRequest) -> ChatResponse:
        try:
            result = await adk_service.send_message(request.user_id, request.message)
            return ChatResponse(
                response=result["response"],
                events=result["events"]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def generate_touching_task(self, request: TouchingTaskRequest) -> ChatResponse:
        try:
            # Construct Prompt
            prompt = "你是一個專業的飯店服務顧問。請根據以下人物的 MBTI 分析結果，為每一位人物生成具體的「感動服務任務」。\n\n"
            for i, person in enumerate(request.people):
                pid = person.get('person_id', f'人物{i+1}')
                mbti = person.get('mbti_type', '未知')
                mbti_name = person.get('mbti_name', '')
                traits = person.get('behavioral_traits', [])
                if isinstance(traits, list):
                    traits = ", ".join(traits)
                
                prompt += f"### {pid}\n"
                prompt += f"- MBTI: {mbti} ({mbti_name})\n"
                prompt += f"- 行為特徵: {traits}\n"
                if person.get('recommendations'):
                    prompt += f"- 建議: {person.get('recommendations')}\n"
                prompt += "\n"
            
            prompt += """
請為每個人物生成一段 HTML 代碼 (不要包含 <html>, <body> 標籤)，格式如下：
<div style="margin-bottom: 30px; background: rgba(255,255,255,0.03); padding: 10px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
        <span style="background: #ff6b5b; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold;">{人物ID}</span>
        <span style="color: #ffc107; font-weight: bold;">{MBTI類型}</span>
    </div>
    <div style="margin-bottom: 15px;">
        <strong style="color: #17a2b8; display: block; margin-bottom: 8px;">🎯 核心感動策略：</strong>
        <p style="color: #eee;">{策略描述}</p>
    </div>
    <div style="background: rgba(23, 162, 184, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #17a2b8;">
        <strong style="color: #fff; display: block; margin-bottom: 10px;">📋 具體執行任務：</strong>
        <ul style="margin: 0; padding-left: 20px; color: #ccc;">
            <li style="margin-bottom: 8px;"><strong>第一步：</strong> {步驟1}</li>
            <li style="margin-bottom: 8px;"><strong>第二步：</strong> {步驟2}</li>
            <li style="margin-bottom: 8px;"><strong>第三步：</strong> {步驟3}</li>
        </ul>
    </div>
</div>
請直接輸出 HTML 代碼，不要有 markdown code block 標記。
"""
            print(f"[TouchingTask] Generated Prompt: {prompt}")

            result = await adk_service.send_message(request.user_id, prompt)
            
            print(f"[TouchingTask] Result: {json.dumps(result, ensure_ascii=False, indent=2)}")

            return ChatResponse(
                response=result["response"],
                events=result["events"]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

adk_controller = AdkController()
