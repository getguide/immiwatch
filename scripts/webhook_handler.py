#!/usr/bin/env python3
"""
Webhook Handler for Express Entry Draw Updates
==============================================

This script handles webhooks from Lambda functions that detect new Express Entry draws.
It automatically processes the draw data and updates the corresponding monthly report.

Usage:
    python3 scripts/webhook_handler.py --webhook-data webhook_data.json
    python3 scripts/webhook_handler.py --test-webhook

Example webhook data:
    {
        "draw_date": "2025-08-05",
        "draw_number": 1,
        "itas": 3000,
        "crs": 475,
        "cec_itas": 2000,
        "pnp_itas": 800,
        "category_based_total": 200,
        "french_speaking": 100,
        "healthcare": 50,
        "education": 50
    }
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path
import argparse
import logging

# Import our existing updater
from update_monthly_report import MonthlyReportUpdater

class WebhookHandler:
    def __init__(self):
        self.base_dir = Path("reports/express-entry")
        self.updater = MonthlyReportUpdater()
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for webhook processing"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('webhook_processing.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def validate_webhook_data(self, data):
        """Validate webhook data structure"""
        required_fields = [
            "draw_date", "draw_number", "itas", "crs"
        ]
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate date format
        try:
            datetime.strptime(data["draw_date"], "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {data['draw_date']}. Use YYYY-MM-DD")
        
        # Validate numeric fields
        numeric_fields = ["draw_number", "itas", "crs"]
        for field in numeric_fields:
            if not isinstance(data[field], (int, float)):
                raise ValueError(f"Field {field} must be numeric")
        
        return True
    
    def extract_month_from_date(self, draw_date):
        """Extract month string from draw date"""
        date_obj = datetime.strptime(draw_date, "%Y-%m-%d")
        return f"{date_obj.year}-{date_obj.month:02d}"
    
    def create_draw_data_file(self, webhook_data):
        """Create draw data file from webhook data"""
        # Extract month
        month_str = self.extract_month_from_date(webhook_data["draw_date"])
        month_info = self.updater.get_month_info(month_str)
        
        # Create draw data structure
        draw_data = {
            "draw_date": webhook_data["draw_date"],
            "draw_number": webhook_data["draw_number"],
            "itas": webhook_data["itas"],
            "crs": webhook_data["crs"],
            "cec_itas": webhook_data.get("cec_itas", 0),
            "pnp_itas": webhook_data.get("pnp_itas", 0),
            "fsw_itas": webhook_data.get("fsw_itas", 0),
            "fst_itas": webhook_data.get("fst_itas", 0),
            "category_based_total": webhook_data.get("category_based_total", 0),
            "french_speaking": webhook_data.get("french_speaking", 0),
            "healthcare": webhook_data.get("healthcare", 0),
            "stem": webhook_data.get("stem", 0),
            "trade": webhook_data.get("trade", 0),
            "education": webhook_data.get("education", 0),
            "agriculture": webhook_data.get("agriculture", 0),
            "draw_type": webhook_data.get("draw_type", "program-based"),
            "notes": f"Automated update from webhook - Draw #{webhook_data['draw_number']}",
            "strategic_insights": [
                f"Draw #{webhook_data['draw_number']} with {webhook_data['itas']} ITAs",
                f"CRS score: {webhook_data['crs']}",
                f"Draw type: {webhook_data.get('draw_type', 'program-based')}"
            ]
        }
        
        # Create filename
        filename = f"webhook_draw_{webhook_data['draw_number']}_{webhook_data['draw_date']}.json"
        filepath = Path("scripts") / filename
        
        # Write draw data file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(draw_data, f, indent=2)
        
        return filepath
    
    def process_webhook(self, webhook_data):
        """Process webhook data and update current monthly report"""
        try:
            self.logger.info("🔄 Processing webhook data...")
            
            # Validate webhook data
            self.logger.info("✅ Validating webhook data...")
            self.validate_webhook_data(webhook_data)
            
            # Use current monthly report manager
            from current_monthly_report_manager import CurrentMonthlyReportManager
            manager = CurrentMonthlyReportManager()
            
            # Get current report info
            current_info = manager.get_current_report_info()
            if not current_info:
                self.logger.error("❌ No current monthly report found")
                return {"success": False, "error": "No current monthly report found"}
            
            self.logger.info(f"📅 Processing for current month: {current_info['month_str']}")
            
            # Update current report with draw data
            self.logger.info("🔄 Updating current monthly report...")
            result = manager.update_current_report_with_draw(webhook_data)
            
            if not result["success"]:
                self.logger.error(f"❌ Failed to update current report: {result['error']}")
                return result
            
            # Create git commit
            self.create_git_commit(webhook_data, current_info['month_str'])
            
            self.logger.info("✅ Webhook processing complete!")
            return {
                "success": True,
                "month": current_info['month_str'],
                "draw_number": webhook_data["draw_number"],
                "updated_file": result["updated_file"],
                "draw_count": result["draw_count"]
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error processing webhook: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_git_commit(self, webhook_data, month_str):
        """Create git commit for the update"""
        try:
            import subprocess
            
            # Add all changes
            subprocess.run(["git", "add", "."], check=True)
            
            # Create commit message
            commit_msg = f"🤖 Auto-update: {month_str} Draw #{webhook_data['draw_number']} - {webhook_data['itas']} ITAs (CRS: {webhook_data['crs']})"
            
            # Commit changes
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            
            # Push to remote
            subprocess.run(["git", "push", "origin", "main"], check=True)
            
            self.logger.info(f"✅ Git commit created: {commit_msg}")
            
        except Exception as e:
            self.logger.error(f"❌ Git commit failed: {e}")
    
    def test_webhook(self):
        """Test webhook with sample data"""
        test_data = {
            "draw_date": "2025-08-05",
            "draw_number": 1,
            "itas": 3000,
            "crs": 475,
            "cec_itas": 2000,
            "pnp_itas": 800,
            "fsw_itas": 0,
            "fst_itas": 0,
            "category_based_total": 200,
            "french_speaking": 100,
            "healthcare": 50,
            "stem": 0,
            "trade": 0,
            "education": 50,
            "agriculture": 0,
            "draw_type": "program-based"
        }
        
        self.logger.info("🧪 Testing webhook with sample data...")
        result = self.process_webhook(test_data)
        
        if result["success"]:
            self.logger.info("✅ Test webhook successful!")
        else:
            self.logger.error(f"❌ Test webhook failed: {result['error']}")
        
        return result

def main():
    parser = argparse.ArgumentParser(description="Process webhook data for Express Entry draws")
    parser.add_argument("--webhook-data", help="JSON file with webhook data")
    parser.add_argument("--test-webhook", action="store_true", help="Test webhook with sample data")
    parser.add_argument("--webhook-json", help="Webhook data as JSON string")
    
    args = parser.parse_args()
    
    handler = WebhookHandler()
    
    try:
        if args.test_webhook:
            result = handler.test_webhook()
        elif args.webhook_data:
            with open(args.webhook_data, 'r', encoding='utf-8') as f:
                webhook_data = json.load(f)
            result = handler.process_webhook(webhook_data)
        elif args.webhook_json:
            webhook_data = json.loads(args.webhook_json)
            result = handler.process_webhook(webhook_data)
        else:
            print("❌ Please provide webhook data via --webhook-data, --webhook-json, or --test-webhook")
            sys.exit(1)
        
        if result["success"]:
            print(f"✅ Webhook processed successfully!")
            print(f"📅 Month: {result.get('month', 'N/A')}")
            print(f"🎯 Draw: #{result.get('draw_number', 'N/A')}")
            print(f"📁 Updated: {result.get('updated_file', 'N/A')}")
        else:
            print(f"❌ Webhook processing failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 