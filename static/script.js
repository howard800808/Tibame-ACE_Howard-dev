/**
 * ACE服務管理後台 - 共用腳本
 * 包含登出、Token 刷新與權限驗證邏輯
 */

// 登出功能
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
    alert('已成功登出!');
    window.location.href = '/login';
}

// 刷新 Token (目前實作為重新登入)
function refreshToken() {
    alert('請重新登入以獲取新的 Token');
    window.location.href = '/login';
}

/**
 * 驗證使用者權限
 * @param {Function} onSuccess - 驗證成功後的回調函數，接收 (userData, token)
 */
async function checkAuth(onSuccess) {
    const token = localStorage.getItem('access_token');
    
    // Token 檢查
    if (!token) {
        alert('未偵測到登入憑證，請先登入');
        window.location.href = '/login';
        return;
    }

    try {
        // 驗證 Token 有效性
        const response = await fetch('/api/users/me', {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            if (response.status === 401) {
                throw new Error('登入憑證已過期，請重新登入');
            } else {
                throw new Error(errorData.detail || `伺服器錯誤 (${response.status})`);
            }
        }

        const userData = await response.json();
        console.log('使用者驗證成功:', userData);
        
        // 儲存使用者資訊
        localStorage.setItem('user_info', JSON.stringify(userData));
        
        // 更新頂部 Header 使用者資訊
        updateHeaderInfo(userData);

        // 初始化側邊欄 (如果存在)
        if (typeof initSidebar === 'function') {
            initSidebar(userData);
        }

        // 執行頁面特定的回調函數
        if (onSuccess && typeof onSuccess === 'function') {
            onSuccess(userData, token);
        }

    } catch (error) {
        console.error('驗證失敗:', error);
        alert(error.message);
        if (error.message.includes('登入憑證已過期')) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user_info');
            window.location.href = '/login';
        }
    }
}

// 自動執行驗證 (排除登入頁面)
if (window.location.pathname !== '/login') {
    window.addEventListener('DOMContentLoaded', function() {
        checkAuth(function(userData, token) {
            if (typeof window.onAuthSuccess === 'function') {
                window.onAuthSuccess(userData, token);
            }
        });
    });
}

// 更新 Header 使用者資訊 UI
function updateHeaderInfo(userData) {
    if (!userData) return;

    const userNameEl = document.getElementById('userName');
    const userEmailEl = document.getElementById('userEmail');
    const userAvatarEl = document.getElementById('userAvatar');
    const userLastLoginEl = document.getElementById('userLastLogin');

    if (userNameEl) userNameEl.textContent = userData.full_name || userData.username;
    if (userEmailEl) userEmailEl.textContent = userData.email;
    
    if (userAvatarEl) {
        const name = userData.full_name || userData.username || '?';
        userAvatarEl.textContent = name.charAt(0).toUpperCase();
        // 根據角色設定不同背景色
        if (userData.role === 'admin') {
            userAvatarEl.style.backgroundColor = '#dc3545'; // 紅色
        } else if (userData.role === 'manager') {
            userAvatarEl.style.backgroundColor = '#ffc107'; // 黃色
            userAvatarEl.style.color = '#000';
        } else {
            userAvatarEl.style.backgroundColor = '#007bff'; // 藍色
        }
    }

    if (userLastLoginEl) {
        const lastLogin = userData.last_login ? new Date(userData.last_login).toLocaleString() : '首次登入';
        userLastLoginEl.textContent = '最後登入: ' + lastLogin;
    }
}
