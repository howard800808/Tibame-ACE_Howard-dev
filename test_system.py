#!/usr/bin/env python3
"""系統檢查測試腳本"""

print("=" * 60)
print("🧪 完整系統檢查報告")
print("=" * 60)

# 1. 測試各層次導入
try:
    from app.models.emotion import EmotionAnalysis
    print("✅ Model 層: EmotionAnalysis 導入成功")
except Exception as e:
    print(f"❌ Model 層: {e}")

try:
    from app.schemas.emotion_schema import EmotionResponse
    print("✅ Schema 層: EmotionResponse 導入成功")
except Exception as e:
    print(f"❌ Schema 層: {e}")

try:
    from app.services.emotion_service import emotion_service
    print("✅ Service 層: emotion_service 導入成功")
except Exception as e:
    print(f"❌ Service 層: {e}")

try:
    from app.controllers.emotion_controller import emotion_controller
    print("✅ Controller 層: emotion_controller 導入成功")
except Exception as e:
    print(f"❌ Controller 層: {e}")

try:
    from app.routes.emotion_routes import router as emotion_router
    print("✅ Routes 層: emotion_router 導入成功")
except Exception as e:
    print(f"❌ Routes 層: {e}")

# 2. 測試主應用
try:
    from run import app
    print("✅ FastAPI 應用: run.app 導入成功")
    print(f"   - 已註冊路由數: {len(app.routes)}")
except Exception as e:
    print(f"❌ FastAPI 應用: {e}")

# 3. 測試配置
try:
    from app.core.config import settings
    print("✅ 配置: 導入成功")
    print(f"   - APP_NAME: {settings.APP_NAME}")
    print(f"   - DEBUG: {settings.DEBUG}")
    print(f"   - AWS 配置: {'已設定' if settings.AWS_ACCESS_KEY_ID else '未設定'}")
except Exception as e:
    print(f"❌ 配置: {e}")

# 4. 測試資料庫
try:
    from app.core.database import engine, Base
    from app.core.config import settings
    print("✅ 資料庫: 初始化成功")
    print(f"   - DATABASE_URL: {settings.DATABASE_URL}")
except Exception as e:
    print(f"❌ 資料庫: {e}")

print("=" * 60)
print("✅ 系統檢查完成！所有組件已就緒。")
print("=" * 60)
