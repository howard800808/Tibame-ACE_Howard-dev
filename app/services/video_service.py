"""
影片情緒分析服務
使用 OpenCV 進行視頻分幀，AWS Rekognition 進行情緒分析，Azure Speech-to-Text 進行語音轉文字
"""

import cv2
import json
import tempfile
from pathlib import Path
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from datetime import datetime
import threading
from app.models.video import VideoAnalysis
from app.services.emotion_service import emotion_service
from app.core.config import settings

# 嘗試導入轉錄服務
try:
    from app.services.azure_transcription_service import azure_transcription_service
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False
    azure_transcription_service = None


class VideoService:
    """影片分析服務"""
    
    # 支援的影片格式
    SUPPORTED_FORMATS = ['.mp4', '.wmv', '.avi', '.mov', '.mkv', '.webm']
    
    # 幀間隔（每 N 幀分析一次，減少 AWS API 呼叫）
    FRAME_INTERVAL = 5
    
    def __init__(self):
        """初始化服務"""
        self.analysis_threads = {}  # 存儲進行中的分析執行緒
    
    @staticmethod
    def validate_video_file(filename: str, file_size: int) -> tuple[bool, str]:
        """
        驗證影片檔案
        
        Returns:
            (is_valid, error_message)
        """
        # 檢查副檔名
        file_ext = Path(filename).suffix.lower()
        if file_ext not in VideoService.SUPPORTED_FORMATS:
            return False, f"不支持的檔案格式。支持的格式: {', '.join(VideoService.SUPPORTED_FORMATS)}"
        
        # 檢查檔案大小 (限制為 500MB)
        max_size = 500 * 1024 * 1024
        if file_size > max_size:
            return False, f"檔案過大。限制為 500MB，目前: {file_size / 1024 / 1024:.2f}MB"
        
        return True, ""
    
    @staticmethod
    def create_video_analysis_record(
        db: Session,
        user_id: int,
        video_filename: str,
        video_format: str
    ) -> VideoAnalysis:
        """建立影片分析記錄"""
        db_video = VideoAnalysis(
            user_id=user_id,
            video_filename=video_filename,
            video_format=video_format.lstrip('.'),
            status="processing",
            progress=0.0,
            overall_dominant_emotion="NEUTRAL",
            overall_confidence=0.0
        )
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
        return db_video
    
    def analyze_video_async(
        self,
        video_path: str,
        analysis_id: int,
        user_id: int,
        db: Session
    ):
        """
        非同步分析影片
        在背景執行緒中進行分析
        """
        video_analysis = None
        
        try:
            # 查詢分析記錄
            video_analysis = db.query(VideoAnalysis).filter(
                VideoAnalysis.id == analysis_id
            ).first()
            
            if not video_analysis:
                raise Exception("分析記錄不存在")
            
            # 打開影片
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise Exception("無法開啟影片檔案")
            
            # 獲取影片資訊
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            duration_seconds = total_frames / fps if fps > 0 else 0
            
            # 更新影片資訊
            video_analysis.total_frames = total_frames
            video_analysis.fps = fps
            video_analysis.duration_seconds = duration_seconds
            db.commit()
            
            # 分析每一幀
            frame_emotions = []
            frame_count = 0
            analyzed_frames = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # 每 FRAME_INTERVAL 幀分析一次
                if frame_count % self.FRAME_INTERVAL == 0:
                    try:
                        # 將幀轉換為 JPEG
                        _, buffer = cv2.imencode('.jpg', frame)
                        frame_data = buffer.tobytes()
                        
                        # 分析幀的情緒
                        analysis_result = emotion_service.analyze_emotion_from_image(frame_data)
                        
                        if "error" not in analysis_result:
                            timestamp = (frame_count / fps) if fps > 0 else 0
                            
                            frame_emotions.append({
                                "frame_number": frame_count,
                                "timestamp_seconds": round(timestamp, 2),
                                "dominant_emotion": analysis_result.get("dominant_emotion", "NEUTRAL"),
                                "confidence": analysis_result.get("dominant_emotion_confidence", 0.0),
                                "emotions_breakdown": json.loads(
                                    analysis_result.get("emotions_json", "{}")
                                ),
                                "people_count": analysis_result.get("face_count", 0)
                            })
                            
                            analyzed_frames += 1
                    
                    except Exception as e:
                        print(f"幀 {frame_count} 分析失敗: {str(e)}")
                        continue
                    
                    # 更新進度
                    progress = (frame_count / total_frames) * 100
                    video_analysis.progress = min(progress, 99.0)
                    db.commit()
            
            cap.release()
            
            # 計算統計資訊
            if frame_emotions:
                stats = self._calculate_statistics(frame_emotions)
                
                # 找出整體主要情緒
                emotion_counts = {}
                total_confidence = 0.0
                
                for frame_data in frame_emotions:
                    emotion = frame_data["dominant_emotion"]
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                    total_confidence += frame_data["confidence"]
                
                overall_emotion = max(emotion_counts, key=emotion_counts.get) if emotion_counts else "NEUTRAL"
                overall_confidence = total_confidence / len(frame_emotions) if frame_emotions else 0.0
                
                # 保存結果
                video_analysis.overall_dominant_emotion = overall_emotion
                video_analysis.overall_confidence = round(overall_confidence, 2)
                video_analysis.frame_by_frame_analysis = json.dumps(frame_emotions)
                video_analysis.emotion_statistics = json.dumps(stats)
                video_analysis.emotion_timeline = self._generate_emotion_timeline(frame_emotions)
                video_analysis.detected_people_count = max(
                    (f.get("people_count", 0) for f in frame_emotions),
                    default=0
                )
            
            # 進行語音轉文字分析 (使用 Azure Speech-to-Text)
            if AZURE_AVAILABLE and azure_transcription_service and settings.AZURE_SPEECH_API_KEY:
                print(f"開始 Azure 語音轉文字分析: {video_path}")
                try:
                    success, transcript_text, segments, confidence = azure_transcription_service.transcribe_video(
                        video_path,
                        language='zh-TW'  # 繁體中文 (台灣)
                    )
                    
                    if success and transcript_text:
                        # 構建說話人分段信息
                        speaker_data = {
                            'speaker_count': len(set(seg.get('speaker', 'Unknown') for seg in segments)) if segments else 0,
                            'segments': segments,
                            'full_text': transcript_text
                        }
                        
                        video_analysis.transcription_text = transcript_text
                        video_analysis.transcription_json = json.dumps(segments)
                        video_analysis.speaker_segments = json.dumps(speaker_data)
                        video_analysis.speaker_count = speaker_data['speaker_count']
                        video_analysis.transcription_confidence = confidence
                        print(f"✓ Azure 語音轉文字成功: {len(segments)} 句, 說話人: {speaker_data['speaker_count']}, 信心度: {confidence:.0%}")
                    else:
                        print("❌ Azure 語音轉文字失敗或無法提取音軌")
                        video_analysis.transcription_text = "無法提取音軌或轉錄失敗"
                        video_analysis.transcription_confidence = 0.0
                except Exception as e:
                    print(f"❌ Azure 語音轉文字異常: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    video_analysis.transcription_text = f"轉錄出錯: {str(e)}"
                    video_analysis.transcription_confidence = 0.0
            else:
                print("ℹ️ Azure Speech-to-Text 服務未配置或 API 密鑰缺失")
                video_analysis.transcription_text = "音頻轉錄服務未配置"
                video_analysis.transcription_confidence = 0.0
            
            video_analysis.status = "success"
            video_analysis.progress = 100.0
            video_analysis.completed_at = datetime.utcnow()
            db.commit()
            
        except Exception as e:
            print(f"影片分析錯誤: {str(e)}")
            if video_analysis:
                video_analysis.status = "failed"
                video_analysis.error_message = str(e)
                video_analysis.progress = 0.0
                db.commit()
    
    @staticmethod
    def _calculate_statistics(frame_emotions: List[Dict]) -> List[Dict]:
        """計算情緒統計"""
        emotion_data = {}
        
        for frame in frame_emotions:
            emotion = frame["dominant_emotion"]
            confidence = frame["confidence"]
            
            if emotion not in emotion_data:
                emotion_data[emotion] = {
                    "count": 0,
                    "total_confidence": 0.0
                }
            
            emotion_data[emotion]["count"] += 1
            emotion_data[emotion]["total_confidence"] += confidence
        
        # 計算百分比和平均信心度
        total_frames = sum(e["count"] for e in emotion_data.values())
        stats = []
        
        for emotion, data in emotion_data.items():
            stats.append({
                "emotion": emotion,
                "count": data["count"],
                "percentage": round((data["count"] / total_frames) * 100, 2),
                "average_confidence": round(
                    data["total_confidence"] / data["count"], 2
                )
            })
        
        return sorted(stats, key=lambda x: x["count"], reverse=True)
    
    @staticmethod
    def _generate_emotion_timeline(frame_emotions: List[Dict]) -> str:
        """生成情緒時間線（簡化版）"""
        if not frame_emotions:
            return "{}"
        
        timeline = {
            "duration_seconds": frame_emotions[-1].get("timestamp_seconds", 0),
            "key_moments": [],
            "emotion_changes": []
        }
        
        # 檢測主要情緒轉變
        prev_emotion = None
        for frame in frame_emotions:
            emotion = frame["dominant_emotion"]
            if emotion != prev_emotion:
                timeline["emotion_changes"].append({
                    "timestamp": frame["timestamp_seconds"],
                    "emotion": emotion,
                    "confidence": frame["confidence"]
                })
                prev_emotion = emotion
        
        # 找出高信心度的時刻
        high_confidence = [f for f in frame_emotions if f["confidence"] > 0.8]
        timeline["key_moments"] = high_confidence[:10]  # 前 10 個高信心度時刻
        
        return json.dumps(timeline)
    
    @staticmethod
    def get_video_analysis_by_id(db: Session, analysis_id: int) -> Optional[VideoAnalysis]:
        """根據 ID 取得影片分析"""
        return db.query(VideoAnalysis).filter(
            VideoAnalysis.id == analysis_id
        ).first()
    
    @staticmethod
    def get_user_video_analyses(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[VideoAnalysis]:
        """取得使用者的影片分析歷史"""
        return db.query(VideoAnalysis).filter(
            VideoAnalysis.user_id == user_id
        ).order_by(
            VideoAnalysis.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def delete_video_analysis(db: Session, analysis_id: int) -> bool:
        """刪除影片分析記錄"""
        analysis = db.query(VideoAnalysis).filter(
            VideoAnalysis.id == analysis_id
        ).first()
        
        if not analysis:
            return False
        
        db.delete(analysis)
        db.commit()
        return True
    
    @staticmethod
    def get_analysis_progress(db: Session, analysis_id: int) -> Optional[Dict[str, Any]]:
        """取得分析進度"""
        analysis = VideoService.get_video_analysis_by_id(db, analysis_id)
        
        if not analysis:
            return None
        
        progress_int = int(analysis.progress) if analysis.progress else 0
        return {
            "analysis_id": analysis.id,
            "progress": progress_int,
            "status": analysis.status,
            "current_frame": analysis.total_frames and int(analysis.total_frames * progress_int / 100) or 0,
            "total_frames": analysis.total_frames,
            "message": analysis.error_message if analysis.status == "failed" else f"分析進度: {analysis.progress:.1f}%"
        }


# 建立全域實例
video_service = VideoService()
