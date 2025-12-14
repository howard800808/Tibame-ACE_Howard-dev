def create_report_flow_card(step, dept, room, task_id):
    """
    生成任務回報流程卡片 (Step 1 ~ 5)
    
    :param step: 目前步驟 (1~5)
    :param dept: 部門名稱 (e.g., "HK 房務部")
    :param room: 房號 (e.g., "Room 1205")
    :param task_id: 任務ID (用於 Postback data 追蹤)
    :return: Flex Message JSON
    """
    
    # --- 1. 定義每個步驟的內容與按鈕設定 (Configuration) ---
    STEPS_CONFIG = {
        1: {
            "title": "任務回報 (1/5)",
            "question": "是否順利完成？",
            "desc": "請確認現場狀況是否符合驗收標準。",
            "buttons": [
                {"label": "是 (Yes)", "color": "#188038", "style": "primary", "data": f"action=report&step=2&id={task_id}&ans=yes"},
                {"label": "否 (No)",  "color": "#D93025", "style": "primary", "data": f"action=report&step=2&id={task_id}&ans=no"} # 異常流程
            ]
        },
        2: {
            "title": "任務回報 (2/5)",
            "question": "補充說明 / 微調查",
            "desc": "請簡述現場執行狀況或特殊備註。",
            "buttons": [ # 這裡使用 URI Action
                {"label": "🎤 語音輸入", "color": "#1A3B5D", "style": "primary", "type": "uri", "uri": "https://line.me/R/nv/audio/"},
                {"label": "⌨️ 文字輸入", "color": "#B4B4B4", "style": "secondary", "type": "uri", "uri": "https://line.me/R/nv/keyboard/"}
            ]
        },
        3: {
            "title": "任務回報 (3/5)",
            "question": "與顧客有互動嗎？",
            "desc": "若有遇見客人，後續請簡述互動內容。",
            "buttons": [
                {"label": "有 (Yes)", "color": "#1A3B5D", "style": "primary",   "data": f"action=report&step=4&id={task_id}&ans=yes"},
                {"label": "無 (No)",  "color": "#B4B4B4", "style": "secondary", "data": f"action=report&step=4&id={task_id}&ans=no"}
            ]
        },
        4: {
            "title": "任務回報 (4/5)",
            "question": "顧客情緒判斷",
            "desc": "請依照觀察，記錄客人當下的情緒反應。",
            "buttons": [
                {"label": "〇 正向", "color": "#188038", "style": "primary", "data": f"action=report&step=5&id={task_id}&ans=positive"},
                {"label": "〇 中性", "color": "#5A6A7B", "style": "primary", "data": f"action=report&step=5&id={task_id}&ans=neutral"},
                {"label": "〇 負向", "color": "#D93025", "style": "primary", "data": f"action=report&step=5&id={task_id}&ans=negative"}
            ]
        },
        5: {
            "title": "任務回報 (5/5)",
            "question": "備註事項",
            "desc": "請補充其他重要事項，若無可直接略過。",
            "buttons": [ # 這裡使用 URI Action
                {"label": "🎤 語音輸入", "color": "#1A3B5D", "style": "primary", "type": "uri", "uri": "https://line.me/R/nv/audio/"},
                {"label": "⌨️ 文字輸入", "color": "#B4B4B4", "style": "secondary", "type": "uri", "uri": "https://line.me/R/nv/keyboard/"}
            ]
        }
    }

    # 防呆：如果步驟超出範圍，預設回傳 Step 1
    current_config = STEPS_CONFIG.get(step, STEPS_CONFIG[1])

    # --- 2. 動態生成按鈕列 (Button Logic) ---
    footer_contents = []
    
    for idx, btn in enumerate(current_config["buttons"]):
        # 處理按鈕間距 (Separator)
        if idx > 0:
            footer_contents.append({"type": "separator", "margin": "md"})
            
        # 建立按鈕物件
        button_obj = {
            "type": "button",
            "style": btn["style"],
            "color": btn["color"],
            "height": "sm",
            "flex": 1 # 確保按鈕均分寬度
        }
        
        # 判斷是 Postback 還是 URI
        if btn.get("type") == "uri":
            button_obj["action"] = {"type": "uri", "label": btn["label"], "uri": btn["uri"]}
        else:
            button_obj["action"] = {"type": "postback", "label": btn["label"], "data": btn.get("data", "no_data")}
            
        footer_contents.append(button_obj)


    # --- 3. 回傳完整 Flex Message JSON ---
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
                "type": "text", "text": dept, # [變數] 部門
                "color": "#B4B4B4", "weight": "bold", "size": "xs", "gravity": "center", "flex": 1
              },
              {
                "type": "text", "text": room, # [變數] 房號
                "weight": "bold", "size": "lg", "color": "#FFFFFF", "gravity": "center", "align": "end", "flex": 1
              }
            ]
          }
        ],
        "backgroundColor": "#1A3B5D", "paddingAll": "20px"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text", "text": current_config["title"], # [變數] 步驟標題 (1/5)
            "weight": "bold", "size": "xs", "color": "#C5A065"
          },
          {
            "type": "text", "text": current_config["question"], # [變數] 核心問題
            "weight": "bold", "size": "xl", "color": "#1A3B5D", "margin": "md"
          },
          {
            "type": "text", "text": current_config["desc"], # [變數] 描述說明
            "size": "sm", "color": "#aaaaaa", "margin": "sm", "wrap": True
          }
        ],
        "paddingAll": "20px"
      },
      "footer": {
        "type": "box",
        "layout": "horizontal", # 水平排列按鈕
        "contents": footer_contents, # [變數] 動態按鈕組
        "paddingAll": "20px"
      }
    }