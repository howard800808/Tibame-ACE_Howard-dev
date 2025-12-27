"""
影片分析路由
處理影片分析相關的 API 端點
"""

from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.controllers.video_controller import video_controller
from app.schemas.video_schema import (
    VideoAnalysisResponse,
    VideoAnalysisDetailResponse,
    VideoAnalysisHistoryResponse,
    VideoUploadResponse,
    VideoAnalysisProgressResponse
)
from app.models.user import User

router = APIRouter(prefix="/videos", tags=["影片情緒分析"])


@router.post("/analyze-video-emotion", response_model=VideoUploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def analyze_video(
    file: UploadFile = File(..., description="影片檔案 (MP4, WMV, AVI 等)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    分析影片中的人物情緒
    
    - **file**: 影片檔案 (必填)
    
    支持的格式: MP4, WMV, AVI, MOV, MKV, WebM
    最大檔案大小: 500MB
    
    該端點返回 202 Accepted，表示分析已在背景進行。
    使用返回的 analysis_id 可查詢分析進度。
    """
    # 驗證檔案副檔名
    allowed_extensions = ['.mp4', '.wmv', '.avi', '.mov', '.mkv', '.webm']
    file_ext = '.' + (file.filename.split('.')[-1].lower() if file.filename else '')
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的檔案類型：{file_ext}。支持的格式: MP4, WMV, AVI, MOV, MKV, WebM"
        )
    
    # 讀取影片檔案
    try:
        video_content = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"讀取檔案失敗: {str(e)}"
        )
    
    if not video_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="影片檔案為空"
        )
    
    # 啟動分析
    try:
        result = video_controller.start_video_analysis(
            video_data=video_content,
            video_filename=file.filename,
            current_user=current_user,
            db=db
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"啟動分析失敗: {str(e)}"
        )
    
    return VideoUploadResponse(
        analysis_id=result["analysis_id"],
        message=result["message"],
        status=result["status"]
    )


@router.get("/video-results/{analysis_id}", response_model=VideoAnalysisDetailResponse)
async def get_video_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    取得影片分析詳細結果
    
    - **analysis_id**: 分析記錄 ID
    
    返回完整的分析結果，包含:
    - 逐幀情緒分析
    - 情緒時間線
    - 統計資訊
    - 面部表情詳細資料
    """
    return video_controller.get_analysis_detail(analysis_id, current_user, db)


@router.get("/video-results/{analysis_id}/progress", response_model=VideoAnalysisProgressResponse)
async def get_video_analysis_progress(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    取得影片分析進度
    
    - **analysis_id**: 分析記錄 ID
    
    用於檢查背景分析的進度。
    當 progress = 100 且 status = 'success' 時，分析完成。
    """
    return video_controller.get_analysis_progress(analysis_id, current_user, db)


@router.get("/history", response_model=VideoAnalysisHistoryResponse)
async def get_video_analysis_history(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    取得使用者的影片分析歷史
    
    - **skip**: 跳過的記錄數 (預設: 0)
    - **limit**: 限制回傳的記錄數 (預設: 10)
    
    分頁取得使用者的所有影片分析記錄
    """
    if skip < 0 or limit < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="skip 必須 >= 0，limit 必須 >= 1"
        )
    
    return video_controller.get_user_analyses(current_user, db, skip, limit)


@router.delete("/video-results/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    刪除影片分析記錄
    
    - **analysis_id**: 分析記錄 ID
    
    刪除指定的分析記錄。只有記錄所有者或管理員可以刪除。
    """
    video_controller.delete_analysis(analysis_id, current_user, db)
