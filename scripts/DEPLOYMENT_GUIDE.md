# 🚀 Deployment Guide

## Quick Setup for Airtable Webhook

### **Step 1: Deploy Webhook Handler**

#### **Option A: Local Development**
```bash
# Install Flask
pip install flask

# Run the webhook handler
python scripts/webhook_handler.py
```

#### **Option B: Deploy to Server**
1. Upload `webhook_handler.py` to your server
2. Install Flask: `pip install flask`
3. Run: `python webhook_handler.py`
4. Your webhook URL will be: `https://your-server.com/webhook/news`

### **Step 2: Update Airtable Script**

In `airtable_webhook_script.js`, update these values:

```javascript
const CONFIG = {
    // UPDATE THIS to your actual webhook URL
    AUTOMATION_WEBHOOK_URL: 'https://your-server.com/webhook/news',
    
    // UPDATE THIS to a secure random string (generate one)
    WEBHOOK_SECRET: 'your-secure-secret-key-here',
    
    // Optional: Your Slack webhook
    SLACK_WEBHOOK_URL: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
};
```

### **Step 3: Generate Secure Secret**

Generate a secure secret key:
```bash
# Option 1: Use openssl
openssl rand -base64 32

# Option 2: Use node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### **Step 4: Test the System**

```bash
# Test the webhook handler
curl -X POST http://localhost:5000/webhook/news \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: your-secret-key" \
  -d @scripts/test_article.json
```

### **Step 5: Set Up Airtable Automation**

1. Go to your Airtable base
2. Create automation: "When record is created"
3. Add action: "Run a script"
4. Copy the `airtable_webhook_script.js` content
5. Update the CONFIG section with your URLs and secret

## 🔐 Security Notes

- **Never commit secrets to Git**
- **Use environment variables for production**
- **Generate a unique secret for each deployment**
- **Use HTTPS in production**

## 📞 Support

If you need help:
1. Check the logs in the webhook handler
2. Verify your URLs and secrets
3. Test with the provided test scripts 