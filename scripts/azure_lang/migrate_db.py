#!/usr/bin/env python3
"""資料庫遷移腳本 - 新增 speaker_segments 和 speaker_count 列"""

import sqlite3
import os

db_path = "admin.db"

if not os.path.exists(db_path):
    print(f"❌ 資料庫不存在: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 檢查 video_analysis 表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='video_analysis'")
    if cursor.fetchone():
        # 獲取所有列信息
        cursor.execute("PRAGMA table_info(video_analysis)")
        columns = {row[1] for row in cursor.fetchall()}
        
        print("現有列:", columns)
        
        # 新增缺失的列
        if 'speaker_segments' not in columns:
            print("✓ 新增 speaker_segments 列...")
            cursor.execute("ALTER TABLE video_analysis ADD COLUMN speaker_segments TEXT")
            
        if 'speaker_count' not in columns:
            print("✓ 新增 speaker_count 列...")
            cursor.execute("ALTER TABLE video_analysis ADD COLUMN speaker_count INTEGER DEFAULT 0")
        
        conn.commit()
        print("✅ 資料庫更新成功")
    else:
        print("⚠️ video_analysis 表不存在")

except sqlite3.OperationalError as e:
    print(f"❌ 資料庫錯誤: {e}")
    conn.rollback()
except Exception as e:
    print(f"❌ 錯誤: {e}")
    conn.rollback()
finally:
    conn.close()
