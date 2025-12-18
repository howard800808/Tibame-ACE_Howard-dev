# 生產環境診斷指南

## 🔍 問題現況
- ✅ **本地環境**：Webhook 端點工作正常，返回 200 OK
- ❌ **生產環境**：`https://ace.89.com.tw/api/linebot/webhook` 返回 404 Not Found

---

## 📋 診斷步驟

### 步驟 1：SSH 連接到生產環境伺服器

```bash
ssh user@ace.89.com.tw
# 或使用您的 SSH 連接方式
```

---

### 步驟 2：檢查 FastAPI/Uvicorn 進程是否在運行

```bash
# 檢查 Python/Uvicorn 進程
ps aux | grep uvicorn
ps aux | grep python | grep -v grep

# 檢查是否監聽在 Port 8000（或其他端口）
netstat -tulpn | grep :8000
# 或使用 ss
ss -tulpn | grep :8000
```

**預期結果**：
- 應該看到 `uvicorn run:app` 或類似的進程
- 應該看到進程監聽在某個端口（例如 8000）

**如果沒有看到進程** → 需要啟動伺服器（見步驟 4）

---

### 步驟 3：檢查 Nginx 配置

```bash
# 查看 Nginx 配置檔案
ls -la /etc/nginx/sites-available/
ls -la /etc/nginx/sites-enabled/
ls -la /etc/nginx/conf.d/

# 檢查 ace.89.com.tw 的配置
cat /etc/nginx/sites-available/ace.89.com.tw
# 或
cat /etc/nginx/conf.d/ace.89.com.tw.conf

# 檢查 Nginx 是否有語法錯誤
sudo nginx -t

# 查看 Nginx 狀態
sudo systemctl status nginx
```

**預期配置應包含**：

```nginx
server {
    listen 80;
    server_name ace.89.com.tw;

    # 如果有 SSL
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # FastAPI 應用程式的反向代理
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 重要：保留 LINE 的簽名標頭
        proxy_pass_request_headers on;
    }
}
```

---

### 步驟 4：檢查伺服器日誌

```bash
# 查看 Nginx 訪問日誌
sudo tail -f /var/log/nginx/access.log

# 查看 Nginx 錯誤日誌
sudo tail -f /var/log/nginx/error.log

# 如果有 FastAPI 應用程式日誌（取決於您的部署方式）
tail -f /path/to/your/app.log

# 如果使用 systemd 管理服務
sudo journalctl -u your-app-service -f
```

**手動測試 Nginx 反向代理**：

```bash
# 在生產環境伺服器上測試 localhost:8000
curl -X POST http://localhost:8000/api/linebot/webhook \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: test" \
  -d '{"events":[]}'

# 測試 Nginx 反向代理
curl -X POST http://localhost/api/linebot/webhook \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: test" \
  -d '{"events":[]}'
```

---

### 步驟 5：如果伺服器未運行，啟動它

#### 方法 A：使用 systemd（推薦）

```bash
# 檢查服務狀態
sudo systemctl status your-app-name

# 啟動服務
sudo systemctl start your-app-name

# 設定開機自動啟動
sudo systemctl enable your-app-name

# 重新啟動服務
sudo systemctl restart your-app-name
```

#### 方法 B：使用 screen 或 tmux

```bash
# 使用 screen
screen -S ace-fastapi
cd /path/to/Tibame-ACE
source .venv/bin/activate
python run.py
# 按 Ctrl+A 然後 D 離開 screen

# 使用 tmux
tmux new -s ace-fastapi
cd /path/to/Tibame-ACE
source .venv/bin/activate
python run.py
# 按 Ctrl+B 然後 D 離開 tmux
```

#### 方法 C：使用 Gunicorn（生產環境推薦）

```bash
cd /path/to/Tibame-ACE
source .venv/bin/activate

# 安裝 Gunicorn（如果還沒安裝）
pip install gunicorn

# 啟動 Gunicorn
gunicorn run:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --daemon \
  --access-logfile /var/log/ace-fastapi/access.log \
  --error-logfile /var/log/ace-fastapi/error.log
```

---

### 步驟 6：重新測試生產環境 Webhook

在**本地電腦**執行：

```powershell
# 測試生產環境 Webhook
try {
  $response = Invoke-WebRequest -Uri "https://ace.89.com.tw/api/linebot/webhook" `
    -Method POST `
    -ContentType "application/json" `
    -Headers @{"X-Line-Signature" = "test"} `
    -Body '{"events":[]}' `
    -UseBasicParsing `
    -TimeoutSec 10
  
  Write-Host "✅ 成功！狀態碼: $($response.StatusCode)" -ForegroundColor Green
  Write-Host "回應: $($response.Content)"
} catch {
  Write-Host "❌ 失敗: $($_.Exception.Message)" -ForegroundColor Red
  if ($_.Exception.Response) {
    Write-Host "HTTP 狀態: $($_.Exception.Response.StatusCode.value__)"
  }
}
```

---

## 🎯 常見問題和解決方案

### ❌ 問題 A：502 Bad Gateway

**原因**：Nginx 配置正確，但 FastAPI 伺服器未運行

**解決方案**：
1. 啟動 FastAPI 伺服器（見步驟 5）
2. 確認伺服器監聽在正確的端口
3. 檢查防火牆規則

---

### ❌ 問題 B：404 Not Found

**原因**：Nginx 沒有正確的反向代理配置

**解決方案**：
1. 檢查 Nginx 配置中的 `location /api/` 區塊
2. 確認 `proxy_pass` 指向正確的端口
3. 重新載入 Nginx：`sudo nginx -s reload`

---

### ❌ 問題 C：連接超時

**原因**：防火牆阻擋或伺服器未監聽公開 IP

**解決方案**：
```bash
# 檢查防火牆規則
sudo ufw status
sudo iptables -L

# 開放必要的端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

## 📊 成功指標

✅ **生產環境配置正確**時應該：
1. FastAPI 伺服器進程正在運行
2. `ps aux | grep uvicorn` 顯示進程
3. `netstat -tulpn | grep :8000` 顯示監聽端口
4. Nginx 配置包含正確的反向代理設定
5. `curl http://localhost:8000/api/linebot/webhook` 返回 200
6. `https://ace.89.com.tw/api/linebot/webhook` 返回 200
7. LINE Developers Webhook 驗證通過 ✅

---

## 🔐 systemd 服務範例（推薦）

創建 `/etc/systemd/system/ace-fastapi.service`：

```ini
[Unit]
Description=ACE FastAPI Application
After=network.target mongodb.service

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/Tibame-ACE
Environment="PATH=/path/to/Tibame-ACE/.venv/bin"
ExecStart=/path/to/Tibame-ACE/.venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

然後：

```bash
# 重新載入 systemd
sudo systemctl daemon-reload

# 啟動服務
sudo systemctl start ace-fastapi

# 設定開機自動啟動
sudo systemctl enable ace-fastapi

# 檢查狀態
sudo systemctl status ace-fastapi
```

---

## 📞 下一步

執行診斷命令後，請告訴我：
1. FastAPI 伺服器是否在運行？
2. Nginx 配置是什麼樣子？
3. 遇到了哪些錯誤訊息？

我會根據您的情況提供具體的解決方案！
