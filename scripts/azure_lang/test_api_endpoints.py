#!/usr/bin/env python3
"""
API 功能测试脚本
验证关键端点是否正常工作
"""

import requests
import json
import time
from pathlib import Path

# API 基础 URL
BASE_URL = "http://127.0.0.1:8000"

# 测试凭证
TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpassword123"
TEST_EMAIL = "test@example.com"

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None
    
    def log(self, message: str):
        """打印日志"""
        print(f"[INFO] {message}")
    
    def log_success(self, message: str):
        """打印成功日志"""
        print(f"✅ {message}")
    
    def log_error(self, message: str):
        """打印错误日志"""
        print(f"❌ {message}")
    
    def test_health(self):
        """测试应用健康状态"""
        print("\n" + "="*60)
        print("🔍 测试 1: 应用健康检查")
        print("="*60)
        
        try:
            response = self.session.get(f"{BASE_URL}/")
            if response.status_code == 200:
                self.log_success("应用正常运行")
                return True
            else:
                self.log_error(f"应用返回状态码 {response.status_code}")
                return False
        except Exception as e:
            self.log_error(f"无法连接到应用: {str(e)}")
            return False
    
    def test_login(self):
        """测试登录功能"""
        print("\n" + "="*60)
        print("🔍 测试 2: 用户认证")
        print("="*60)
        
        # 先尝试用已存在的用户登录 (demo用户)
        login_data = {
            "username": "demo",
            "password": "demo123"
        }
        
        try:
            response = self.session.post(
                f"{BASE_URL}/api/auth/login/json",
                json=login_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.log_success(f"用户认证成功，获得 Token")
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                return True
            else:
                self.log_error(f"登录失败: {response.status_code} - {response.text[:100]}")
                return False
        except Exception as e:
            self.log_error(f"登录异常: {str(e)}")
            return False
    
    def test_video_routes(self):
        """测试视频分析路由"""
        print("\n" + "="*60)
        print("🔍 测试 3: 视频分析路由")
        print("="*60)
        
        if not self.token:
            self.log_error("没有有效的 Token，跳过此测试")
            return False
        
        try:
            # 测试获取分析历史
            response = self.session.get(f"{BASE_URL}/api/videos/history")
            
            if response.status_code == 200:
                data = response.json()
                self.log_success(f"获取分析历史成功 (共 {data.get('total_count', 0)} 条)")
                return True
            else:
                self.log_error(f"获取分析历史失败: {response.status_code}")
                return False
        except Exception as e:
            self.log_error(f"获取分析历史异常: {str(e)}")
            return False
    
    def test_config(self):
        """测试 Azure 配置"""
        print("\n" + "="*60)
        print("🔍 测试 4: Azure 配置检查")
        print("="*60)
        
        try:
            from app.core.config import settings
            
            has_api_key = bool(settings.AZURE_SPEECH_API_KEY)
            has_endpoint = bool(settings.AZURE_SPEECH_ENDPOINT)
            has_region = bool(settings.AZURE_SPEECH_REGION)
            
            self.log(f"Azure Speech API Key: {'✓' if has_api_key else '✗'}")
            self.log(f"Azure Speech Endpoint: {'✓' if has_endpoint else '✗'}")
            self.log(f"Azure Speech Region: {'✓' if has_region else '✗'}")
            
            if has_api_key and has_endpoint and has_region:
                self.log_success("Azure 配置完整")
                return True
            else:
                self.log_error("Azure 配置不完整")
                return False
        except Exception as e:
            self.log_error(f"检查配置异常: {str(e)}")
            return False
    
    def test_azure_service(self):
        """测试 Azure 服务导入"""
        print("\n" + "="*60)
        print("🔍 测试 5: Azure 服务导入")
        print("="*60)
        
        try:
            from app.services.azure_transcription_service import azure_transcription_service, AZURE_SPEECH_AVAILABLE
            
            self.log(f"Azure Speech SDK 可用: {AZURE_SPEECH_AVAILABLE}")
            
            if azure_transcription_service:
                self.log_success("Azure Transcription Service 已初始化")
                return True
            else:
                self.log_error("Azure Transcription Service 初始化失败")
                return False
        except Exception as e:
            self.log_error(f"导入服务异常: {str(e)}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n")
        print("╔" + "═"*58 + "╗")
        print("║" + " "*15 + "FastAPI 应用功能测试" + " "*22 + "║")
        print("╚" + "═"*58 + "╝")
        
        results = []
        
        # 运行各项测试
        tests = [
            ("应用健康检查", self.test_health),
            ("用户认证", self.test_login),
            ("视频分析路由", self.test_video_routes),
            ("Azure 配置", self.test_config),
            ("Azure 服务", self.test_azure_service),
        ]
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                self.log_error(f"{test_name} 测试异常: {str(e)}")
                results.append((test_name, False))
        
        # 打印摘要
        print("\n" + "="*60)
        print("📊 测试摘要")
        print("="*60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{status} - {test_name}")
        
        print(f"\n总计: {passed}/{total} 测试通过")
        
        if passed == total:
            print("\n🎉 所有测试都通过了！系统已准备好使用。")
        else:
            print(f"\n⚠️  还有 {total - passed} 个问题需要解决。")
        
        return passed == total

if __name__ == "__main__":
    tester = APITester()
    success = tester.run_all_tests()
    exit(0 if success else 1)
