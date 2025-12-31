"""
情緒辨識路由
處理情緒分析相關的 API 端點
"""

from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.controllers.emotion_controller import emotion_controller
from app.schemas.emotion_schema import (
    EmotionResponse, 
    EmotionDetailResponse, 
    EmotionHistoryResponse, 
    EmotionStatsResponse
)
from app.models.user import User

router = APIRouter(prefix="/emotions", tags=["影像情緒分析"])


@router.post("/analyze-image-emotion", response_model=EmotionDetailResponse, status_code=status.HTTP_201_CREATED)
async def analyze_emotion(
    file: UploadFile = File(..., description="要分析的影像檔案 (JPEG, PNG, etc.)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    分析影像情緒
    
    - **file**: 影像檔案 (必填)
    
    使用 AWS Rekognition 服務分析影像中人物的情緒
    
    回傳結果包含:
    - dominant_emotion: 主要情緒 (HAPPY, SAD, ANGRY, CONFUSED, DISGUSTED, SURPRISED, CALM, NEUTRAL)
    - dominant_emotion_confidence: 主要情緒的信心度
    - face_count: 檢測到的人臉數量
    - emotions_breakdown: 所有情緒的信心度分佈
    - face_details: 每個人臉的詳細情緒資訊
    """
    # 驗證檔案類型
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp", "image/tiff"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的檔案類型。支持的格式: {', '.join(allowed_types)}"
        )
    
    # 驗證檔案大小 (限制為 5MB)
    max_size = 5 * 1024 * 1024  # 5MB
    file_content = await file.read()
    if len(file_content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"檔案過大，限制為 5MB，目前大小: {len(file_content) / 1024 / 1024:.2f}MB"
        )
    
    # 分析情緒
    result = await emotion_controller.analyze_emotion_from_image(
        image_data=file_content,
        image_filename=file.filename,
        current_user=current_user,
        db=db
    )
    
    return result


@router.get("/image-results/{analysis_id}", response_model=EmotionDetailResponse)
async def get_emotion_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    取得情緒分析詳細結果
    
    - **analysis_id**: 分析記錄 ID
    
    取得指定分析記錄的詳細資訊，包含完整的情緒分析數據
    """
    return emotion_controller.get_analysis_detail(analysis_id, current_user, db)


@router.get("/history", response_model=EmotionHistoryResponse)
async def get_emotion_history(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    取得使用者的情緒分析歷史
    
    - **skip**: 跳過的記錄數 (預設: 0)
    - **limit**: 限制回傳的記錄數 (預設: 10)
    
    分頁取得使用者的所有情緒分析記錄，並統計各情緒的出現次數
    """
    if skip < 0 or limit < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="skip 必須 >= 0，limit 必須 >= 1"
        )
    
    return emotion_controller.get_user_analyses(current_user, db, skip, limit)


@router.get("/statistics", response_model=EmotionStatsResponse)
async def get_emotion_statistics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    取得使用者的情緒統計資訊
    
    統計使用者所有分析記錄的情緒分佈，包含:
    - 總分析次數
    - 最常見的情緒
    - 各情緒的百分比分佈
    - 平均信心度
    - 分析時間範圍
    """
    return emotion_controller.get_emotion_statistics(current_user, db)


@router.delete("/image-results/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_emotion_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    刪除情緒分析記錄
    
    - **analysis_id**: 分析記錄 ID
    
    刪除指定的分析記錄。只有記錄所有者或管理員可以刪除
    """
    emotion_controller.delete_analysis(analysis_id, current_user, db)
