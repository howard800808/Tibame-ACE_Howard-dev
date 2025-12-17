"""
情緒辨識控制器
處理情緒分析相關的業務邏輯
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.services.emotion_service import emotion_service
from app.schemas.emotion_schema import EmotionResponse, EmotionDetailResponse, EmotionHistoryResponse, EmotionStatsResponse
from app.models.emotion import EmotionAnalysis
from app.models.user import User
import json


class EmotionController:
    """情緒辨識控制器"""
    
    @staticmethod
    def analyze_emotion_from_image(
        image_data: bytes,
        image_filename: str,
        current_user: User,
        db: Session
    ) -> EmotionDetailResponse:
        """
        分析影像情緒
        
        Args:
            image_data: 影像二進位資料
            image_filename: 影像檔案名稱
            current_user: 當前使用者
            db: 資料庫 session
        
        Returns:
            EmotionDetailResponse: 分析結果
        """
        # 使用 AWS Rekognition 分析影像
        analysis_result = emotion_service.analyze_emotion_from_image(image_data)
        
        # 檢查分析是否失敗
        if "error" in analysis_result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"影像分析失敗: {analysis_result['error']}"
            )
        
        # 存儲到資料庫
        db_emotion = emotion_service.create_emotion_analysis(
            db=db,
            user_id=current_user.id,
            image_filename=image_filename,
            image_data=image_data,
            analysis_result=analysis_result
        )
        
        # 返回詳細結果
        response = EmotionDetailResponse.from_orm(db_emotion)
        
        # 解析 JSON 欄位
        if db_emotion.emotions_json:
            response.emotions_breakdown = json.loads(db_emotion.emotions_json)
        
        if db_emotion.face_details_json:
            response.face_details = json.loads(db_emotion.face_details_json)
        
        if db_emotion.analysis_result_json:
            response.analysis_result_json = db_emotion.analysis_result_json
        
        return response
    
    @staticmethod
    def get_analysis_detail(
        analysis_id: int,
        current_user: User,
        db: Session
    ) -> EmotionDetailResponse:
        """
        取得情緒分析詳細結果
        
        Args:
            analysis_id: 分析 ID
            current_user: 當前使用者
            db: 資料庫 session
        
        Returns:
            EmotionDetailResponse: 分析結果
        """
        db_emotion = emotion_service.get_emotion_analysis_by_id(db, analysis_id)
        
        if not db_emotion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="分析記錄不存在"
            )
        
        # 驗證所有權 (使用者只能查看自己的分析)
        if db_emotion.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您沒有權限查看此分析記錄"
            )
        
        # 組構詳細回應
        response = EmotionDetailResponse.from_orm(db_emotion)
        
        if db_emotion.emotions_json:
            response.emotions_breakdown = json.loads(db_emotion.emotions_json)
        
        if db_emotion.face_details_json:
            response.face_details = json.loads(db_emotion.face_details_json)
        
        if db_emotion.analysis_result_json:
            response.analysis_result_json = db_emotion.analysis_result_json
        
        return response
    
    @staticmethod
    def get_user_analyses(
        current_user: User,
        db: Session,
        skip: int = 0,
        limit: int = 10
    ) -> EmotionHistoryResponse:
        """
        取得使用者的情緒分析歷史
        
        Args:
            current_user: 當前使用者
            db: 資料庫 session
            skip: 跳過記錄數
            limit: 限制記錄數
        
        Returns:
            EmotionHistoryResponse: 歷史記錄
        """
        user_id = current_user.id
        analyses = emotion_service.get_user_emotion_analyses(db, user_id, skip, limit)
        
        # 計算統計資訊
        all_analyses = emotion_service.get_user_emotion_analyses(db, user_id, skip=0, limit=10000)
        emotion_summary = {}
        
        for analysis in all_analyses:
            emotion = analysis.dominant_emotion
            emotion_summary[emotion] = emotion_summary.get(emotion, 0) + 1
        
        # 組構回應
        recent = [EmotionResponse.from_orm(a) for a in analyses]
        
        return EmotionHistoryResponse(
            total_count=len(all_analyses),
            emotions_summary=emotion_summary,
            recent_analyses=recent
        )
    
    @staticmethod
    def get_emotion_statistics(
        current_user: User,
        db: Session
    ) -> EmotionStatsResponse:
        """
        取得使用者的情緒統計資訊
        
        Args:
            current_user: 當前使用者
            db: 資料庫 session
        
        Returns:
            EmotionStatsResponse: 統計結果
        """
        stats = emotion_service.get_emotion_statistics(db, current_user.id)
        
        return EmotionStatsResponse(
            user_id=current_user.id,
            **stats
        )
    
    @staticmethod
    def delete_analysis(
        analysis_id: int,
        current_user: User,
        db: Session
    ) -> dict:
        """
        刪除情緒分析記錄
        
        Args:
            analysis_id: 分析 ID
            current_user: 當前使用者
            db: 資料庫 session
        
        Returns:
            dict: 刪除結果訊息
        """
        # 驗證所有權
        db_emotion = emotion_service.get_emotion_analysis_by_id(db, analysis_id)
        
        if not db_emotion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="分析記錄不存在"
            )
        
        if db_emotion.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您沒有權限刪除此分析記錄"
            )
        
        # 執行刪除
        success = emotion_service.delete_emotion_analysis(db, analysis_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="刪除失敗"
            )
        
        return {"message": "分析記錄已刪除"}


# 建立全域實例
emotion_controller = EmotionController()
