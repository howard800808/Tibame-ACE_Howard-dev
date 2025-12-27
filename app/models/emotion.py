from sqlalchemy import Column, Integer, String, Float, DateTime, LargeBinary, Text
from sqlalchemy.sql import func
from app.core.database import Base


class EmotionAnalysis(Base):
    """情緒辨識分析結果模型 (Model層)"""
    __tablename__ = "emotion_analysis"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False, comment="使用者 ID")
    image_filename = Column(String(255), nullable=False, comment="影像檔案名稱")
    image_data = Column(LargeBinary, nullable=True, comment="影像二進位資料")
    
    # 主要情緒
    dominant_emotion = Column(String(50), nullable=False, comment="主要情緒: HAPPY, SAD, ANGRY, CONFUSED, DISGUSTED, SURPRISED, CALM, NEUTRAL")
    dominant_emotion_confidence = Column(Float, nullable=False, comment="主要情緒信心度 (0-100)")
    
    # 詳細情緒分析 (JSON 儲存)
    emotions_json = Column(Text, nullable=True, comment="所有情緒的信心度 (JSON格式)")
    
    # 人臉檢測資訊
    face_count = Column(Integer, default=0, comment="檢測到的臉部數量")
    face_details_json = Column(Text, nullable=True, comment="臉部詳細資訊 (JSON)")
    
    # 其他分析結果
    analysis_result_json = Column(Text, nullable=True, comment="AWS 完整分析結果 (JSON)")
    
    # 狀態與時間
    status = Column(String(20), default="success", comment="分析狀態: success, processing, failed")
    error_message = Column(String(500), nullable=True, comment="錯誤訊息 (若分析失敗)")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="建立時間")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新時間")
    
    def __repr__(self):
        return f"<EmotionAnalysis(id={self.id}, user_id={self.user_id}, dominant_emotion='{self.dominant_emotion}')>"
