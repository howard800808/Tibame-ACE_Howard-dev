"""
影片分析控制器
處理影片分析相關的業務邏輯
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import threading
import tempfile
import traceback
from app.services.video_service import video_service
from app.schemas.video_schema import VideoAnalysisResponse, VideoAnalysisDetailResponse, VideoAnalysisHistoryResponse
from app.models.video import VideoAnalysis
from app.models.user import User
from app.core.database import SessionLocal
import json


class VideoController:
    """影片分析控制器"""
    
    @staticmethod
    def start_video_analysis(
        video_data: bytes,
        video_filename: str,
        current_user: User,
        db: Session
    ) -> dict:
        """
        開始影片分析
        
        Args:
            video_data: 影片二進位資料
            video_filename: 影片檔案名稱
            current_user: 當前使用者
            db: 資料庫 session
        
        Returns:
            dict: 分析初始化結果
        """
        try:
            # 驗證影片檔案
            is_valid, error_msg = video_service.validate_video_file(
                video_filename,
                len(video_data)
            )
            
            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_msg
                )
            
            # 確定檔案格式
            file_ext = video_filename.split('.')[-1].lower()
            
            # 建立分析記錄
            db_video = video_service.create_video_analysis_record(
                db=db,
                user_id=current_user.id,
                video_filename=video_filename,
                video_format=file_ext
            )
            
            # 保存臨時檔案
            with tempfile.NamedTemporaryFile(
                suffix=f".{file_ext}",
                delete=False
            ) as tmp_file:
                tmp_file.write(video_data)
                tmp_path = tmp_file.name
            
            # 在背景執行緒中進行分析（為線程創建新的 Session）
            def analyze_in_thread():
                # 為線程創建新的 Session
                thread_db = SessionLocal()
                try:
                    video_service.analyze_video_async(
                        tmp_path, 
                        db_video.id, 
                        current_user.id, 
                        thread_db
                    )
                except Exception as e:
                    print(f"❌ 背景分析線程錯誤: {str(e)}")
                    traceback.print_exc()
                    # 更新數據庫記錄為失敗狀態
                    try:
                        video_record = thread_db.query(VideoAnalysis).filter(
                            VideoAnalysis.id == db_video.id
                        ).first()
                        if video_record:
                            video_record.status = "failed"
                            video_record.error_message = str(e)[:500]
                            thread_db.commit()
                    except:
                        pass
                finally:
                    thread_db.close()
            
            analysis_thread = threading.Thread(target=analyze_in_thread)
            analysis_thread.daemon = True
            analysis_thread.start()
            
            return {
                "analysis_id": db_video.id,
                "message": "影片分析已啟動，請稍候...",
                "status": "processing"
            }
        
        except HTTPException as he:
            # 重新拋出 HTTP 異常
            raise he
        except Exception as e:
            # 捕獲其他異常並記錄
            print(f"❌ 啟動分析時出錯: {str(e)}")
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"啟動分析失敗: {str(e)[:200]}"
            )
    
    @staticmethod
    def get_analysis_detail(
        analysis_id: int,
        current_user: User,
        db: Session
    ) -> VideoAnalysisDetailResponse:
        """
        取得影片分析詳細結果
        
        Args:
            analysis_id: 分析 ID
            current_user: 當前使用者
            db: 資料庫 session
        
        Returns:
            VideoAnalysisDetailResponse: 分析詳細結果
        """
        db_video = video_service.get_video_analysis_by_id(db, analysis_id)
        
        if not db_video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="分析記錄不存在"
            )
        
        # 驗證所有權
        if db_video.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您沒有權限查看此分析記錄"
            )
        
        # 先將 JSON 字符串轉換為 Python 對象
        frame_by_frame = None
        if db_video.frame_by_frame_analysis:
            try:
                frame_by_frame = json.loads(db_video.frame_by_frame_analysis)
            except:
                frame_by_frame = None
        
        emotion_stats = None
        if db_video.emotion_statistics:
            try:
                emotion_stats = json.loads(db_video.emotion_statistics)
            except:
                emotion_stats = None
        
        # 解析 transcription_json (保存的是 JSON 字符串，需轉換為列表)
        transcription_json = None
        if hasattr(db_video, 'transcription_json') and db_video.transcription_json:
            try:
                transcription_json = json.loads(db_video.transcription_json)
                if not isinstance(transcription_json, list):
                    transcription_json = [transcription_json] if transcription_json else None
            except:
                transcription_json = None
        
        # 手動構建 response 對象，避免 from_orm 驗證失敗
        response = VideoAnalysisDetailResponse(
            id=db_video.id,
            user_id=db_video.user_id,
            video_filename=db_video.video_filename,
            video_format=db_video.video_format,
            duration_seconds=db_video.duration_seconds,
            total_frames=db_video.total_frames,
            fps=db_video.fps,
            overall_dominant_emotion=db_video.overall_dominant_emotion,
            overall_confidence=db_video.overall_confidence,
            detected_people_count=db_video.detected_people_count,
            status=db_video.status,
            progress=db_video.progress,
            created_at=db_video.created_at,
            completed_at=db_video.completed_at,
            frame_by_frame_analysis=frame_by_frame,
            emotion_timeline=db_video.emotion_timeline,
            emotion_statistics=emotion_stats,
            facial_expressions_json=db_video.facial_expressions_json if hasattr(db_video, 'facial_expressions_json') else None,
            transcription_text=db_video.transcription_text if hasattr(db_video, 'transcription_text') else None,
            transcription_json=transcription_json,
            transcription_confidence=db_video.transcription_confidence if hasattr(db_video, 'transcription_confidence') else None,
            speaker_segments=db_video.speaker_segments if hasattr(db_video, 'speaker_segments') else None,
            speaker_count=db_video.speaker_count if hasattr(db_video, 'speaker_count') else 0
        )
        
        return response
    
    @staticmethod
    def get_analysis_progress(
        analysis_id: int,
        current_user: User,
        db: Session
    ) -> dict:
        """取得分析進度"""
        db_video = video_service.get_video_analysis_by_id(db, analysis_id)
        
        if not db_video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="分析記錄不存在"
            )
        
        # 驗證所有權
        if db_video.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您沒有權限查看此分析進度"
            )
        
        return video_service.get_analysis_progress(db, analysis_id)
    
    @staticmethod
    def get_user_analyses(
        current_user: User,
        db: Session,
        skip: int = 0,
        limit: int = 10
    ) -> VideoAnalysisHistoryResponse:
        """取得使用者的影片分析歷史"""
        analyses = video_service.get_user_video_analyses(
            db,
            current_user.id,
            skip,
            limit
        )
        
        # 計算總數
        total_count = db.query(VideoAnalysis).filter(
            VideoAnalysis.user_id == current_user.id
        ).count()
        
        return VideoAnalysisHistoryResponse(
            total_count=total_count,
            analyses=[VideoAnalysisResponse.from_orm(a) for a in analyses]
        )
    
    @staticmethod
    def delete_analysis(
        analysis_id: int,
        current_user: User,
        db: Session
    ) -> dict:
        """刪除影片分析記錄"""
        db_video = video_service.get_video_analysis_by_id(db, analysis_id)
        
        if not db_video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="分析記錄不存在"
            )
        
        # 驗證所有權
        if db_video.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您沒有權限刪除此分析記錄"
            )
        
        # 執行刪除
        success = video_service.delete_video_analysis(db, analysis_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="刪除失敗"
            )
        
        return {"message": "分析記錄已刪除"}


# 建立全域實例
video_controller = VideoController()
