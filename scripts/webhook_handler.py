#!/usr/bin/env python3
"""
ImmiWatch Webhook Handler
Simple Flask server to receive Airtable data and process it with our automation system
"""

from flask import Flask, request, jsonify
import json
import os
import sys
from pathlib import Path

# Add the scripts directory to the path so we can import our automation system
sys.path.append(str(Path(__file__).parent))

from news_automation import NewsAutomationSystem

app = Flask(__name__)

# Configuration - Update these with your actual values
CONFIG = {
    # Secret key for webhook authentication (generate a secure random key)
    'WEBHOOK_SECRET': os.getenv('WEBHOOK_SECRET', 'your-secret-key-here'),
    
    # Slack webhook URL (optional)
    'SLACK_WEBHOOK_URL': os.getenv('SLACK_WEBHOOK_URL'),
    
    # Logging configuration
    'LOG_LEVEL': 'INFO'
}

def validate_webhook_secret(request):
    """Validate the webhook secret for security"""
    # Check if secret is provided in headers or query params
    provided_secret = request.headers.get('X-Webhook-Secret') or request.args.get('secret')
    
    if not provided_secret:
        return False, "No webhook secret provided"
    
    if provided_secret != CONFIG['WEBHOOK_SECRET']:
        return False, "Invalid webhook secret"
    
    return True, "Secret validated"

@app.route('/webhook/news', methods=['POST'])
def handle_news_webhook():
    """Handle incoming news data from Airtable"""
    try:
        # Validate webhook secret
        is_valid, message = validate_webhook_secret(request)
        if not is_valid:
            return jsonify({'error': message}), 401
        
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        print(f"📥 Received webhook data: {json.dumps(data, indent=2)}")
        
        # Process the data with our automation system
        automation = NewsAutomationSystem()
        result = automation.publish_article(data)
        
        if result:
            # Generate article URL
            if 'category' in data and 'date_of_update' in data and 'slug' in data:
                article_url = f"https://immiwatch.ca/news/daily/{data['category']}/{data['date_of_update']}/{data['slug']}/"
            else:
                article_url = "N/A"
            
            response = {
                'success': True,
                'message': 'Article published successfully',
                'article_url': article_url,
                'processing_time': 'N/A'  # Could add timing if needed
            }
            
            print(f"✅ Article published: {article_url}")
            return jsonify(response), 200
        else:
            response = {
                'success': False,
                'message': 'Article publication failed',
                'error': 'Check logs for details'
            }
            
            print("❌ Article publication failed")
            return jsonify(response), 500
            
    except Exception as e:
        error_response = {
            'success': False,
            'message': f'Webhook processing error: {str(e)}',
            'error': str(e)
        }
        
        print(f"💥 Webhook error: {str(e)}")
        return jsonify(error_response), 500

@app.route('/webhook/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ImmiWatch News Webhook',
        'version': '1.0.0'
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with instructions"""
    return jsonify({
        'service': 'ImmiWatch News Webhook Handler',
        'endpoints': {
            '/webhook/news': 'POST - Receive news data from Airtable',
            '/webhook/health': 'GET - Health check',
            '/': 'GET - This information'
        },
        'usage': {
            'method': 'POST',
            'url': '/webhook/news',
            'headers': {
                'Content-Type': 'application/json',
                'X-Webhook-Secret': 'your-secret-key'
            },
            'body': 'JSON data from Airtable'
        }
    }), 200

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.getenv('PORT', 5000))
    
    print(f"🚀 Starting ImmiWatch Webhook Handler on port {port}")
    print(f"📡 Webhook URL: http://localhost:{port}/webhook/news")
    print(f"🔐 Secret Key: {CONFIG['WEBHOOK_SECRET']}")
    print(f"📊 Health Check: http://localhost:{port}/webhook/health")
    
    app.run(host='0.0.0.0', port=port, debug=True) 