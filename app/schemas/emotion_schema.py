from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class EmotionBase(BaseModel):
    """情緒分析基礎 Schema"""
    user_id: int
    dominant_emotion: str
    dominant_emotion_confidence: float


class EmotionCreate(BaseModel):
    """建立情緒分析 Schema (用於上傳影像)"""
    user_id: int = Field(..., gt=0, description="使用者 ID")
    # 影像資料將通過 multipart/form-data 上傳
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 1
                }
            ]
        }
    }


class EmotionResponse(EmotionBase):
    """情緒分析回應 Schema"""
    id: int
    image_filename: str
    face_count: int
    status: str
    emotions_json: Optional[str] = None
    face_details_json: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class EmotionDetailResponse(EmotionResponse):
    """情緒分析詳細回應 Schema"""
    analysis_result_json: Optional[str] = None
    emotions_breakdown: Optional[Dict[str, float]] = None  # 解析後的情緒詳細數據
    face_details: Optional[List[Dict[str, Any]]] = None  # 解析後的臉部詳細資訊


class EmotionHistoryResponse(BaseModel):
    """使用者情緒分析歷史 Schema"""
    total_count: int
    emotions_summary: Dict[str, int]  # 各情緒的計數統計
    recent_analyses: List[EmotionResponse]  # 最近的分析結果


class EmotionStatsResponse(BaseModel):
    """情緒統計回應 Schema"""
    user_id: int
    total_analyses: int
    most_common_emotion: str
    emotion_distribution: Dict[str, float]  # 各情緒的百分比分佈
    average_confidence: float  # 平均信心度
    analysis_period: str  # 分析時間範圍
