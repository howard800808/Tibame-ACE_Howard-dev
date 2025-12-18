# LINE Bot 廣播問題診斷腳本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LINE Bot 廣播診斷" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 1. 檢查伺服器
Write-Host "[1/5] 檢查伺服器狀態..." -ForegroundColor Yellow
$proc = Get-Process python* -ErrorAction SilentlyContinue | Where-Object {$_.Id -eq 14992}
if ($proc) {
    Write-Host "  OK - 伺服器運行中 (PID: $($proc.Id))" -ForegroundColor Green
} else {
    Write-Host "  FAIL - 伺服器未運行" -ForegroundColor Red
    exit 1
}

# 2. 檢查診斷端點
Write-Host "`n[2/5] 檢查診斷資訊..." -ForegroundColor Yellow
try {
    $diag = Invoke-WebRequest "http://localhost:8000/api/linebot/diagnostics" -UseBasicParsing
    $diagJson = $diag.Content | ConvertFrom-Json
    Write-Host "  OK - 診斷端點正常，部門數: $($diagJson.departments.Count)" -ForegroundColor Green
} catch {
    Write-Host "  FAIL - 無法訪問: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 3. 檢查 Token
Write-Host "`n[3/5] 檢查 Channel Access Token..." -ForegroundColor Yellow
$hasToken = 0
$noToken = 0
foreach ($dept in $diagJson.departments) {
    if ($dept.channel_access_token -and $dept.channel_access_token -ne "" -and $dept.channel_access_token -ne "null") {
        $hasToken++
    } else {
        $noToken++
        Write-Host "  - $($dept.code) ($($dept.name)): 無 Token" -ForegroundColor Red
    }
}
Write-Host "  有 Token: $hasToken, 無 Token: $noToken" -ForegroundColor $(if ($noToken -eq 0) {"Green"} else {"Red"})

# 4. 測試單個廣播
Write-Host "`n[4/5] 測試單個部門廣播 (HK)..." -ForegroundColor Yellow
try {
    $test = Invoke-WebRequest -Method POST "http://localhost:8000/api/linebot/demo/HK/task" -UseBasicParsing -TimeoutSec 15
    Write-Host "  OK - 狀態碼: $($test.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "  FAIL: $($_.Exception.Message)" -ForegroundColor Red
}

# 5. 完整廣播
Write-Host "`n[5/5] 執行完整廣播..." -ForegroundColor Yellow
try {
    $bc = Invoke-WebRequest -Method POST "http://localhost:8000/api/linebot/demo/all/tasks" -UseBasicParsing -TimeoutSec 60
    $bcJson = $bc.Content | ConvertFrom-Json
    
    $success = ($bcJson.broadcasted | Where-Object {$_.sent -eq $true}).Count
    Write-Host "  成功: $success / $($bcJson.broadcasted.Count)" -ForegroundColor $(if ($success -gt 0) {"Green"} else {"Red"})
    
    Write-Host "`n結果明細：" -ForegroundColor Cyan
    $bcJson.broadcasted | Format-Table code, name, sent -AutoSize
    
} catch {
    Write-Host "  FAIL: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "如果失敗，請檢查 run.py 終端的日誌" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan
