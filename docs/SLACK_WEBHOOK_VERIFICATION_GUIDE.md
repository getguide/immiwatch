# 🧪 Slack Webhook Verification Guide

## ✅ **Setup Complete!**

You've successfully:
- ✅ Got the new webhook URL from Slack
- ✅ Added it as a GitHub Secret named `SLACK_WEBHOOK_URL`
- ✅ Updated workflows to use the secure secret

## 🔍 **How to Verify Everything is Working**

### **Method 1: Manual GitHub Actions Test**
1. Go to: https://github.com/getguide/immiwatch/actions
2. Click on **Monthly Report Scheduler** workflow
3. Click **Run workflow** → **Run workflow**
4. Check if you receive a Slack notification

### **Method 2: Test with Airtable**
1. Go to your Airtable automation
2. Trigger a test record
3. Check if you receive a Slack notification

### **Method 3: Local Test (Optional)**
1. Edit `test_slack_webhook.py`
2. Replace `YOUR_NEW_WEBHOOK_URL_HERE` with your actual webhook URL
3. Run: `python3 test_slack_webhook.py`

## 📊 **Expected Slack Notifications**

### **Success Notification:**
```
🎉 Express Entry Draw Processed Successfully!

📊 Draw Details:
• Program: EE-PNP
• ITAs: 277
• CRS Score: 726
• Draw Number: 348
• Date: 2025-08-05
• Category: General
• Region: All

📈 Updated Report: reports/express-entry/ee-july-2025/index.html
🔗 View Report: https://immiwatch.ca/reports/express-entry/ee-july-2025/

✅ Status: Report updated and committed to GitHub

📊 Summary: Added 277 ITAs to EE-PNP program

🔗 GitHub Commit: https://github.com/getguide/immiwatch/commit/abc123
```

### **Daily Check Notification:**
```
✅ Monthly Report Check Complete

📅 Current Month: 2025-07
📊 Status: No month transition needed

🔄 Next Check: Tomorrow at 2 AM UTC

📋 Summary: Daily check completed - current month report is active and ready for draws
```

## 🚨 **Troubleshooting**

### **If No Notifications:**
1. **Check GitHub Secret**: Verify `SLACK_WEBHOOK_URL` is set correctly
2. **Check Webhook URL**: Ensure it's the latest one from Slack
3. **Check GitHub Actions**: Look for workflow runs and logs
4. **Check Slack Channel**: Ensure notifications are going to the right channel

### **If Error Notifications:**
1. **Check GitHub Actions Logs**: Look for detailed error messages
2. **Verify Webhook URL**: Make sure it's valid and active
3. **Check Permissions**: Ensure the webhook has proper permissions

## 🔗 **Useful Links**

- **GitHub Actions**: https://github.com/getguide/immiwatch/actions
- **GitHub Secrets**: https://github.com/getguide/immiwatch/settings/secrets/actions
- **Slack Webhook**: https://immigratic.slack.com/services/B08TSSNCJTH
- **Repository**: https://github.com/getguide/immiwatch

## 🎯 **Next Steps**

1. **Test the system** with a manual workflow trigger
2. **Monitor Slack** for notifications
3. **Verify Airtable integration** works correctly
4. **Set up monitoring** for the automation pipeline

---

**Your Slack webhook is now secure and ready for production!** 🚀 