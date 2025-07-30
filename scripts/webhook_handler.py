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
        """Validate webhook data structure from Lambda function"""
        # Check if data has the expected structure
        if "body" not in data:
            raise ValueError("Missing 'body' field in webhook data")
        
        body = data["body"]
        required_fields = [
            "Program", "draw.date.most.recent", "Score", "Invitation", "Draw Number"
        ]
        
        for field in required_fields:
            if field not in body:
                raise ValueError(f"Missing required field in body: {field}")
        
        # Validate date format
        try:
            datetime.strptime(body["draw.date.most.recent"], "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {body['draw.date.most.recent']}. Use YYYY-MM-DD")
        
        # Validate numeric fields
        numeric_fields = ["Score", "Invitation", "Draw Number"]
        for field in numeric_fields:
            if not isinstance(body[field], (int, float)):
                raise ValueError(f"Field {field} must be numeric")
        
        return True
    
    def extract_month_from_date(self, draw_date):
        """Extract month string from draw date"""
        date_obj = datetime.strptime(draw_date, "%Y-%m-%d")
        return f"{date_obj.year}-{date_obj.month:02d}"
    
    def parse_program_category(self, program):
        """Parse program/category from Lambda data"""
        program_mapping = {
            # Program-based draws
            "EE-PNP": {"type": "program-based", "program": "pnp", "category": None},
            "EE-CEC": {"type": "program-based", "program": "cec", "category": None},
            "EE-FSW": {"type": "program-based", "program": "fsw", "category": None},
            "EE-FST": {"type": "program-based", "program": "fst", "category": None},
            
            # Category-based draws
            "EE-Health": {"type": "category-based", "program": None, "category": "healthcare"},
            "EE-French": {"type": "category-based", "program": None, "category": "french_speaking"},
            "EE-Trade": {"type": "category-based", "program": None, "category": "trade"},
            "EE-Education": {"type": "category-based", "program": None, "category": "education"},
            "EE-Agriculture": {"type": "category-based", "program": None, "category": "agriculture"},
            "EE-STEM": {"type": "category-based", "program": None, "category": "stem"}
        }
        
        return program_mapping.get(program, {"type": "unknown", "program": None, "category": None})
    
    def create_draw_data_file(self, webhook_data):
        """Create draw data file from Lambda webhook data"""
        body = webhook_data["body"]
        
        # Parse program/category
        program_info = self.parse_program_category(body["Program"])
        
        # Extract month
        month_str = self.extract_month_from_date(body["draw.date.most.recent"])
        month_info = self.updater.get_month_info(month_str)
        
        # Initialize draw data with zeros
        draw_data = {
            "draw_date": body["draw.date.most.recent"],
            "draw_number": body["Draw Number"],
            "itas": body["Invitation"],
            "crs": body["Score"],
            "cec_itas": 0,
            "pnp_itas": 0,
            "fsw_itas": 0,
            "fst_itas": 0,
            "category_based_total": 0,
            "french_speaking": 0,
            "healthcare": 0,
            "stem": 0,
            "trade": 0,
            "education": 0,
            "agriculture": 0,
            "draw_type": program_info["type"],
            "notes": f"Automated update from Lambda webhook - Draw #{body['Draw Number']} ({body['Program']})",
            "strategic_insights": [
                f"Draw #{body['Draw Number']} with {body['Invitation']} ITAs",
                f"CRS score: {body['Score']}",
                f"Draw type: {program_info['type']}",
                f"Program/Category: {body['Program']}"
            ]
        }
        
        # Set the appropriate field based on program/category
        if program_info["type"] == "program-based":
            if program_info["program"] == "cec":
                draw_data["cec_itas"] = body["Invitation"]
            elif program_info["program"] == "pnp":
                draw_data["pnp_itas"] = body["Invitation"]
            elif program_info["program"] == "fsw":
                draw_data["fsw_itas"] = body["Invitation"]
            elif program_info["program"] == "fst":
                draw_data["fst_itas"] = body["Invitation"]
        elif program_info["type"] == "category-based":
            draw_data["category_based_total"] = body["Invitation"]
            if program_info["category"] == "healthcare":
                draw_data["healthcare"] = body["Invitation"]
            elif program_info["category"] == "french_speaking":
                draw_data["french_speaking"] = body["Invitation"]
            elif program_info["category"] == "trade":
                draw_data["trade"] = body["Invitation"]
            elif program_info["category"] == "education":
                draw_data["education"] = body["Invitation"]
            elif program_info["category"] == "agriculture":
                draw_data["agriculture"] = body["Invitation"]
            elif program_info["category"] == "stem":
                draw_data["stem"] = body["Invitation"]
        
        # Create filename
        filename = f"lambda_draw_{body['Draw Number']}_{body['draw.date.most.recent']}.json"
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
            
            # Extract data from Lambda format
            body = webhook_data["body"]
            draw_number = body["Draw Number"]
            invitations = body["Invitation"]
            crs_score = body["Score"]
            program = body["Program"]
            
            # Create commit message
            commit_msg = f"🤖 Auto-update: {month_str} Draw #{draw_number} ({program}) - {invitations} ITAs (CRS: {crs_score})"
            
            # Commit changes
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            
            # Push to remote
            subprocess.run(["git", "push", "origin", "main"], check=True)
            
            self.logger.info(f"✅ Git commit created: {commit_msg}")
            
        except Exception as e:
            self.logger.error(f"❌ Git commit failed: {e}")
    
    def test_webhook(self):
        """Test webhook with sample Lambda data"""
        test_data = {
            "body": {
                "Program": "EE-PNP",
                "Category": "General",
                "Region": "All",
                "draw.date.most.recent": "2025-08-05",
                "Score": 726,
                "Scoring System": "CRS",
                "Filter by program": "Express Entry",
                "Invitation": 277,
                "Last Checked": "2025-08-05T13:25:51.846699",
                "Draw Number": 348
            }
        }
        
        self.logger.info("🧪 Testing webhook with sample Lambda data...")
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