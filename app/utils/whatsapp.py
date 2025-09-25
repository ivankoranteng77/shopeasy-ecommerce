import requests
import logging
from typing import Optional
from app.config import settings
from app.models.models import Order

logger = logging.getLogger(__name__)


def format_order_message(order: Order) -> str:
    """Format order details for WhatsApp message."""
    message = f"""🛒 *NEW ORDER RECEIVED*

📋 *Order Details:*
• Order Number: {order.order_number}
• Customer: {order.customer_name}
• Phone: {order.customer_phone}
• Total: ${order.total_amount:.2f}

📍 *Delivery Address:*
{order.customer_address}

🛍️ *Items Ordered:*
"""
    
    for item in order.order_items:
        message += f"• {item.product.name} x{item.quantity} - ${item.price:.2f}\n"
    
    if order.notes:
        message += f"\n📝 *Customer Notes:*\n{order.notes}"
    
    message += f"\n\n⏰ *Order Time:* {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    message += f"\n\n👆 *Please confirm this order and prepare for delivery!*"
    
    return message


def send_whatsapp_facebook_api(phone_number: str, message: str) -> bool:
    """Send via Facebook/Meta WhatsApp Business API."""
    try:
        url = settings.whatsapp_api_url
        headers = {
            "Authorization": f"Bearer {settings.whatsapp_access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number.replace("+", ""),
            "text": {"body": message}
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code in [200, 201]:
            logger.info(f"WhatsApp message sent successfully via Facebook API to {phone_number}")
            return True
        else:
            logger.error(f"Facebook API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending WhatsApp via Facebook API: {str(e)}")
        return False


def send_whatsapp_twilio(phone_number: str, message: str) -> bool:
    """Send via Twilio WhatsApp API."""
    try:
        import base64
        
        # Extract account SID and auth token from URL and settings
        account_sid = "YOUR_TWILIO_ACCOUNT_SID"  # You'll need to set this
        auth_token = settings.whatsapp_access_token
        
        auth_string = f"{account_sid}:{auth_token}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        payload = {
            "From": "whatsapp:+14155238886",  # Twilio WhatsApp number
            "To": f"whatsapp:{phone_number}",
            "Body": message
        }
        
        response = requests.post(settings.whatsapp_api_url, data=payload, headers=headers, timeout=10)
        
        if response.status_code in [200, 201]:
            logger.info(f"WhatsApp message sent successfully via Twilio to {phone_number}")
            return True
        else:
            logger.error(f"Twilio error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending WhatsApp via Twilio: {str(e)}")
        return False


def send_whatsapp_generic_api(phone_number: str, message: str) -> bool:
    """Send via generic WhatsApp API service."""
    try:
        payload = {
            "phone": phone_number,
            "message": message,
            "token": settings.whatsapp_access_token
        }
        
        response = requests.post(
            settings.whatsapp_api_url,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info(f"WhatsApp message sent successfully via generic API to {phone_number}")
            return True
        else:
            logger.error(f"Generic API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending WhatsApp via generic API: {str(e)}")
        return False


def send_whatsapp_message(phone_number: str, message: str) -> bool:
    """
    Send WhatsApp message using configured service.
    Automatically detects the service based on API URL.
    """
    try:
        # Check for development mode indicators
        is_dev_mode = (
            not settings.whatsapp_api_url or 
            not settings.whatsapp_access_token or
            "YOUR_PHONE_NUMBER_ID" in str(settings.whatsapp_api_url) or
            "your-whatsapp-access-token" in str(settings.whatsapp_access_token) or
            "your-whatsapp-business-api-token" in str(settings.whatsapp_access_token)
        )
        
        if is_dev_mode:
            # Development mode - just log the message
            logger.info("="*50)
            logger.info("📱 WHATSAPP MESSAGE (DEVELOPMENT MODE)")
            logger.info(f"📞 To: {phone_number}")
            logger.info("📝 Message:")
            logger.info(message)
            logger.info("="*50)
            print(f"\n📱 WhatsApp notification would be sent to: {phone_number}")
            print("💡 Configure WhatsApp API credentials to enable real messaging")
            print(f"📝 Message preview:\n{'-'*30}")
            print(message)
            print(f"{'-'*30}\n")
            return True
        
        # Production mode - detect service type based on URL
        api_url = settings.whatsapp_api_url.lower()
        
        if "graph.facebook.com" in api_url:
            return send_whatsapp_facebook_api(phone_number, message)
        elif "twilio.com" in api_url:
            return send_whatsapp_twilio(phone_number, message)
        else:
            return send_whatsapp_generic_api(phone_number, message)
            
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {str(e)}")
        return False


def send_order_notification(order: Order) -> bool:
    """Send order notification to admin via WhatsApp."""
    message = format_order_message(order)
    return send_whatsapp_message(settings.admin_whatsapp_number, message)


def send_order_status_update(order: Order, new_status: str) -> bool:
    """Send order status update to customer via WhatsApp."""
    status_messages = {
        "confirmed": "✅ Your order has been confirmed and is being prepared!",
        "preparing": "👨‍🍳 Your order is being prepared with care!",
        "ready": "🎉 Your order is ready for pickup/delivery!",
        "delivered": "📦 Your order has been delivered. Thank you for your order!",
        "cancelled": "❌ Your order has been cancelled. Please contact us if you have any questions."
    }
    
    message = f"""
📋 *Order Update*

Order Number: {order.order_number}
Status: {status_messages.get(new_status, new_status)}

Customer: {order.customer_name}
Total: ${order.total_amount:.2f}

Thank you for choosing us! 🙏
"""
    
    return send_whatsapp_message(order.customer_phone, message)