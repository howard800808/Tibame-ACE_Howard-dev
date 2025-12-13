"""
Broadcast a test message to all 12 department LINE Bots using the access tokens
from .env (loaded via app.core.config.Settings).

Usage:
    python test_linebot_broadcast.py "測試訊息"
If no argument is provided, a default test message with timestamp is sent.

This sends a LINE broadcast to each channel's followers. Ensure tokens are set.
"""
from datetime import datetime
import sys
from linebot import LineBotApi
from linebot.models import TextSendMessage
from app.core.config import settings

DEPARTMENTS = [
    ("GS", "客務部", settings.GS_ACCESS_TOKEN),
    ("HK", "房務部", settings.HK_ACCESS_TOKEN),
    ("CON", "門房諮詢", settings.CON_ACCESS_TOKEN),
    ("BP", "烘焙點心房", settings.BP_ACCESS_TOKEN),
    ("FB", "餐飲", settings.FB_ACCESS_TOKEN),
    ("CBS", "會議宴會", settings.CBS_ACCESS_TOKEN),
    ("FS", "花房", settings.FS_ACCESS_TOKEN),
    ("LUR", "洗衣房與制服室", settings.LUR_ACCESS_TOKEN),
    ("GAE", "總務工程", settings.GAE_ACCESS_TOKEN),
    ("BB", "飲料酒吧", settings.BB_ACCESS_TOKEN),
    ("AD", "美術設計", settings.AD_ACCESS_TOKEN),
    ("LA", "休閒活動部", settings.LA_ACCESS_TOKEN),
]


def main():
    user_msg = " ".join(sys.argv[1:]).strip()
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    message_text = user_msg or f"[整合測試] 12 部門 LINE Bot 廣播\n時間: {ts}"

    print("開始廣播測試訊息到 12 部門…\n")
    for code, name, token in DEPARTMENTS:
        if not token:
            print(f"⚠️  {code} {name}: 未設定 ACCESS_TOKEN，跳過")
            continue
        try:
            api = LineBotApi(token)
            api.broadcast(TextSendMessage(text=f"[{code}] {name}\n{message_text}"))
            print(f"✓ {code} {name}: 已送出廣播")
        except Exception as exc:  # noqa: BLE001
            print(f"✗ {code} {name}: 發送失敗 - {exc}")

    print("\n測試完成。請在對應 LINE 官方帳號中確認是否收到訊息。")


if __name__ == "__main__":
    main()
