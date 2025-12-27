#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 get_analysis_detail 函数是否能正确处理数据
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.controllers.video_controller import video_controller
from app.models.video import VideoAnalysis
from app.models.user import User

db = SessionLocal()

try:
    # 查找最新的分析
    latest = db.query(VideoAnalysis).order_by(VideoAnalysis.id.desc()).first()
    
    if latest:
        print(f"✅ 找到分析记录: ID={latest.id}, Status={latest.status}")
        print(f"   转录文字: {latest.transcription_text[:50] if latest.transcription_text else 'None'}...")
        print(f"   转录 JSON (raw): {latest.transcription_json[:60] if latest.transcription_json else 'None'}...")
        
        # 获取用户
        user = db.query(User).filter(User.id == latest.user_id).first()
        
        # 测试 get_analysis_detail 函数
        try:
            response = video_controller.get_analysis_detail(latest.id, user, db)
            print(f"\n✅ get_analysis_detail 成功")
            print(f"   - 转录文字: {response.transcription_text[:50] if response.transcription_text else 'None'}...")
            print(f"   - 转录 JSON 类型: {type(response.transcription_json)}")
            print(f"   - 转录 JSON 长度: {len(response.transcription_json) if response.transcription_json else 0}")
            print(f"   - 说话人数: {response.speaker_count}")
        except Exception as e:
            print(f"\n❌ get_analysis_detail 失败: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("⚠️ 数据库中没有分析记录")
        
        # 查看有多少记录
        count = db.query(VideoAnalysis).count()
        print(f"   总记录数: {count}")
finally:
    db.close()
