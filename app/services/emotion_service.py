"""
AWS 情緒辨識服務
使用 Amazon Rekognition 進行影像情緒分析
"""

import boto3
import json
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models.emotion import EmotionAnalysis
from app.core.config import settings


class EmotionService:
    """情緒辨識服務"""
    
    # AWS Rekognition 情緒映射
    EMOTION_MAP = {
        "HAPPY": "開心",
        "SAD": "悲傷",
        "ANGRY": "憤怒",
        "CONFUSED": "困惑",
        "DISGUSTED": "厭惡",
        "SURPRISED": "驚訝",
        "CALM": "平靜",
        "NEUTRAL": "中立"
    }
    
    def __init__(self):
        """初始化 AWS Rekognition 客戶端"""
        self.rekognition_client = None
        self._init_aws_client()
    
    def _init_aws_client(self):
        """初始化 AWS 客戶端"""
        try:
            self.rekognition_client = boto3.client(
                'rekognition',
                region_name=settings.AWS_DEFAULT_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
        except Exception as e:
            print(f"AWS 客戶端初始化失敗: {str(e)}")
            self.rekognition_client = None
    
    @staticmethod
    def create_emotion_analysis(
        db: Session,
        user_id: int,
        image_filename: str,
        image_data: bytes,
        analysis_result: Dict[str, Any]
    ) -> EmotionAnalysis:
        """
        建立情緒分析記錄
        
        Args:
            db: 資料庫 session
            user_id: 使用者 ID
            image_filename: 影像檔案名稱
            image_data: 影像二進位資料
            analysis_result: AWS 分析結果
        
        Returns:
            EmotionAnalysis: 新建立的分析記錄
        """
        try:
            # 提取主要情緒資訊
            dominant_emotion = analysis_result.get("dominant_emotion", "NEUTRAL")
            dominant_confidence = analysis_result.get("dominant_emotion_confidence", 0.0)
            face_count = analysis_result.get("face_count", 0)
            emotions_json = analysis_result.get("emotions_json", "{}")
            face_details_json = analysis_result.get("face_details_json", "{}")
            
            # 建立資料庫記錄
            db_emotion = EmotionAnalysis(
                user_id=user_id,
                image_filename=image_filename,
                image_data=image_data,
                dominant_emotion=dominant_emotion,
                dominant_emotion_confidence=dominant_confidence,
                face_count=face_count,
                emotions_json=emotions_json,
                face_details_json=face_details_json,
                analysis_result_json=json.dumps(analysis_result),
                status="success"
            )
            
            db.add(db_emotion)
            db.commit()
            db.refresh(db_emotion)
            return db_emotion
            
        except Exception as e:
            # 建立失敗記錄
            db_emotion = EmotionAnalysis(
                user_id=user_id,
                image_filename=image_filename,
                image_data=image_data,
                dominant_emotion="NEUTRAL",
                dominant_emotion_confidence=0.0,
                face_count=0,
                status="failed",
                error_message=str(e)
            )
            db.add(db_emotion)
            db.commit()
            db.refresh(db_emotion)
            return db_emotion
    
    def analyze_emotion_from_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        使用 AWS Rekognition 分析影像情緒
        
        Args:
            image_data: 影像二進位資料
        
        Returns:
            分析結果字典，包含情緒資訊
        """
        if not self.rekognition_client:
            return {
                "status": "failed",
                "error": "AWS 客戶端未初始化"
            }
        
        try:
            # 呼叫 AWS Rekognition DetectFaces API
            response = self.rekognition_client.detect_faces(
                Image={'Bytes': image_data},
                Attributes=['ALL']
            )
            
            # 處理分析結果
            face_details = response.get('FaceDetails', [])
            face_count = len(face_details)
            
            if face_count == 0:
                return {
                    "dominant_emotion": "NEUTRAL",
                    "dominant_emotion_confidence": 0.0,
                    "face_count": 0,
                    "emotions_json": "{}",
                    "face_details_json": "{}",
                    "message": "未檢測到人臉"
                }
            
            # 合併所有臉部的情緒數據（取平均值）
            merged_emotions = self._merge_face_emotions(face_details)
            
            # 找出主要情緒
            dominant_emotion = max(merged_emotions, key=merged_emotions.get)
            dominant_confidence = merged_emotions[dominant_emotion]
            
            # 提取臉部詳細資訊
            face_details_simplified = self._extract_face_details(face_details)
            
            return {
                "dominant_emotion": dominant_emotion,
                "dominant_emotion_confidence": dominant_confidence,
                "face_count": face_count,
                "emotions_json": json.dumps(merged_emotions),
                "face_details_json": json.dumps(face_details_simplified),
                "full_response": response
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    @staticmethod
    def _merge_face_emotions(face_details: List[Dict]) -> Dict[str, float]:
        """
        合併多個臉部的情緒數據（取平均值）
        
        Args:
            face_details: AWS 回傳的臉部詳細資訊
        
        Returns:
            合併後的情緒字典
        """
        emotion_keys = ["HAPPY", "SAD", "ANGRY", "CONFUSED", "DISGUSTED", "SURPRISED", "CALM", "NEUTRAL"]
        merged = {emotion: 0.0 for emotion in emotion_keys}
        
        if not face_details:
            return merged
        
        for face in face_details:
            emotions = face.get('Emotions', [])
            for emotion in emotions:
                emotion_type = emotion['Type']
                confidence = emotion['Confidence']
                if emotion_type in merged:
                    merged[emotion_type] += confidence
        
        # 計算平均值
        for emotion in merged:
            merged[emotion] = round(merged[emotion] / len(face_details), 2)
        
        return merged
    
    @staticmethod
    def _extract_face_details(face_details: List[Dict]) -> List[Dict]:
        """
        提取簡化的臉部詳細資訊
        
        Args:
            face_details: AWS 回傳的臉部詳細資訊
        
        Returns:
            簡化後的臉部資訊
        """
        simplified = []
        
        for i, face in enumerate(face_details):
            face_info = {
                "face_id": i + 1,
                "bounding_box": face.get('BoundingBox', {}),
                "confidence": face.get('Confidence', 0),
                "emotions": {}
            }
            
            # 提取該臉部的情緒資訊
            for emotion in face.get('Emotions', []):
                emotion_type = emotion['Type']
                confidence = emotion['Confidence']
                face_info['emotions'][emotion_type] = round(confidence, 2)
            
            simplified.append(face_info)
        
        return simplified
    
    @staticmethod
    def get_emotion_analysis_by_id(db: Session, analysis_id: int) -> Optional[EmotionAnalysis]:
        """根據 ID 取得情緒分析記錄"""
        return db.query(EmotionAnalysis).filter(EmotionAnalysis.id == analysis_id).first()
    
    @staticmethod
    def get_user_emotion_analyses(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[EmotionAnalysis]:
        """取得使用者的情緒分析歷史"""
        return db.query(EmotionAnalysis).filter(
            EmotionAnalysis.user_id == user_id
        ).order_by(
            EmotionAnalysis.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_emotion_statistics(db: Session, user_id: int) -> Dict[str, Any]:
        """取得使用者的情緒統計資訊"""
        analyses = db.query(EmotionAnalysis).filter(
            EmotionAnalysis.user_id == user_id,
            EmotionAnalysis.status == "success"
        ).all()
        
        if not analyses:
            return {
                "total_analyses": 0,
                "most_common_emotion": "NEUTRAL",
                "emotion_distribution": {},
                "average_confidence": 0.0
            }
        
        # 計算情緒分佈
        emotion_count = {}
        total_confidence = 0.0
        
        for analysis in analyses:
            emotion = analysis.dominant_emotion
            emotion_count[emotion] = emotion_count.get(emotion, 0) + 1
            total_confidence += analysis.dominant_emotion_confidence
        
        # 計算百分比
        total = len(analyses)
        emotion_distribution = {
            emotion: round((count / total) * 100, 2)
            for emotion, count in emotion_count.items()
        }
        
        # 找出最常見的情緒
        most_common = max(emotion_count, key=emotion_count.get) if emotion_count else "NEUTRAL"
        
        return {
            "total_analyses": total,
            "most_common_emotion": most_common,
            "emotion_distribution": emotion_distribution,
            "average_confidence": round(total_confidence / total, 2),
            "analysis_period": f"{analyses[-1].created_at} ~ {analyses[0].created_at}"
        }
    
    @staticmethod
    def delete_emotion_analysis(db: Session, analysis_id: int) -> bool:
        """刪除情緒分析記錄"""
        analysis = db.query(EmotionAnalysis).filter(EmotionAnalysis.id == analysis_id).first()
        if not analysis:
            return False
        
        db.delete(analysis)
        db.commit()
        return True


# 建立全域實例
emotion_service = EmotionService()
