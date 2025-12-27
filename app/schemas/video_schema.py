from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class VideoAnalysisBase(BaseModel):
    """影片分析基礎 Schema"""
    user_id: int
    video_filename: str


class VideoAnalysisCreate(BaseModel):
    """建立影片分析 Schema"""
    user_id: int = Field(..., gt=0, description="使用者 ID")
    # 影片資料將通過 multipart/form-data 上傳


class FrameEmotionData(BaseModel):
    """單幀情緒數據"""
    frame_number: int
    timestamp_seconds: float
    dominant_emotion: str
    confidence: float
    emotions_breakdown: Dict[str, float]
    people_count: int


class EmotionStatistics(BaseModel):
    """情緒統計"""
    emotion: str
    count: int
    percentage: float
    average_confidence: float


class TranscriptionSegment(BaseModel):
    """語音轉錄片段"""
    start_time: float = Field(..., description="開始時間（秒）")
    end_time: float = Field(..., description="結束時間（秒）")
    content: str = Field(..., description="對話內容")
    confidence: float = Field(..., description="信心度 (0-1)")
    speaker: Optional[str] = Field(None, description="說話者")


class VideoAnalysisResponse(BaseModel):
    """影片分析回應 Schema"""
    id: int
    user_id: int
    video_filename: str
    video_format: str
    duration_seconds: Optional[float]
    total_frames: Optional[int]
    fps: Optional[float]
    overall_dominant_emotion: str
    overall_confidence: float
    detected_people_count: int
    status: str
    progress: int
    created_at: datetime
    completed_at: Optional[datetime]
    
    model_config = {"from_attributes": True}


class VideoAnalysisDetailResponse(VideoAnalysisResponse):
    """影片分析詳細回應 Schema"""
    frame_by_frame_analysis: Optional[List[FrameEmotionData]] = None
    emotion_timeline: Optional[str] = None
    emotion_statistics: Optional[List[EmotionStatistics]] = None
    facial_expressions_json: Optional[str] = None
    transcription_text: Optional[str] = Field(None, description="對話文字內容")
    transcription_json: Optional[List[TranscriptionSegment]] = Field(None, description="詳細語音轉錄結果")
    transcription_confidence: Optional[float] = Field(None, description="轉錄信心度")
    speaker_segments: Optional[str] = Field(None, description="說話人分段信息 (JSON)")
    speaker_count: Optional[int] = Field(None, description="偵測到的說話人數量")


class VideoAnalysisHistoryResponse(BaseModel):
    """影片分析歷史回應 Schema"""
    total_count: int = Field(..., description="總數")
    analyses: List[VideoAnalysisResponse] = Field(..., description="分析清單")


class VideoUploadResponse(BaseModel):
    """影片上傳回應 Schema"""
    analysis_id: int = Field(..., description="分析 ID")
    message: str = Field(..., description="訊息")
    status: str = Field(..., description="狀態")


class VideoAnalysisProgressResponse(BaseModel):
    """影片分析進度回應 Schema"""
    analysis_id: int = Field(..., description="分析 ID")
    status: str = Field(..., description="狀態 (processing/success/failed)")
    progress: int = Field(..., ge=0, le=100, description="進度百分比")
    message: Optional[str] = Field(None, description="進度訊息")
