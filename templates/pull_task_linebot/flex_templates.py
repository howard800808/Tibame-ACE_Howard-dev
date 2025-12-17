# -*- coding: utf-8 -*-
"""
Project: Hotel Task Management System
Module: Flex Message Templates
Description: 通用派工卡片生成模組 (Universal Task Card Template)
Author: Gemini (Assisted)
"""

def create_universal_task_card(dept, priority, room, guest, title, content, time, remark, status="PENDING", task_id=None):
    """
    生成五星級飯店通用派工卡片 (萬用模板)
    
    :param dept: 部門名稱 (如 "HK 房務部", "F&B 餐飲")
    :param priority: 優先級代碼 ("P", "E", "F") - 自動對應顏色
    :param room: 地點或房號
    :param guest: 客人稱謂
    :param title: 任務標題
    :param content: 任務內容
    :param time: 預定時間
    :param remark: 備註事項
    :param status: 目前狀態 ("PENDING", "PROGRESS", "DONE")
    :param task_id: 任務 ID (用於 Postback)
    :return: dict (符合 Line Flex Message 規範的 JSON 物件)
    """

    # ==========================================
    # 1. 設定檔 (Configuration) - 集中管理顏色與樣式
    # ==========================================
    
    # 優先級色碼表 (P=紅, E=黃, F=綠)
    PRIORITY_MAP = {
        "P": {"color": "#D93025"},  # Red
        "E": {"color": "#F59E0B"},  # Amber Yellow
        "F": {"color": "#188038"}   # Green
    }

    # 狀態與按鈕邏輯表
    STATUS_MAP = {
        "PENDING": {
            "label": "● 任務未執行",
            "color": "#D93025",       # 紅色文字
            "btn_text": "接受任務 (Accept)",
            "btn_color": "#1A3B5D",   # 藍色按鈕
            "op": "accept"
        },
        "PROGRESS": {
            "label": "▶ 任務執行中",
            "color": "#188038",       # 綠色文字
            "btn_text": "任務完成回報 (Report)",
            "btn_color": "#188038",   # 綠色按鈕
            "op": "complete"
        },
        "DONE": {
            "label": "✔ 已完成",
            "color": "#2C3E50",       # 灰色文字
            "btn_text": "查看歸檔 (Archived)",
            "btn_color": "#B4B4B4",   # 灰色按鈕
            "op": "archive"
        }
    }

    # ==========================================
    # 2. 邏輯處理 (Logic)
    # ==========================================
    
    # 防呆機制：若輸入未知的代碼，預設為 F (綠) 和 PENDING
    p_code = priority.upper()
    p_style = PRIORITY_MAP.get(p_code, PRIORITY_MAP["F"])
    
    s_code = status.upper()
    s_style = STATUS_MAP.get(s_code, STATUS_MAP["PENDING"])

    # ==========================================
    # 3. 視圖生成 (View) - Flex Message JSON 結構
    # ==========================================
    
    return {
      "type": "bubble",
      "size": "mega",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": dept,  # [變數] 部門
                "color": "#B4B4B4",
                "weight": "bold",
                "size": "xs",
                "gravity": "center",
                "flex": 1
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": p_code,  # [變數] 優先級單字 (P/E/F)
                    "color": "#FFFFFF",
                    "size": "xs",
                    "weight": "bold",
                    "align": "center"
                  }
                ],
                "backgroundColor": p_style["color"],  # [變數] Badge 背景色
                "cornerRadius": "10px",
                "width": "30px",
                "height": "20px",
                "justifyContent": "center"
              }
            ]
          },
          {
            "type": "text",
            "text": room,  # [變數] 房號/地點
            "weight": "bold",
            "size": "3xl",
            "color": "#FFFFFF",
            "margin": "md"
          },
          {
            "type": "text",
            "text": f"Guest: {guest}",  # [變數] 客人
            "color": "#C5A065",
            "size": "sm",
            "margin": "sm",
            "weight": "bold"
          }
        ],
        "backgroundColor": "#1A3B5D",  # 品牌深藍色
        "paddingAll": "20px"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": title,  # [變數] 標題
            "weight": "bold",
            "size": "xl",
            "color": "#1A3B5D"
          },
          {
            "type": "separator",
            "margin": "lg",
            "color": "#E5E5E5"
          },
          # --- 欄位 1: 狀態 ---
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box", "layout": "vertical",
                "contents": [{"type": "text", "text": "目前狀態", "size": "sm", "color": "#aaaaaa"}],
                "width": "85px", "flex": 0
              },
              {
                "type": "text",
                "text": s_style["label"],  # [變數] 狀態文字
                "size": "sm",
                "color": s_style["color"], # [變數] 狀態顏色
                "flex": 1, "weight": "bold", "wrap": True
              }
            ],
            "margin": "lg"
          },
          # --- 欄位 2: 時間 ---
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box", "layout": "vertical",
                "contents": [{"type": "text", "text": "預定時間", "size": "sm", "color": "#aaaaaa"}],
                "width": "85px", "flex": 0
              },
              {
                "type": "text",
                "text": time,  # [變數] 時間
                "size": "sm",
                "color": "#333333",
                "flex": 1, "wrap": True, "weight": "bold"
              }
            ],
            "margin": "md"
          },
          # --- 欄位 3: 內容 ---
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box", "layout": "vertical",
                "contents": [{"type": "text", "text": "任務內容", "size": "sm", "color": "#aaaaaa"}],
                "width": "85px", "flex": 0
              },
              {
                "type": "text",
                "text": content,  # [變數] 內容
                "size": "sm",
                "color": "#555555",
                "flex": 1, "wrap": True
              }
            ],
            "margin": "md"
          },
          # --- 欄位 4: 備註 ---
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box", "layout": "vertical",
                "contents": [{"type": "text", "text": "備註", "size": "sm", "color": "#aaaaaa"}],
                "width": "85px", "flex": 0
              },
              {
                "type": "text",
                "text": remark,  # [變數] 備註
                "size": "sm",
                "color": p_style["color"], # [變數] 備註顏色跟隨優先級
                "flex": 1, "wrap": True, "weight": "bold"
              }
            ],
            "margin": "md"
          }
        ],
        "paddingAll": "20px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": s_style["btn_text"],
              "data": f"action=task&op={s_style['op']}&id={task_id}&dept={dept.split(' ')[0]}" if task_id else "action=none"
            },
            "style": "primary",
            "color": s_style["btn_color"],  # [變數] 按鈕顏色
            "height": "sm"
          }
        ],
        "paddingAll": "20px"
      }
    }

# Alias for backward compatibility
create_hotel_task_card = create_universal_task_card