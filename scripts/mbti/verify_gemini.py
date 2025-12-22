import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.core.config import settings
from app.services.mbti_service import MBTIService

def verify_gemini_setup():
    print(f"Checking Gemini Configuration...")
    print(f"API Key present: {'Yes' if settings.GEMINI_API_KEY else 'No'}")
    print(f"Model Name: {settings.GEMINI_MODEL}")
    
    service = MBTIService()
    if service.model:
        print("✅ MBTIService initialized with model successfully.")
        return True
    else:
        print("❌ MBTIService model is None.")
        return False

if __name__ == "__main__":
    verify_gemini_setup()
