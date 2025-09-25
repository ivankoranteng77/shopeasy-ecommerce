#!/usr/bin/env python3
"""
Simple WhatsApp integration test - no user input required.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.whatsapp import send_whatsapp_message
from app.config import settings

def main():
    print("📱 Testing WhatsApp Integration...")
    print("=" * 50)
    
    # Show configuration status
    if settings.whatsapp_api_url and settings.whatsapp_access_token:
        if "YOUR_PHONE_NUMBER_ID" in settings.whatsapp_api_url:
            print("🔧 Status: Development Mode (placeholder credentials)")
        else:
            print("🔧 Status: Production Mode (real credentials configured)")
    else:
        print("🔧 Status: Development Mode (no credentials configured)")
    
    print(f"📞 Admin Number: {settings.whatsapp_admin_number}")
    print()
    
    # Test message
    test_message = """🎉 WhatsApp Integration Test

✅ Your e-commerce system is working!

When customers place orders, you'll receive notifications like this with:
• Order details
• Customer information  
• Items ordered
• Delivery address

This test confirms WhatsApp integration is ready! 🚀"""

    print("📤 Sending test notification...")
    print()
    
    # Send test message
    result = send_whatsapp_message(settings.whatsapp_admin_number, test_message)
    
    if result:
        print("✅ WhatsApp integration test successful!")
        
        if not settings.whatsapp_api_url or "YOUR_PHONE_NUMBER_ID" in str(settings.whatsapp_api_url):
            print()
            print("💡 Development Mode Active:")
            print("   - Messages are logged to console (see above)")
            print("   - No real WhatsApp messages sent")
            print("   - Perfect for testing your store")
            print()
            print("🚀 To enable real WhatsApp notifications:")
            print("   1. See WHATSAPP_SETUP.md for instructions")
            print("   2. Configure Facebook/Twilio/other WhatsApp API")
            print("   3. Update .env file with real credentials")
        else:
            print("📱 Check your WhatsApp for the test message!")
            
    else:
        print("❌ WhatsApp integration test failed")
        print("💡 Check your API configuration and try again")
    
    print()
    print("🛒 Your e-commerce system is ready!")
    print("   - Place test orders at: http://localhost:3000")
    print("   - Admin API docs at: http://127.0.0.1:8000/docs")
    
if __name__ == "__main__":
    main()