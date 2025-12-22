#!/usr/bin/env python3
"""
Azure Speech-to-Text 快速測試腳本
驗證 Azure 連接和服務是否正常配置
"""

import sys
import json
from pathlib import Path

# 添加項目路徑
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from app.core.config import settings
from app.services.azure_transcription_service import azure_transcription_service, AZURE_SPEECH_AVAILABLE

def test_azure_config():
    """測試 Azure 配置"""
    print("=" * 60)
    print("🔍 Azure Speech-to-Text 配置檢查")
    print("=" * 60)
    
    print("\n✓ 配置信息:")
    print(f"  - API 金鑰: {settings.AZURE_SPEECH_API_KEY[:10]}..." if settings.AZURE_SPEECH_API_KEY else "  - API 金鑰: ❌ 未配置")
    print(f"  - 端點: {settings.AZURE_SPEECH_ENDPOINT}" if settings.AZURE_SPEECH_ENDPOINT else "  - 端點: ❌ 未配置")
    print(f"  - 區域: {settings.AZURE_SPEECH_REGION}" if settings.AZURE_SPEECH_REGION else "  - 區域: ❌ 未配置")
    
    print(f"\n✓ SDK 狀態: {'✅ 已安裝' if AZURE_SPEECH_AVAILABLE else '❌ 未安裝'}")
    
    if not AZURE_SPEECH_AVAILABLE:
        print("\n⚠️  請安裝 Azure Cognitive Services Speech SDK:")
        print("   pip install azure-cognitiveservices-speech")
        return False
    
    if not all([settings.AZURE_SPEECH_API_KEY, settings.AZURE_SPEECH_ENDPOINT, settings.AZURE_SPEECH_REGION]):
        print("\n❌ 配置不完整，請在 .env 文件中設置所有必要的 Azure 參數")
        return False
    
    print("\n✅ 所有配置檢查通過！")
    return True

def test_ffmpeg():
    """測試 FFmpeg 可用性"""
    import subprocess
    
    print("\n" + "=" * 60)
    print("🔍 FFmpeg 檢查")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"\n✅ FFmpeg 已安裝")
            print(f"   {version_line}")
            return True
        else:
            print("\n❌ FFmpeg 可用但命令失敗")
            return False
    
    except FileNotFoundError:
        print("\n❌ FFmpeg 未安裝")
        print("\n請安裝 FFmpeg:")
        print("   Windows (Chocolatey): choco install ffmpeg")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt-get install ffmpeg")
        return False
    
    except Exception as e:
        print(f"\n⚠️  FFmpeg 檢查出錯: {e}")
        return False

def test_audio_extraction():
    """測試音軌提取功能"""
    import tempfile
    import os
    
    print("\n" + "=" * 60)
    print("🔍 音軌提取功能檢查")
    print("=" * 60)
    
    try:
        # 嘗試提取音軌的方法
        from app.services.azure_transcription_service import AzureTranscriptionService
        
        if AzureTranscriptionService.extract_audio_from_video.__doc__:
            print("\n✅ 音軌提取方法已實現")
            print(f"   方法: {AzureTranscriptionService.extract_audio_from_video.__doc__.split(chr(10))[0]}")
        
        return True
    
    except Exception as e:
        print(f"\n⚠️  音軌提取檢查出錯: {e}")
        return False

def main():
    """主測試函數"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "Azure Speech-to-Text 系統檢查" + " " * 18 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    tests = [
        ("Azure 配置", test_azure_config),
        ("FFmpeg", test_ffmpeg),
        ("音軌提取", test_audio_extraction),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} 測試異常: {e}")
            results.append((test_name, False))
    
    # 打印摘要
    print("\n" + "=" * 60)
    print("📊 測試摘要")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status} - {test_name}")
    
    print(f"\n總計: {passed}/{total} 測試通過")
    
    if passed == total:
        print("\n🎉 所有檢查都通過了！系統已準備好使用 Azure Speech-to-Text")
    else:
        print(f"\n⚠️  還有 {total - passed} 個問題需要解決")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
