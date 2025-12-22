from sqlalchemy import Column, Integer, String, Float, DateTime, LargeBinary, Text
from sqlalchemy.sql import func
from app.core.database import Base


class VideoAnalysis(Base):
    """影片情緒分析模型 (Model層)"""
    __tablename__ = "video_analysis"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False, comment="使用者 ID")
    video_filename = Column(String(255), nullable=False, comment="影片檔案名稱")
    video_format = Column(String(10), nullable=False, comment="影片格式: mp4, wmv, etc")
    
    # 影片資訊
    duration_seconds = Column(Float, nullable=True, comment="影片時長（秒）")
    total_frames = Column(Integer, nullable=True, comment="總幀數")
    fps = Column(Float, nullable=True, comment="幀率")
    
    # 分析結果
    overall_dominant_emotion = Column(String(50), nullable=False, comment="整體主要情緒")
    overall_confidence = Column(Float, nullable=False, comment="整體信心度")
    
    # 詳細分析結果（JSON 格式）
    frame_by_frame_analysis = Column(Text, nullable=True, comment="逐幀分析結果 (JSON)")
    emotion_timeline = Column(Text, nullable=True, comment="情緒時間線 (JSON)")
    emotion_statistics = Column(Text, nullable=True, comment="情緒統計資訊 (JSON)")
    detected_people_count = Column(Integer, default=0, comment="檢測到的人物數量")
    
    # 面部動作識別
    facial_expressions_json = Column(Text, nullable=True, comment="面部表情詳細資訊 (JSON)")
    
    # 語音轉文字
    transcription_json = Column(Text, nullable=True, comment="語音轉文字結果 (JSON)")
    transcription_text = Column(Text, nullable=True, comment="對話文字內容")
    transcription_confidence = Column(Float, default=0.0, comment="轉錄信心度")
    speaker_segments = Column(Text, nullable=True, comment="說話人分段結果 (JSON)")
    speaker_count = Column(Integer, default=0, comment="檢測到的說話人數量")
    
    # 狀態與錯誤
    status = Column(String(20), default="processing", comment="分析狀態: processing, success, failed")
    progress = Column(Float, default=0.0, comment="分析進度 (0-100)")
    error_message = Column(String(500), nullable=True, comment="錯誤訊息")
    
    # 時間戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="建立時間")
    completed_at = Column(DateTime(timezone=True), nullable=True, comment="完成時間")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新時間")
    
    def __repr__(self):
        return f"<VideoAnalysis(id={self.id}, user_id={self.user_id}, filename='{self.video_filename}')>"
