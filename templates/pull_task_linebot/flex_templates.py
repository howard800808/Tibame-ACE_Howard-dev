def create_hotel_task_card(dept, priority, room, guest, title, content, time, remark, status="PENDING", task_id=None):
    """
    五星級飯店派工萬用函式 (支援：待派工 / 執行中 / 已完成)
    
    :param status: 關鍵參數! 
           - "PENDING":  顯示紅色「未執行」，按鈕為藍色「接受派工」
           - "PROGRESS": 顯示綠色「執行中」，按鈕為綠色「已完成派工」
    """

    # --- 1. 優先級設定 (控制 Badge 與 備註顏色) ---
    PRIORITY_MAP = {
        "P": {"label": "P", "color": "#D93025"},  # 紅
        "E": {"label": "E", "color": "#F59E0B"},  # 黃
        "F": {"label": "F", "color": "#188038"}   # 綠
    }

    # --- 2. 狀態設定 (控制 狀態文字 與 按鈕行為) ---
    # 這裡就是整合的核心：定義不同狀態下的文字與按鈕樣式
    STATUS_MAP = {
        "PENDING": {
            "text_label": "● 未執行", 
            "text_color": "#D93025",       # 紅色文字
            "btn_label": "接受任務 (Accept)", 
            "btn_color": "#1A3B5D",        # 藍色按鈕
            "btn_style": "primary"
        },
        "PROGRESS": {
            "text_label": "▶ 任務執行中", 
            "text_color": "#188038",       # 綠色文字
            "btn_label": "已完成任務 (Complete)", 
            "btn_color": "#188038",        # 綠色按鈕 (代表成功/完成)
            "btn_style": "primary"
        },
        # "DONE": {
        #     "text_label": "✔ 已完成", 
        #     "text_color": "#2C3E50",       # 灰色文字
        #     "btn_label": "查看歸檔 (Archive)", 
        #     "btn_color": "#B4B4B4",        # 灰色按鈕
        #     "btn_style": "secondary"
        # }
    }

    # --- 3. 邏輯處理 ---
    # 防呆機制：如果找不到代碼，預設回傳 F 或 PENDING
    p_conf = PRIORITY_MAP.get(priority.upper(), PRIORITY_MAP["F"])
    s_conf = STATUS_MAP.get(status.upper(), STATUS_MAP["PENDING"])

    # --- 4. 生成 Flex Message ---
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
                "type": "text", "text": dept,
                "color": "#B4B4B4", "weight": "bold", "size": "xs", "gravity": "center", "flex": 1
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text", "text": p_conf["label"], # [變數] 優先級 Badge
                    "color": "#FFFFFF", "size": "xxs", "weight": "bold", "align": "center"
                  }
                ],
                "backgroundColor": p_conf["color"], # [變數] 優先級顏色
                "cornerRadius": "10px", "width": "60px", "height": "18px", "justifyContent": "center"
              }
            ]
          },
          {
            "type": "text", "text": room, "weight": "bold", "size": "3xl", "color": "#FFFFFF", "margin": "md"
          },
          {
            "type": "text", "text": f"Guest: {guest}", "color": "#C5A065", "size": "sm", "margin": "sm", "weight": "bold"
          }
        ],
        "backgroundColor": "#1A3B5D", "paddingAll": "20px"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text", "text": title, "weight": "bold", "size": "xl", "color": "#1A3B5D"
          },
          {
            "type": "separator", "margin": "lg", "color": "#E5E5E5"
          },
          # 狀態欄位 (動態變化)
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
                "text": s_conf["text_label"],  # [變數] 狀態文字 (未執行/執行中)
                "size": "sm", 
                "color": s_conf["text_color"], # [變數] 狀態顏色 (紅/綠)
                "flex": 1, "weight": "bold", "wrap": True
              }
            ],
            "margin": "lg"
          },
          # 時間欄位
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
                "type": "text", "text": time, "size": "sm", "color": "#333333", "flex": 1, "wrap": True, "weight": "bold"
              }
            ],
            "margin": "md"
          },
          # 內容欄位
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
                "type": "text", "text": content, "size": "sm", "color": "#555555", "flex": 1, "wrap": True
              }
            ],
            "margin": "md"
          },
          # 備註欄位
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
                "type": "text", "text": remark, "size": "sm", 
                "color": p_conf["color"], # 備註顏色跟隨優先級
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
          # 按鈕 1 (主按鈕：動態變化)
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": s_conf["btn_label"],
              "data": f"action=task&op={'accept' if status.upper()=='PENDING' else 'complete'}&dept={dept}&room={room}&id={task_id or ''}"
            },
            "style": s_conf["btn_style"],
            "color": s_conf["btn_color"],   # [變數] 按鈕顏色 (藍/綠)
            "height": "sm"
          },
          # 按鈕 2 (固定為問題彙報)
          # {
          #   "type": "button",
          #   "action": {
          #     "type": "uri", "label": "問題彙報 (Report)", "uri": "https://line.me"
          #   },
          #   "style": "secondary",
          #   "margin": "md",
          #   "height": "sm",
          #   "color": "#B4B4B4"
          # }
        ],
        "paddingAll": "20px"
      }
    }