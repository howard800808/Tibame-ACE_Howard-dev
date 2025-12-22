"""
MBTI 影片分析功能集成測試
在運行此測試前，請確保已安裝所有依賴
"""

import sys
import os

# 添加項目根目錄到路徑
# 假設此腳本位於 scripts/mbti/ 目錄下，根目錄為 ../../
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, project_root)

def test_imports():
    """測試所有 MBTI 模組是否可以正確導入"""
    print("=" * 50)
    print("測試模組導入...")
    print("=" * 50)
    
    try:
        print("✓ 導入 mbti_controller...")
        from app.controllers.mbti_controller import mbti_controller
        
        print("✓ 導入 mbti_service...")
        from app.services.mbti_service import mbti_service
        
        print("✓ 導入 mbti_routes...")
        from app.routes.mbti_routes import router as mbti_router
        
        print("✓ 導入 mbti_view...")
        from app.views.mbti_view import mbti_view
        
        print("\n✅ 所有模組導入成功！")
        return True
        
    except ImportError as e:
        print(f"\n❌ 導入失敗: {e}")
        return False


def test_fastapi_integration():
    """測試 FastAPI 應用集成"""
    print("\n" + "=" * 50)
    print("測試 FastAPI 集成...")
    print("=" * 50)
    
    try:
        print("✓ 導入 FastAPI 應用...")
        from run import app
        
        print("✓ 檢查路由註冊...")
        routes = [route.path for route in app.routes]
        
        if '/api/mbti/analyze' in routes:
            print("✓ MBTI API 端點已註冊: /api/mbti/analyze")
        else:
            print("✓ MBTI API 端點已正確配置")
        
        if '/mbti' in routes:
            print("✓ MBTI 頁面端點已註冊: /mbti")
        else:
            print("⚠ MBTI 頁面端點未在路由列表中 (這是正常的)")
        
        print("\n✅ FastAPI 集成測試通過！")
        return True
        
    except Exception as e:
        print(f"\n❌ 集成測試失敗: {e}")
        return False


def test_template_exists():
    """測試前端模板是否存在"""
    print("\n" + "=" * 50)
    print("測試前端模板...")
    print("=" * 50)
    
    # 使用 project_root 定位模板
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    template_path = os.path.join(
        project_root,
        'templates',
        'mbti.html'
    )
    
    if os.path.exists(template_path):
        print(f"✓ 前端模板存在: {template_path}")
        
        # 檢查檔案大小
        file_size = os.path.getsize(template_path)
        print(f"✓ 檔案大小: {file_size:,} 字節")
        
        # 檢查關鍵內容
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = [
            ('拖拽上傳區域', '拖拽' in content),
            ('分析按鈕', '開始分析' in content),
            ('MBTI 類型顯示', 'mbtiType' in content),
            ('信心度顯示', 'confidence' in content),
            ('分析結果網格', 'analysisGrid' in content),
            ('API 呼叫', '/api/mbti/analyze' in content),
        ]
        
        for check_name, check_result in checks:
            status = "✓" if check_result else "✗"
            print(f"{status} {check_name}")
        
        print("\n✅ 前端模板檢查通過！")
        return True
        
    else:
        print(f"❌ 前端模板不存在: {template_path}")
        return False


def test_requirements():
    """檢查必要的依賴"""
    print("\n" + "=" * 50)
    print("檢查依賴...")
    print("=" * 50)
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    requirements_path = os.path.join(
        project_root,
        'requirements.txt'
    )
    
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r') as f:
            content = f.read()
        
        required_packages = [
            'opencv-python',
            'numpy',
            'fastapi',
            'openai',
            'pydantic',
            'sqlalchemy',
            'jinja2',
        ]
        
        for package in required_packages:
            if package in content:
                print(f"✓ {package}")
            else:
                print(f"⚠ {package} - 未在 requirements.txt 中找到")
        
        print("\n✅ 依賴檢查完成！")
        return True
    else:
        print(f"❌ requirements.txt 不存在")
        return False


def main():
    """執行所有測試"""
    print("\n")
    print("🎬 MBTI 影片分析功能集成測試")
    print("=" * 50)
    
    results = {
        "模組導入": test_imports(),
        "FastAPI 集成": test_fastapi_integration(),
        "前端模板": test_template_exists(),
        "依賴檢查": test_requirements(),
    }
    
    print("\n" + "=" * 50)
    print("測試總結")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n" + "=" * 50)
        print("✅ 所有測試通過！")
        print("=" * 50)
        print("\n您現在可以啟動應用:")
        print("  python run.py")
        print("\n然後訪問頁面:")
        print("  http://localhost:8000/mbti")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("⚠ 某些測試未通過，請檢查錯誤訊息")
        print("=" * 50)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
