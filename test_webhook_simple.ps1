# Test 1: Empty webhook request
Write-Host "Test 1: Empty request" -ForegroundColor Cyan
$r1 = Invoke-WebRequest "http://localhost:8000/api/linebot/webhook" -Method POST -ContentType "application/json" -Body '{"events":[]}' -Headers @{"X-Line-Signature"="test"} -UseBasicParsing
Write-Host "Status: $($r1.StatusCode)" -ForegroundColor Green
Write-Host ""

# Test 2: Postback - Accept task
Write-Host "Test 2: Accept Task Postback" -ForegroundColor Cyan
$body2 = '{"events":[{"type":"postback","postback":{"data":"action=task&department=HK&id=task-001&op=accept&room=1205"},"replyToken":"token001"}]}'
$r2 = Invoke-WebRequest "http://localhost:8000/api/linebot/webhook" -Method POST -ContentType "application/json" -Body $body2 -Headers @{"X-Line-Signature"="test"} -UseBasicParsing
Write-Host "Status: $($r2.StatusCode), Response: $($r2.Content)" -ForegroundColor Green
Write-Host ""

# Test 3: Postback - Complete task (should trigger report flow)
Write-Host "Test 3: Complete Task Postback" -ForegroundColor Cyan
$body3 = '{"events":[{"type":"postback","postback":{"data":"action=task&department=HK&id=task-001&op=complete&room=1205"},"replyToken":"token002"}]}'
$r3 = Invoke-WebRequest "http://localhost:8000/api/linebot/webhook" -Method POST -ContentType "application/json" -Body $body3 -Headers @{"X-Line-Signature"="test"} -UseBasicParsing
Write-Host "Status: $($r3.StatusCode), Response: $($r3.Content)" -ForegroundColor Green
Write-Host ""

# Test 4: Postback - Report step 1
Write-Host "Test 4: Report Flow Step 1" -ForegroundColor Cyan
$body4 = '{"events":[{"type":"postback","postback":{"data":"action=report&step=1&id=task-001&ans=yes&room=1205"},"replyToken":"token003"}]}'
$r4 = Invoke-WebRequest "http://localhost:8000/api/linebot/webhook" -Method POST -ContentType "application/json" -Body $body4 -Headers @{"X-Line-Signature"="test"} -UseBasicParsing
Write-Host "Status: $($r4.StatusCode), Response: $($r4.Content)" -ForegroundColor Green
Write-Host ""

Write-Host "All tests completed! Check server logs for [Postback] messages." -ForegroundColor Yellow
