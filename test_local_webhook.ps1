# LINE Bot 本地 Webhook 測試腳本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LINE Bot 本地測試腳本" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 測試 1: 檢查伺服器狀態
Write-Host "[1/5] 檢查伺服器狀態..." -ForegroundColor Yellow
try {
    $diagnostics = Invoke-WebRequest -Uri "http://localhost:8000/api/linebot/diagnostics" -UseBasicParsing
    $json = $diagnostics.Content | ConvertFrom-Json
    Write-Host "  ✅ 伺服器運行中，已初始化 $($json.departments.Count) 個部門`n" -ForegroundColor Green
} catch {
    Write-Host "  ❌ 伺服器未運行或無法連接`n" -ForegroundColor Red
    exit 1
}

# 測試 2: 測試空的 Webhook 請求
Write-Host "[2/5] 測試空的 Webhook 請求..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/linebot/webhook" `
        -Method POST `
        -ContentType "application/json" `
        -Body '{"events":[]}' `
        -Headers @{"X-Line-Signature" = "test_signature"} `
        -UseBasicParsing
    
    Write-Host "  ✅ 空請求測試通過 (狀態碼: $($response.StatusCode))`n" -ForegroundColor Green
} catch {
    Write-Host "  ❌ 空請求測試失敗`n" -ForegroundColor Red
}

# 測試 3: 測試 Postback 事件 - 任務接受
Write-Host "[3/5] 測試 Postback - 接受任務..." -ForegroundColor Yellow
$acceptBody = @{
    events = @(
        @{
            type = "postback"
            postback = @{
                data = "action=task&department=HK&id=test-task-001&op=accept&room=1205"
            }
            replyToken = "test_reply_token_001"
            source = @{
                type = "group"
                groupId = "test_group_hk"
            }
        }
    )
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/linebot/webhook" `
        -Method POST `
        -ContentType "application/json" `
        -Body $acceptBody `
        -Headers @{"X-Line-Signature" = "test_sig_accept"} `
        -UseBasicParsing
    
    Write-Host "  ✅ 接受任務測試完成 (狀態碼: $($response.StatusCode))" -ForegroundColor Green
    Write-Host "  📋 回應: $($response.Content)`n" -ForegroundColor White
} catch {
    Write-Host "  ❌ 接受任務測試失敗: $($_.Exception.Message)`n" -ForegroundColor Red
}

# 測試 4: 測試 Postback 事件 - 完成任務（觸發回報流程）
Write-Host "[4/5] 測試 Postback - 完成任務（應自動啟動回報流程）..." -ForegroundColor Yellow
$completeBody = @{
    events = @(
        @{
            type = "postback"
            postback = @{
                data = "action=task&department=HK&id=test-task-001&op=complete&room=1205"
            }
            replyToken = "test_reply_token_002"
            source = @{
                type = "group"
                groupId = "test_group_hk"
            }
        }
    )
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/linebot/webhook" `
        -Method POST `
        -ContentType "application/json" `
        -Body $completeBody `
        -Headers @{"X-Line-Signature" = "test_sig_complete"} `
        -UseBasicParsing
    
    Write-Host "  ✅ 完成任務測試完成 (狀態碼: $($response.StatusCode))" -ForegroundColor Green
    Write-Host "  📋 回應: $($response.Content)" -ForegroundColor White
    Write-Host "  💡 檢查伺服器日誌，應該看到自動啟動回報流程的訊息`n" -ForegroundColor Cyan
} catch {
    Write-Host "  ❌ 完成任務測試失敗: $($_.Exception.Message)`n" -ForegroundColor Red
}

# 測試 5: 測試回報流程 - 第 1 步回答
Write-Host "[5/5] 測試 Postback - 回報流程第 1 步..." -ForegroundColor Yellow
$reportBody = @{
    events = @(
        @{
            type = "postback"
            postback = @{
                data = "action=report&step=1&id=test-task-001&ans=yes&room=1205"
            }
            replyToken = "test_reply_token_003"
            source = @{
                type = "group"
                groupId = "test_group_hk"
            }
        }
    )
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/linebot/webhook" `
        -Method POST `
        -ContentType "application/json" `
        -Body $reportBody `
        -Headers @{"X-Line-Signature" = "test_sig_report"} `
        -UseBasicParsing
    
    Write-Host "  ✅ 回報流程測試完成 (狀態碼: $($response.StatusCode))" -ForegroundColor Green
    Write-Host "  📋 回應: $($response.Content)" -ForegroundColor White
    Write-Host "  💡 檢查伺服器日誌，應該看到回報流程進度訊息`n" -ForegroundColor Cyan
} catch {
    Write-Host "  ❌ 回報流程測試失敗: $($_.Exception.Message)`n" -ForegroundColor Red
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  測試完成！" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📋 下一步：" -ForegroundColor Yellow
Write-Host "1. 查看伺服器終端的日誌輸出" -ForegroundColor White
Write-Host "2. 確認看到 [Postback] 和 [LINEBot 任務]/[LINEBot 回報] 相關訊息" -ForegroundColor White
Write-Host "3. 如果要在實際 LINE 上測試，請執行廣播命令發送任務卡片`n" -ForegroundColor White
