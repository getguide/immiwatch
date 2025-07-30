#!/usr/bin/env python3
"""
Test script to verify Slack webhook is working
"""

import os
import requests
import json

def test_slack_webhook():
    """Test if Slack webhook is accessible"""
    
    # This would normally be in GitHub Secrets
    # For testing, we'll use a placeholder
    webhook_url = "YOUR_NEW_WEBHOOK_URL_HERE"
    
    if webhook_url == "YOUR_NEW_WEBHOOK_URL_HERE":
        print("❌ Please replace 'YOUR_NEW_WEBHOOK_URL_HERE' with your actual webhook URL")
        print("🔗 Get it from: https://immigratic.slack.com/services/B08TSSNCJTH")
        return False
    
    test_message = {
        "text": "🧪 *Slack Webhook Test*\n\n✅ **Status:** Webhook is working correctly!\n\n📊 **Test Details:**\n• **Test Type:** Manual verification\n• **System:** ImmiWatch Automation\n• **Time:** Test completed\n\n🔗 **GitHub:** https://github.com/getguide/immiwatch\n\n✅ **Result:** Webhook configured and ready for Express Entry draws!"
    }
    
    try:
        response = requests.post(webhook_url, json=test_message, timeout=10)
        
        if response.status_code == 200:
            print("✅ Slack webhook test successful!")
            print(f"📊 Response: {response.status_code}")
            return True
        else:
            print(f"❌ Slack webhook test failed!")
            print(f"📊 Status Code: {response.status_code}")
            print(f"📊 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Slack webhook: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Slack Webhook Configuration...")
    print("=" * 50)
    
    success = test_slack_webhook()
    
    print("=" * 50)
    if success:
        print("🎉 All tests passed! Your Slack webhook is ready.")
    else:
        print("⚠️ Please check your webhook URL and try again.") 