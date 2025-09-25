#!/usr/bin/env python3
"""
Test script for WhatsApp integration.
This script helps you test your WhatsApp configuration.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.whatsapp import send_whatsapp_message
from app.config import settings

def test_whatsapp_integration():
    """Test WhatsApp integration with a simple message."""
    print("📱 WhatsApp Integration Test")
    print("=" * 40)
    
    # Show current configuration
    print(f"🔧 Configuration:")
    print(f"   API URL: {settings.whatsapp_api_url or 'Not configured (Development mode)'}")
    print(f"   Token: {'✅ Set' if settings.whatsapp_access_token else '❌ Not set'}")
    print(f"   Admin Number: {settings.whatsapp_admin_number}")
    print()
    
    # Get phone number for testing
    phone_number = input(f"📞 Enter phone number to test (or press Enter for {settings.whatsapp_admin_number}): ").strip()
    if not phone_number:
        phone_number = settings.whatsapp_admin_number
    
    # Create test message
    test_message = """🎉 *WhatsApp Integration Test*

This is a test message from your e-commerce system!

✅ If you received this message, WhatsApp integration is working correctly.

🛒 Your customers will receive order notifications like this when they place orders.

Thank you for setting up WhatsApp notifications! 🙏"""

    print(f"\n📤 Sending test message to: {phone_number}")
    print("📝 Message content:")
    print("-" * 30)
    print(test_message)
    print("-" * 30)
    
    # Send the message
    try:
        result = send_whatsapp_message(phone_number, test_message)
        
        if result:
            print("✅ Test message sent successfully!")
            if not settings.whatsapp_api_url or not settings.whatsapp_access_token:
                print("💡 You're in development mode - check your terminal logs above for the message content.")
            else:
                print("📱 Check your WhatsApp for the test message.")
        else:
            print("❌ Failed to send test message.")
            print("💡 Check your WhatsApp API configuration and try again.")
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        return False
    
    return result

def show_setup_help():
    """Show setup help information."""
    print("\n🔧 WhatsApp Setup Help")
    print("=" * 30)
    print("1. For development: No setup needed - messages show in logs")
    print("2. For production: Configure one of these options:")
    print("   • Facebook/Meta WhatsApp Business API (recommended)")
    print("   • Twilio WhatsApp API (easy setup)")
    print("   • Alternative WhatsApp API provider")
    print()
    print("📖 See WHATSAPP_SETUP.md for detailed setup instructions")
    print()

if __name__ == "__main__":
    try:
        show_setup_help()
        
        # Ask if user wants to test
        response = input("🧪 Do you want to run a WhatsApp test? (y/n): ").strip().lower()
        
        if response == 'y':
            success = test_whatsapp_integration()
            if success:
                print("\n🎉 WhatsApp integration test completed successfully!")
                print("💡 Your e-commerce system is ready to send order notifications.")
            else:
                print("\n❌ WhatsApp integration test failed.")
                print("💡 Check your configuration and try again.")
        else:
            print("\n👋 Test skipped. Run this script again when you're ready to test.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Test cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)