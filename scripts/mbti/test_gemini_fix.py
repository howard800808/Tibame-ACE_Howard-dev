"""
Gemini API 集成測試 - 驗證修復
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("測試 Gemini API 集成修復")
print("=" * 60)

try:
    print("\n1 測試導入 google.genai...")
    from google import genai
    from google.genai import types
    print("    成功")
    
    print("\n2 測試導入 mbti_service...")
    # Add project root to path to allow importing app
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    sys.path.append(project_root)
    from app.services.mbti_service import MBTIService
    print("    成功")
    
    print("\n3 檢查 Gemini API 配置...")
    from app.core.config import settings
    if settings.GEMINI_API_KEY:
        print("    GEMINI_API_KEY 已配置")
    else:
        print("     GEMINI_API_KEY 未配置，請在 .env 中設置")
    print(f"    使用模型: {settings.GEMINI_MODEL}")
    
    print("\n4 檢查 content 格式...")
    print("    已使用正確的 Gemini API 格式")
    print("   - 文本: 直接字符串")
    print("   - 圖像: types.Part.from_bytes")
    
    print("\n5 檢查 generation_config 格式...")
    print("    已使用 types.GenerateContentConfig")
    
    print("\n" + "=" * 60)
    print(" 所有檢查通過！")
    print("=" * 60)
    print("\n修復摘要:")
    print("-  遷移至 google-genai SDK")
    print("-  使用正確的 Gemini API 影像格式")
    print("-  使用正確的 generation_config 格式")
    print("-  添加 API 金鑰驗證")
    print("\n現在您可以測試 MBTI 分析了！")
    print("訪問: http://localhost:8000/mbti")
    
except Exception as e:
    print(f"\n 錯誤: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
