"""
IRCC Express Entry Draw Monitor
===============================

AWS Lambda function that monitors the IRCC website for new Express Entry draws
and sends webhooks to GitHub when new draws are detected.

This function should be triggered every hour via CloudWatch Events.
"""

import json
import requests
import boto3
import re
from datetime import datetime, timezone
import os
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# GitHub webhook configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'getguide/immiwatch')
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/dispatches"

# IRCC URLs to monitor
IRCC_URLS = [
    "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/submit-profile/rounds-invitations.html",
    "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/submit-profile/rounds-invitations.html"
]

# S3 bucket for storing last known draw data
S3_BUCKET = os.environ.get('S3_BUCKET', 'immiwatch-draw-data')
S3_KEY = 'last_known_draw.json'

def get_last_known_draw():
    """Get the last known draw from S3"""
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
        return json.loads(response['Body'].read().decode('utf-8'))
    except Exception as e:
        logger.warning(f"Could not retrieve last known draw: {e}")
        return None

def save_last_known_draw(draw_data):
    """Save the last known draw to S3"""
    try:
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=S3_KEY,
            Body=json.dumps(draw_data, indent=2),
            ContentType='application/json'
        )
        logger.info("Saved last known draw to S3")
    except Exception as e:
        logger.error(f"Failed to save last known draw: {e}")

def parse_ircc_page(html_content):
    """Parse IRCC page for draw information"""
    draws = []
    
    # Look for draw patterns in the HTML
    # This is a simplified example - you'd need to adapt based on actual IRCC page structure
    
    # Pattern for draw announcements
    draw_patterns = [
        r'Round of invitations.*?(\d{1,2},\d{3}).*?(\d{3,4})',
        r'Express Entry.*?(\d{1,2},\d{3}).*?CRS.*?(\d{3,4})',
        r'Invitations.*?(\d{1,2},\d{3}).*?score.*?(\d{3,4})'
    ]
    
    for pattern in draw_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
        for match in matches:
            itas = int(match[0].replace(',', ''))
            crs = int(match[1])
            
            draw_data = {
                "draw_date": datetime.now().strftime("%Y-%m-%d"),
                "draw_number": len(draws) + 1,
                "itas": itas,
                "crs": crs,
                "cec_itas": int(itas * 0.7),  # Estimate based on typical distribution
                "pnp_itas": int(itas * 0.2),
                "fsw_itas": 0,
                "fst_itas": 0,
                "category_based_total": int(itas * 0.1),
                "french_speaking": 0,
                "healthcare": 0,
                "stem": 0,
                "trade": 0,
                "education": 0,
                "agriculture": 0,
                "draw_type": "program-based",
                "detected_at": datetime.now(timezone.utc).isoformat()
            }
            draws.append(draw_data)
    
    return draws

def fetch_ircc_data():
    """Fetch data from IRCC website"""
    draws = []
    
    for url in IRCC_URLS:
        try:
            logger.info(f"Fetching data from: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse the page for draw information
            page_draws = parse_ircc_page(response.text)
            draws.extend(page_draws)
            
            logger.info(f"Found {len(page_draws)} draws from {url}")
            
        except Exception as e:
            logger.error(f"Error fetching from {url}: {e}")
    
    return draws

def send_github_webhook(draw_data):
    """Send webhook to GitHub"""
    try:
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'event_type': 'express_entry_draw',
            'client_payload': draw_data
        }
        
        response = requests.post(GITHUB_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        logger.info(f"Webhook sent successfully for draw #{draw_data['draw_number']}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send webhook: {e}")
        return False

def lambda_handler(event, context):
    """Main Lambda handler"""
    logger.info("🔄 Starting IRCC monitoring...")
    
    try:
        # Get last known draw
        last_known = get_last_known_draw()
        logger.info(f"Last known draw: {last_known}")
        
        # Fetch current data from IRCC
        current_draws = fetch_ircc_data()
        logger.info(f"Found {len(current_draws)} draws on IRCC website")
        
        # Check for new draws
        new_draws = []
        
        for draw in current_draws:
            # Simple comparison - you might want more sophisticated logic
            if not last_known or (
                draw['itas'] != last_known.get('itas') or
                draw['crs'] != last_known.get('crs') or
                draw['draw_date'] != last_known.get('draw_date')
            ):
                new_draws.append(draw)
        
        logger.info(f"Found {len(new_draws)} new draws")
        
        # Process new draws
        for draw in new_draws:
            logger.info(f"Processing new draw: {draw}")
            
            # Send webhook to GitHub
            if send_github_webhook(draw):
                # Save as last known draw
                save_last_known_draw(draw)
                logger.info(f"✅ Successfully processed draw #{draw['draw_number']}")
            else:
                logger.error(f"❌ Failed to process draw #{draw['draw_number']}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'IRCC monitoring completed',
                'draws_found': len(current_draws),
                'new_draws': len(new_draws)
            })
        }
        
    except Exception as e:
        logger.error(f"❌ Error in lambda_handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

# For local testing
if __name__ == "__main__":
    # Mock environment for testing
    os.environ['GITHUB_TOKEN'] = 'test_token'
    os.environ['GITHUB_REPO'] = 'getguide/immiwatch'
    os.environ['S3_BUCKET'] = 'test-bucket'
    
    # Test the function
    result = lambda_handler({}, None)
    print(json.dumps(result, indent=2)) 