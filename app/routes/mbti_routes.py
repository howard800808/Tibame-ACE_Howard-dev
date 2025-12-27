from fastapi import APIRouter, UploadFile, File, status, HTTPException
from fastapi.responses import JSONResponse
from app.controllers.mbti_controller import mbti_controller

router = APIRouter(prefix="/mbti", tags=["MBTI分析"])


@router.post("/test-upload", status_code=status.HTTP_200_OK)
async def test_upload(file: UploadFile = File(...)):
    """
    測試上傳端點 - 用於診斷檔案上傳問題
    """
    try:
        print("\n" + "="*80)
        print("【測試上傳】")
        print(f"  檔案名: {file.filename}")
        print(f"  檔案類型: {file.content_type}")
        print(f"  檔案大小: {file.size} bytes")
        
        # 讀取檔案內容
        content = await file.read()
        content_length = len(content)
        
        print(f"  實際讀取大小: {content_length} bytes")
        print(f"  檔案前 20 字節: {content[:20]}")
        
        print("【測試成功】")
        print("="*80 + "\n")
        
        return {
            "success": True,
            "message": "上傳成功",
            "filename": file.filename,
            "content_type": file.content_type,
            "size": content_length
        }
        
    except Exception as e:
        print(f"【測試失敗】{str(e)}")
        print("="*80 + "\n")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": str(e)
            }
        )


@router.post("/analyze", status_code=status.HTTP_200_OK)
async def analyze_video_mbti(file: UploadFile = File(...)):
    """
    上傳影片並分析人物行為特徵，預測 MBTI 類型
    
    - **file**: 影片檔案 (支援 MP4, MOV, AVI, WebM)
    
    Returns:
        - **success**: 是否成功
        - **data**: MBTI 預測結果，包含：
            - mbti_type: 預測的 MBTI 類型
            - confidence: 信心度 (0-100)
            - analysis: 各維度的詳細分析
            - behavioral_traits: 觀察到的行為特徵
            - recommendations: 針對該類型的建議
    """
    try:
        print("\n" + "="*80)
        print("【接收到上傳請求】")
        print(f"  檔案名: {file.filename}")
        print(f"  檔案類型: {file.content_type}")
        print(f"  檔案大小: {file.size} bytes")
        
        # 驗證檔案是否存在
        if not file:
            print("【錯誤】沒有收到檔案")
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "沒有上傳檔案"
                }
            )
        
        if not file.filename:
            print("【錯誤】檔案名為空")
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "檔案名為空"
                }
            )
        
        result = await mbti_controller.analyze_video(file)
        
        print("【分析成功】返回結果")
        print("="*80 + "\n")
        return result
        
    except ValueError as e:
        error_msg = str(e)
        print(f"【驗證錯誤】{error_msg}")
        print("="*80 + "\n")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": error_msg
            }
        )
    except Exception as e:
        error_msg = str(e)
        print(f"【分析異常】{error_msg}")
        import traceback
        traceback.print_exc()
        print("="*80 + "\n")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"分析失敗: {error_msg}"
            }
        )

@router.post("/analyze-emotion", status_code=status.HTTP_200_OK)
async def analyze_emotion(file: UploadFile = File(...)):
    """
    上傳影片並分析表情情緒
    
    - **file**: 影片檔案 (支援 MP4, MOV, AVI, WebM)
    
    Returns:
        - **success**: 是否成功
        - **data**: 表情情緒分析結果，包含：
            - emotions: 各種表情的識別率 (開心、悲傷、憤怒等)
    """
    try:
        print("\n" + "="*80)
        print("【接收到表情情緒分析請求】")
        print(f"  檔案名: {file.filename}")
        print(f"  檔案類型: {file.content_type}")
        print(f"  檔案大小: {file.size} bytes")
        
        # 驗證檔案是否存在
        if not file:
            print("【錯誤】沒有收到檔案")
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "沒有上傳檔案"
                }
            )
        
        if not file.filename:
            print("【錯誤】檔案名為空")
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "檔案名為空"
                }
            )
        
        result = await mbti_controller.analyze_emotion(file)
        
        print("【表情情緒分析成功】返回結果")
        print("="*80 + "\n")
        return result
        
    except ValueError as e:
        error_msg = str(e)
        print(f"【驗證錯誤】{error_msg}")
        print("="*80 + "\n")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": error_msg
            }
        )
    except Exception as e:
        error_msg = str(e)
        print(f"【分析異常】{error_msg}")
        import traceback
        traceback.print_exc()
        print("="*80 + "\n")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"表情情緒分析失敗: {error_msg}"
            }
        )
