# FFmpeg 自動安裝腳本 (Windows)
# 使用方式: 以管理員運行 PowerShell，執行: Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process; .\install_ffmpeg.ps1

Write-Host "FFmpeg Installation Script" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# 1. 檢查 Chocolatey
Write-Host "檢查 Chocolatey..." -ForegroundColor Yellow
$chocoPath = (Get-Command choco -ErrorAction SilentlyContinue).Source

if ($chocoPath) {
    Write-Host "已找到 Chocolatey，開始安裝 FFmpeg..." -ForegroundColor Green
    & choco install ffmpeg -y
    Write-Host "FFmpeg 安裝完成！" -ForegroundColor Green
}
else {
    Write-Host "Chocolatey 未安裝。嘗試手動下載..." -ForegroundColor Yellow
    
    # 2. 手動下載 FFmpeg (使用 BinTray)
    $ffmpegZip = "$env:TEMP\ffmpeg-release-full.zip"
    $ffmpegDir = "C:\ffmpeg"
    
    Write-Host "下載 FFmpeg (可能需要幾分鐘)..." -ForegroundColor Yellow
    
    # 使用 WebClient 下載 (支持更廣泛)
    $url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        (New-Object Net.WebClient).DownloadFile($url, $ffmpegZip)
        Write-Host "下載完成！" -ForegroundColor Green
        
        # 3. 解壓
        Write-Host "解壓 FFmpeg..." -ForegroundColor Yellow
        Expand-Archive $ffmpegZip -DestinationPath $env:TEMP -Force
        
        # 4. 移動到 C:\ffmpeg
        if (-not (Test-Path $ffmpegDir)) {
            New-Item -ItemType Directory -Path $ffmpegDir | Out-Null
        }
        
        $extractedDir = Get-ChildItem $env:TEMP -Directory -Filter "*ffmpeg*" | Select-Object -First 1
        if ($extractedDir) {
            Copy-Item "$($extractedDir.FullName)\bin\*" "$ffmpegDir\" -Force
            Write-Host "FFmpeg 已複製到 $ffmpegDir" -ForegroundColor Green
        }
        
        # 5. 添加到環境變數
        Write-Host "添加到環境變數..." -ForegroundColor Yellow
        $env:Path += ";$ffmpegDir"
        [Environment]::SetEnvironmentVariable("Path", $env:Path, "User")
        
        Write-Host "FFmpeg 已添加到系統 PATH" -ForegroundColor Green
        
        # 清理
        Remove-Item $ffmpegZip -Force -ErrorAction SilentlyContinue
        
    } catch {
        Write-Host "下載失敗: $_" -ForegroundColor Red
        Write-Host "請手動下載: https://ffmpeg.org/download.html#build-windows" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "驗證安裝..." -ForegroundColor Yellow
$ffmpegTest = ffmpeg -version 2>$null
if ($ffmpegTest) {
    Write-Host "✅ FFmpeg 已成功安裝！" -ForegroundColor Green
    ffmpeg -version | Select-Object -First 1
} else {
    Write-Host "❌ FFmpeg 驗證失敗，請重新啟動 PowerShell 或電腦後重試。" -ForegroundColor Red
}
