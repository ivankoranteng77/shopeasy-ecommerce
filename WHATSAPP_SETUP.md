# WhatsApp Integration Setup Guide

This guide helps you configure WhatsApp notifications for your e-commerce system. When customers place orders, you'll automatically receive notifications on WhatsApp.

## 🚀 Quick Start (Development Mode)

Your system already works in **Development Mode**! When orders are placed:

- Messages are logged to console/terminal
- You'll see what would be sent to WhatsApp
- No actual WhatsApp messages are sent (perfect for testing)

**To see this in action:**

1. Place a test order through your frontend (http://localhost:3000)
2. Check your backend terminal for the WhatsApp message preview

## 📱 WhatsApp Integration Options

### Option 1: Facebook/Meta WhatsApp Business API (Recommended)

**Pros:** Official API, reliable, feature-rich
**Cons:** Requires business verification

**Setup Steps:**

1. **Create Facebook Business Account**

   - Go to https://business.facebook.com/
   - Create or use existing business account

2. **Set up WhatsApp Business API**

   - Visit https://developers.facebook.com/
   - Create a new App → Business → WhatsApp
   - Add WhatsApp product to your app

3. **Get Phone Number ID**

   - In WhatsApp dashboard, note your Phone Number ID
   - This replaces `YOUR_PHONE_NUMBER_ID` in the API URL

4. **Generate Access Token**

   - In App Dashboard → WhatsApp → API Setup
   - Generate a permanent access token
   - Copy this token

5. **Update .env file:**
   ```env
   whatsapp_api_url=https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages
   whatsapp_access_token=your_permanent_access_token_here
   whatsapp_admin_number=+1234567890
   ```

**Testing:**

```bash
curl -X POST "https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "messaging_product": "whatsapp",
       "to": "1234567890",
       "text": {"body": "Test message from your e-commerce store!"}
     }'
```

### Option 2: Twilio WhatsApp API (Easy Setup)

**Pros:** Quick setup, good documentation, trial credits
**Cons:** Costs money, requires Twilio account

**Setup Steps:**

1. **Create Twilio Account**

   - Go to https://www.twilio.com/
   - Sign up and verify your account
   - Get $15 trial credit

2. **Enable WhatsApp**

   - In Twilio Console → Messaging → Try WhatsApp
   - Follow the sandbox setup
   - Note your WhatsApp number (usually +1 415 523 8886)

3. **Get Credentials**

   - Account SID (found in dashboard)
   - Auth Token (found in dashboard)

4. **Update .env file:**

   ```env
   whatsapp_api_url=https://api.twilio.com/2010-04-01/Accounts/YOUR_ACCOUNT_SID/Messages.json
   whatsapp_access_token=your_twilio_auth_token
   whatsapp_admin_number=+1234567890
   ```

5. **Update Twilio function** in `whatsapp.py`:
   - Replace `YOUR_TWILIO_ACCOUNT_SID` with your actual Account SID

**Testing:**

```bash
curl -X POST "https://api.twilio.com/2010-04-01/Accounts/YOUR_ACCOUNT_SID/Messages.json" \
     -u "YOUR_ACCOUNT_SID:YOUR_AUTH_TOKEN" \
     -d "From=whatsapp:+14155238886" \
     -d "To=whatsapp:+1234567890" \
     -d "Body=Test message from your store!"
```

### Option 3: Alternative Services

**Popular Services:**

- **WhatsApp Business API providers:** Vonage, MessageBird, 360Dialog
- **Multi-channel platforms:** SendGrid, Mailgun (some offer WhatsApp)
- **Local providers:** Many countries have WhatsApp API resellers

**Generic Setup:**

1. Sign up with your chosen provider
2. Get API endpoint and token
3. Update .env file with their specific format
4. Test their API documentation

## 🔧 Configuration

### Update Your Phone Number

Replace `+1234567890` with your actual WhatsApp number:

```env
whatsapp_admin_number=+1234567890  # Your actual number with country code
```

**Format Examples:**

- US: `+1234567890`
- UK: `+441234567890`
- India: `+911234567890`
- Ghana: `+233241234567`

### Test Configuration

Run this test script to verify your setup:

```python
# Create test_whatsapp.py
from app.utils.whatsapp import send_whatsapp_message

# Test message
result = send_whatsapp_message(
    phone_number="+1234567890",  # Your number
    message="🎉 WhatsApp integration test successful! Your e-commerce store is ready."
)

print(f"Message sent: {result}")
```

Run it:

```bash
venv\Scripts\python.exe test_whatsapp.py
```

## 📋 Message Templates

Your system sends these types of messages:

### New Order Notification (to Admin)

```
🛒 NEW ORDER RECEIVED

📋 Order Details:
• Order Number: ORD-001
• Customer: John Doe
• Phone: +1234567890
• Total: $99.99

📍 Delivery Address:
123 Main St, City, State 12345

🛍️ Items Ordered:
• iPhone 15 Pro x1 - $999.99
• Case x1 - $29.99

📝 Customer Notes:
Please call before delivery

⏰ Order Time: 2025-09-24 14:30:00

👆 Please confirm this order and prepare for delivery!
```

### Order Status Updates (to Customer)

```
📋 Order Update

Order Number: ORD-001
Status: ✅ Your order has been confirmed and is being prepared!

Customer: John Doe
Total: $99.99

Thank you for choosing us! 🙏
```

## 🛠️ Development & Testing

### Test Without Real WhatsApp

Your system works perfectly without WhatsApp API configured:

- Messages appear in terminal/logs
- All functionality works normally
- Perfect for development and testing

### Enable Debug Logging

Add to your code to see detailed logs:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Test Order Flow

1. **Place Test Order:** Use frontend to place order
2. **Check Backend Logs:** Look for WhatsApp message in terminal
3. **Verify Database:** Check if order was saved
4. **Test Status Updates:** Use admin API to update order status

## 🔒 Security & Best Practices

### Protect Your Credentials

- Never commit API tokens to git
- Use environment variables (`.env` file)
- Rotate tokens regularly
- Use least-privilege access

### Rate Limiting

- WhatsApp APIs have rate limits
- Implement retry logic for failed messages
- Don't spam customers with updates

### Message Content

- Keep messages concise and professional
- Include essential order information
- Provide clear next steps
- Add business branding

### Error Handling

Your system already handles:

- Network failures gracefully
- Invalid phone numbers
- API errors
- Service downtime

## 🚀 Going Live

### Before Production

- [ ] Test with real WhatsApp API
- [ ] Verify phone number format validation
- [ ] Test error scenarios
- [ ] Set up monitoring/alerts
- [ ] Configure proper logging
- [ ] Test with different order types

### Production Environment

1. **Use Production API Credentials**
2. **Set up Monitoring** - Track message delivery
3. **Configure Alerts** - Know when messages fail
4. **Backup Strategy** - Store message history
5. **Scale Considerations** - Handle high order volumes

## 🆘 Troubleshooting

### Common Issues

**"Phone number not found"**

- Verify phone number format (+countrycode)
- Ensure number is registered with WhatsApp
- Check for extra spaces or characters

**"API key invalid"**

- Regenerate access token
- Check token permissions
- Verify API URL is correct

**"Message not delivered"**

- Check recipient has WhatsApp
- Verify number is active
- Check API rate limits

**"Network timeout"**

- Increase timeout in code
- Check internet connection
- Try different API endpoint

### Debug Steps

1. Check .env file configuration
2. Verify API credentials are valid
3. Test with simple message first
4. Check server logs for errors
5. Test phone number format

### Get Help

- Check your WhatsApp API provider's documentation
- Look at their support/status pages
- Test with their official examples
- Contact their support team

## 💡 Tips for Success

1. **Start Simple:** Use development mode first
2. **Test Thoroughly:** Try different scenarios
3. **Monitor Performance:** Track message delivery rates
4. **User Experience:** Keep messages helpful and timely
5. **Backup Plan:** Have email notifications as fallback
6. **Compliance:** Follow WhatsApp's business policies

Your e-commerce system is ready for WhatsApp integration! 🎉
