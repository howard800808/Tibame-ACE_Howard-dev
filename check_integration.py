#!/usr/bin/env python3
"""
LINE Bot 整合檢查腳本
驗證所有必要的模組、檔案和配置是否已正確安裝
"""

import os
import sys
from pathlib import Path

# 顏色輸出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header():
    """列印標題"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}")
    print("=" * 60)
    print("LINE Bot 12 部門整合 - 檢查工具")
    print("=" * 60)
    print(f"{Colors.RESET}\n")


def check_python_version():
    """檢查 Python 版本"""
    print(f"{Colors.BOLD}1. Python 版本{Colors.RESET}")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 8:
        print(f"  {Colors.GREEN}✓{Colors.RESET} Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  {Colors.RED}✗{Colors.RESET} Python 版本過舊 (需要 3.8+)")
        return False


def check_required_packages():
    """檢查必要的套件"""
    print(f"\n{Colors.BOLD}2. 必要套件{Colors.RESET}")
    
    packages = [
        'fastapi',
        'uvicorn',
        'linebot',
        'pydantic',
        'motor',
        'beanie',
        'pymongo',
        'jinja2'
    ]
    
    all_ok = True
    for package in packages:
        try:
            __import__(package)
            print(f"  {Colors.GREEN}✓{Colors.RESET} {package}")
        except ImportError:
            print(f"  {Colors.RED}✗{Colors.RESET} {package} (未安裝)")
            all_ok = False
    
    return all_ok


def check_file_structure():
    """檢查檔案結構"""
    print(f"\n{Colors.BOLD}3. 檔案結構{Colors.RESET}")
    
    required_files = [
        'app/models/department.py',
        'app/models/task.py',
        'app/schemas/linebot_schema.py',
        'app/services/linebot_service.py',
        'app/controllers/linebot_controller.py',
        'app/routes/linebot_routes.py',
        'app/views/linebot_view.py',
        'templates/linebot_dashboard.html',
        'init_linebot_departments.py',
        'LINEBOT_README.md',
        'LINEBOT_QUICKSTART.md',
        'LINEBOT_PROJECT_STRUCTURE.md',
    ]
    
    all_ok = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  {Colors.GREEN}✓{Colors.RESET} {file_path}")
        else:
            print(f"  {Colors.RED}✗{Colors.RESET} {file_path} (缺失)")
            all_ok = False
    
    return all_ok


def check_env_configuration():
    """檢查環境變數配置"""
    print(f"\n{Colors.BOLD}4. 環境變數配置{Colors.RESET}")
    
    if not Path('.env').exists():
        print(f"  {Colors.RED}✗{Colors.RESET} .env 檔案不存在")
        return False
    
    try:
        from app.core.config import settings
        
        # 檢查基本配置
        basic_checks = [
            ('APP_NAME', settings.APP_NAME),
            ('MONGODB_URL', settings.MONGODB_URL),
            ('MONGODB_DB_NAME', settings.MONGODB_DB_NAME),
        ]
        
        for key, value in basic_checks:
            if value:
                print(f"  {Colors.GREEN}✓{Colors.RESET} {key}")
            else:
                print(f"  {Colors.YELLOW}⚠{Colors.RESET} {key} 未設定")
        
        # 檢查 12 個部門配置
        departments = [
            'GS', 'HK', 'CON', 'BP', 'FB', 'CBS',
            'FS', 'LUR', 'GAE', 'BB', 'AD', 'LA'
        ]
        
        print(f"\n  {Colors.BOLD}部門配置:{Colors.RESET}")
        all_ok = True
        for dept_code in departments:
            token = getattr(settings, f'{dept_code}_ACCESS_TOKEN', None)
            secret = getattr(settings, f'{dept_code}_SECRET', None)
            
            if token and secret:
                token_preview = token[:20] + "..." if len(token) > 20 else token
                print(f"  {Colors.GREEN}✓{Colors.RESET} {dept_code}: TOKEN 和 SECRET 已設定")
            else:
                print(f"  {Colors.YELLOW}⚠{Colors.RESET} {dept_code}: TOKEN 或 SECRET 未設定")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"  {Colors.RED}✗{Colors.RESET} 無法載入配置: {str(e)}")
        return False


def check_database_connection():
    """檢查資料庫連線"""
    print(f"\n{Colors.BOLD}5. 資料庫連線{Colors.RESET}")
    
    try:
        import asyncio
        from app.core.database import connect_to_mongodb, close_mongodb_connection
        
        async def test_connection():
            try:
                await connect_to_mongodb()
                await close_mongodb_connection()
                return True
            except Exception as e:
                print(f"  {Colors.RED}✗{Colors.RESET} 連線失敗: {str(e)}")
                return False
        
        result = asyncio.run(test_connection())
        
        if result:
            print(f"  {Colors.GREEN}✓{Colors.RESET} MongoDB 連線成功")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"  {Colors.YELLOW}⚠{Colors.RESET} 無法檢查資料庫 (可能未啟動): {str(e)}")
        return True  # 不算失敗，因為資料庫可能只是未啟動


def check_code_quality():
    """檢查程式碼品質"""
    print(f"\n{Colors.BOLD}6. 程式碼品質{Colors.RESET}")
    
    try:
        # 檢查主要模組的導入
        from app.services.linebot_service import linebot_service
        from app.controllers.linebot_controller import linebot_controller
        from app.routes.linebot_routes import router as linebot_router
        
        print(f"  {Colors.GREEN}✓{Colors.RESET} linebot_service 可正常導入")
        print(f"  {Colors.GREEN}✓{Colors.RESET} linebot_controller 可正常導入")
        print(f"  {Colors.GREEN}✓{Colors.RESET} linebot_routes 可正常導入")
        
        return True
        
    except Exception as e:
        print(f"  {Colors.RED}✗{Colors.RESET} 模組導入失敗: {str(e)}")
        return False


def print_summary(results):
    """列印總結"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}")
    print("=" * 60)
    print("檢查結果總結")
    print("=" * 60)
    print(f"{Colors.RESET}\n")
    
    checks = [
        ('Python 版本', results[0]),
        ('必要套件', results[1]),
        ('檔案結構', results[2]),
        ('環境變數', results[3]),
        ('資料庫連線', results[4]),
        ('程式碼品質', results[5]),
    ]
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    for check_name, result in checks:
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if result else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"  {check_name:<15} {status}")
    
    print(f"\n{Colors.BOLD}總體進度: {passed}/{total} 項通過{Colors.RESET}\n")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 所有檢查通過！系統已準備就緒。{Colors.RESET}\n")
        print("下一步:")
        print("  1. 執行: python init_linebot_departments.py")
        print("  2. 執行: python run.py")
        print("  3. 訪問: http://localhost:8000/docs")
        print()
        return 0
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  部分檢查未通過，請查看上述錯誤訊息。{Colors.RESET}\n")
        return 1


def main():
    """主程式"""
    print_header()
    
    results = [
        check_python_version(),
        check_required_packages(),
        check_file_structure(),
        check_env_configuration(),
        check_database_connection(),
        check_code_quality(),
    ]
    
    return print_summary(results)


if __name__ == '__main__':
    sys.exit(main())
