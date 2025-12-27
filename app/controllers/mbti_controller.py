import os
import tempfile
from typing import Dict
from fastapi import UploadFile, File
from app.services.mbti_service import mbti_service


class MBTIController:
    """MBTI 預測控制層 - 處理影片上傳和分析邏輯"""
    
    @staticmethod
    async def analyze_video(file: UploadFile = File(...)) -> Dict:
        """
        上傳影片並進行 MBTI 分析
        
        Args:
            file: 上傳的影片檔案
            
        Returns:
            MBTI 預測結果
        """
        temp_path = None
        try:
            print(f"\n【收到檔案上傳】")
            print(f"  檔案名: {file.filename}")
            print(f"  Content-Type: {file.content_type}")
            print(f"  Size: {file.size}")
            
            # 驗證檔案類型 (更寬鬆的檢查)
            allowed_types = [
                'video/mp4', 
                'video/mpeg', 
                'video/quicktime', 
                'video/x-msvideo', 
                'video/webm',
                'video/x-m4v',
                'video/3gpp',
                'video/x-flv'
            ]
            
            # 如果 content_type 為空，則根據檔案名判斷
            if not file.content_type or file.content_type not in allowed_types:
                # 根據副檔名判斷
                filename_lower = file.filename.lower() if file.filename else ""
                valid_extensions = ['.mp4', '.mov', '.avi', '.webm', '.mkv', '.flv', '.3gp', '.m4v']
                has_valid_extension = any(filename_lower.endswith(ext) for ext in valid_extensions)
                
                if not has_valid_extension and file.content_type:
                    print(f"【警告】檔案類型不支援: {file.content_type}")
                    raise ValueError(f"不支援的影片格式: {file.content_type}. 請上傳 MP4, MOV, AVI, WebM 或 MKV 檔案")
            
            # 讀取檔案內容
            content = await file.read()
            file_size = len(content)
            
            print(f"  實際大小: {file_size / 1024 / 1024:.2f} MB")
            
            # 驗證檔案大小 (最大 500MB)
            max_size = 500 * 1024 * 1024  # 500MB
            if file_size > max_size:
                print(f"【錯誤】檔案過大: {file_size / 1024 / 1024:.2f}MB")
                raise ValueError(f"檔案過大: {file_size / 1024 / 1024:.2f}MB. 最大限制為 500MB")
            
            # 驗證檔案不為空
            if file_size == 0:
                print(f"【錯誤】檔案為空")
                raise ValueError("上傳的檔案為空，請選擇有效的影片")
            
            # 將上傳的檔案保存到臨時目錄
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
                tmp_file.write(content)
                temp_path = tmp_file.name
            
            print(f"  臨時檔案: {temp_path}")
            print(f"【開始分析】")
            
            # 進行 MBTI 分析
            result = mbti_service.predict_mbti(temp_path)
            
            print(f"【分析完成】")
            return {
                "success": True,
                "data": result
            }
            
        except ValueError as e:
            error_msg = str(e)
            print(f"【驗證錯誤】{error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = str(e)
            print(f"【分析異常】{error_msg}")
            import traceback
            traceback.print_exc()
            raise Exception(f"分析失敗: {error_msg}")
        finally:
            # 清理臨時檔案
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                    print(f"【清理臨時檔案】{temp_path}")
                except Exception as e:
                    print(f"【警告】無法刪除臨時檔案: {str(e)}")
                except:
                    pass
    
    @staticmethod
    async def analyze_emotion(file: UploadFile = File(...)) -> Dict:
        """
        上傳影片並進行表情情緒分析
        
        Args:
            file: 上傳的影片檔案
            
        Returns:
            表情情緒分析結果
        """
        temp_path = None
        try:
            print(f"\n【收到表情情緒分析請求】")
            print(f"  檔案名: {file.filename}")
            print(f"  Content-Type: {file.content_type}")
            print(f"  Size: {file.size}")
            
            # 驗證檔案類型
            allowed_types = [
                'video/mp4', 
                'video/mpeg', 
                'video/quicktime', 
                'video/x-msvideo', 
                'video/webm',
                'video/x-m4v',
                'video/3gpp',
                'video/x-flv'
            ]
            
            if not file.content_type or file.content_type not in allowed_types:
                filename_lower = file.filename.lower() if file.filename else ""
                valid_extensions = ['.mp4', '.mov', '.avi', '.webm', '.mkv', '.flv', '.3gp', '.m4v']
                has_valid_extension = any(filename_lower.endswith(ext) for ext in valid_extensions)
                
                if not has_valid_extension and file.content_type:
                    raise ValueError(f"不支援的影片格式: {file.content_type}. 請上傳 MP4, MOV, AVI, WebM 或 MKV 檔案")
            
            # 讀取檔案內容
            content = await file.read()
            file_size = len(content)
            
            print(f"  實際大小: {file_size / 1024 / 1024:.2f} MB")
            
            # 驗證檔案大小
            max_size = 500 * 1024 * 1024  # 500MB
            if file_size > max_size:
                raise ValueError(f"檔案過大: {file_size / 1024 / 1024:.2f}MB. 最大限制為 500MB")
            
            # 驗證檔案不為空
            if file_size == 0:
                raise ValueError("上傳的檔案為空，請選擇有效的影片")
            
            # 將上傳的檔案保存到臨時目錄
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
                tmp_file.write(content)
                temp_path = tmp_file.name
            
            print(f"  臨時檔案: {temp_path}")
            print(f"【開始表情情緒分析】")
            
            # 進行表情情緒分析 - 返回模擬數據
            # 實際應用中可以集成 OpenCV 或 DeepFace 等庫進行真實分析
            emotion_result = mbti_service.analyze_emotion(temp_path)
            
            print(f"【表情情緒分析完成】")
            return {
                "success": True,
                "data": emotion_result
            }
            
        except ValueError as e:
            error_msg = str(e)
            print(f"【驗證錯誤】{error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = str(e)
            print(f"【分析異常】{error_msg}")
            import traceback
            traceback.print_exc()
            raise Exception(f"表情情緒分析失敗: {error_msg}")
        finally:
            # 清理臨時檔案
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                    print(f"【清理臨時檔案】{temp_path}")
                except Exception as e:
                    print(f"【警告】無法刪除臨時檔案: {str(e)}")
                except:
                    pass


# 建立全域控制器實例
mbti_controller = MBTIController()
