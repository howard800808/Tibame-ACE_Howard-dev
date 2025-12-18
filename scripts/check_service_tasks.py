import sys
import os

# Add the project root to the python path
sys.path.append(os.getcwd())

from app.services.linebot_service import linebot_service

def check_service_tasks():
    # We don't need to initialize the full bot for this, just the DB part which is handled inside the method
    # But get_tasks_for_department imports SessionLocal inside, so it should work.
    
    dept = "GS"
    print(f"Checking tasks for {dept}...")
    bubbles = linebot_service.get_tasks_for_department(dept)
    
    # The bubbles are Flex Message objects (dicts). We need to extract the task_id from the postback data.
    # Structure: bubble -> footer -> contents[0] (button) -> action -> data
    
    for i, bubble in enumerate(bubbles):
        try:
            # Navigate to the button action data
            # Based on flex_templates.py:
            # footer -> box (vertical) -> button (action)
            footer = bubble.get('footer', {})
            footer_contents = footer.get('contents', [])
            if footer_contents:
                button = footer_contents[0]
                action = button.get('action', {})
                data = action.get('data', '')
                label = action.get('label', '')
                print(f"Task {i+1}: Label='{label}', Data='{data}'")
        except Exception as e:
            print(f"Error parsing bubble {i+1}: {e}")

if __name__ == "__main__":
    check_service_tasks()
