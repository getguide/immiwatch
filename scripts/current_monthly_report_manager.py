#!/usr/bin/env python3
"""
Current Monthly Report Manager
==============================

This script manages the "current monthly report" system:
1. Creates new monthly reports at the start of each month
2. Designates the current month's report as the active one
3. Updates the current report designation
4. Provides utilities for webhook updates

Usage:
    python3 scripts/current_monthly_report_manager.py --create-current
    python3 scripts/current_monthly_report_manager.py --get-current
    python3 scripts/current_monthly_report_manager.py --update-current
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import logging
from generate_monthly_report import MonthlyReportGenerator

class CurrentMonthlyReportManager:
    def __init__(self):
        self.base_dir = Path("reports/express-entry")
        self.current_file = Path("scripts/current_monthly_report.json")
        self.generator = MonthlyReportGenerator()
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for current report management"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('current_report_management.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_current_month_info(self):
        """Get current month information"""
        now = datetime.now()
        month_str = f"{now.year}-{now.month:02d}"
        
        month_info = {
            "year": now.year,
            "month": now.month,
            "month_name": now.strftime("%B"),
            "month_short": now.strftime("%b"),
            "directory": f"ee-{now.strftime('%B').lower()}-{now.year}",
            "url_path": f"reports/express-entry/ee-{now.strftime('%B').lower()}-{now.year}/",
            "is_current_month": True
        }
        
        return month_str, month_info
    
    def get_next_month_info(self):
        """Get next month information - actually gets current month when on first day"""
        now = datetime.now()
        
        # If we're on the first day of the month, we want to create the current month
        # not the next month
        if now.day == 1:
            target_month = now
        else:
            # For other days, get the next month
            target_month = now.replace(day=1) + timedelta(days=32)
            target_month = target_month.replace(day=1)
        
        month_str = f"{target_month.year}-{target_month.month:02d}"
        
        month_info = {
            "year": target_month.year,
            "month": target_month.month,
            "month_name": target_month.strftime("%B"),
            "month_short": target_month.strftime("%b"),
            "directory": f"ee-{target_month.strftime('%B').lower()}-{target_month.year}",
            "url_path": f"reports/express-entry/ee-{target_month.strftime('%B').lower()}-{target_month.year}/",
            "is_current_month": True
        }
        
        return month_str, month_info
    
    def load_current_report_info(self):
        """Load current report information from file"""
        try:
            if self.current_file.exists():
                with open(self.current_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return None
        except Exception as e:
            self.logger.error(f"Error loading current report info: {e}")
            return None
    
    def save_current_report_info(self, report_info):
        """Save current report information to file"""
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                json.dump(report_info, f, indent=2)
            self.logger.info(f"✅ Saved current report info: {report_info['month_str']}")
        except Exception as e:
            self.logger.error(f"Error saving current report info: {e}")
    
    def create_initial_monthly_data(self, month_str, month_info):
        """Create initial data for a new monthly report"""
        initial_data = {
            "total_itas": 0,
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
            "executive_summary": f"{month_info['month_name']} {month_info['year']} begins with automated monitoring. This report will be updated automatically as new Express Entry draws are announced throughout the month.",
            "strategic_insights": [
                f"Month initialized on {datetime.now().strftime('%B %d, %Y')}",
                "Automated draw monitoring active",
                "Real-time updates enabled",
                "Intelligent analysis pending first draw"
            ],
            "key_highlights": [
                "0 Total ITAs",
                "0 CEC",
                "0 PNP", 
                "Automated Processing"
            ],
            "month_str": month_str,
            "month_info": month_info,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "draw_count": 0,
            "status": "initialized"
        }
        
        return initial_data
    
    def create_current_monthly_report(self):
        """Create the current month's report if it doesn't exist"""
        try:
            month_str, month_info = self.get_current_month_info()
            self.logger.info(f"🔄 Creating current monthly report for {month_str}")
            
            # Check if report already exists
            report_file = self.base_dir / month_info["directory"] / "index.html"
            
            if report_file.exists():
                self.logger.info(f"✅ Report already exists: {report_file}")
                return self.update_current_report_designation(month_str, month_info)
            
            # Create initial data
            initial_data = self.create_initial_monthly_data(month_str, month_info)
            
            # Save initial data file
            initial_file = Path("scripts") / f"current_monthly_{month_str}.json"
            with open(initial_file, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=2)
            
            # Generate the report
            self.logger.info("📄 Generating monthly report...")
            generated_file = self.generator.generate_report(month_str, str(initial_file))
            
            # Update current report designation
            self.update_current_report_designation(month_str, month_info)
            
            self.logger.info(f"✅ Successfully created current monthly report: {generated_file}")
            return {
                "success": True,
                "month_str": month_str,
                "month_info": month_info,
                "report_file": str(generated_file),
                "status": "created"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error creating current monthly report: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def update_current_report_designation(self, month_str, month_info):
        """Update the current report designation"""
        try:
            current_info = {
                "month_str": month_str,
                "month_info": month_info,
                "designated_at": datetime.now().isoformat(),
                "report_url": f"https://immiwatch.ca/{month_info['url_path']}",
                "local_path": str(self.base_dir / month_info["directory"] / "index.html"),
                "status": "current"
            }
            
            self.save_current_report_info(current_info)
            
            # Create a symbolic link or reference file for easy access
            current_link = Path("scripts/current_monthly_report_link.txt")
            with open(current_link, 'w', encoding='utf-8') as f:
                f.write(f"Current Monthly Report: {month_str}\n")
                f.write(f"URL: {current_info['report_url']}\n")
                f.write(f"Local Path: {current_info['local_path']}\n")
                f.write(f"Designated: {current_info['designated_at']}\n")
            
            self.logger.info(f"✅ Updated current report designation: {month_str}")
            return current_info
            
        except Exception as e:
            self.logger.error(f"❌ Error updating current report designation: {e}")
            return None
    
    def get_current_report_info(self):
        """Get information about the current monthly report"""
        try:
            current_info = self.load_current_report_info()
            
            if current_info:
                self.logger.info(f"📋 Current report: {current_info['month_str']}")
                return current_info
            else:
                # If no current designation, create one for current month
                self.logger.info("⚠️ No current report designation found, creating one...")
                return self.create_current_monthly_report()
                
        except Exception as e:
            self.logger.error(f"❌ Error getting current report info: {e}")
            return None
    
    def update_current_report_with_draw(self, draw_data):
        """Update the current monthly report with new draw data"""
        try:
            current_info = self.get_current_report_info()
            
            if not current_info:
                self.logger.error("❌ No current report found")
                return {"success": False, "error": "No current report found"}
            
            # Import the updater
            from update_monthly_report import MonthlyReportUpdater
            updater = MonthlyReportUpdater()
            
            # Create draw data file
            draw_file = Path("scripts") / f"current_draw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(draw_file, 'w', encoding='utf-8') as f:
                json.dump(draw_data, f, indent=2)
            
            # Update the current report
            month_str = current_info['month_str']
            updated_file = updater.update_report(month_str, str(draw_file))
            
            # Update current info
            current_info['last_updated'] = datetime.now().isoformat()
            current_info['draw_count'] = current_info.get('draw_count', 0) + 1
            self.save_current_report_info(current_info)
            
            self.logger.info(f"✅ Updated current report with draw data: {updated_file}")
            return {
                "success": True,
                "month_str": month_str,
                "updated_file": str(updated_file),
                "draw_count": current_info['draw_count']
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error updating current report: {e}")
            return {"success": False, "error": str(e)}
    
    def check_and_create_next_month_report(self):
        """Check if we need to create next month's report"""
        try:
            now = datetime.now()
            current_month_str, _ = self.get_current_month_info()
            next_month_str, next_month_info = self.get_next_month_info()
            
            # Check if we're at the start of a new month
            if now.day == 1 and now.hour < 6:  # Early morning of first day
                self.logger.info(f"🔄 First day of month detected: {next_month_str}")
                
                # Create next month's report
                initial_data = self.create_initial_monthly_data(next_month_str, next_month_info)
                
                # Save initial data file
                initial_file = Path("scripts") / f"next_monthly_{next_month_str}.json"
                with open(initial_file, 'w', encoding='utf-8') as f:
                    json.dump(initial_data, f, indent=2)
                
                # Generate the report
                generated_file = self.generator.generate_report(next_month_str, str(initial_file))
                
                # Update current report designation to new month
                self.update_current_report_designation(next_month_str, next_month_info)
                
                self.logger.info(f"✅ Created and designated new month report: {next_month_str}")
                
                # Output results for GitHub Actions
                print(f"::set-output name=status::month_transition")
                print(f"::set-output name=new_month::{next_month_str}")
                print(f"::set-output name=report_file::{generated_file}")
                print(f"::set-output name=new_month_directory::{next_month_info['directory']}")
                
                return {
                    "success": True,
                    "new_month": next_month_str,
                    "report_file": str(generated_file),
                    "status": "month_transition"
                }
            
            # Output results for GitHub Actions
            print(f"::set-output name=status::no_transition_needed")
            print(f"::set-output name=current_month::{current_month_str}")
            
            return {"success": True, "status": "no_transition_needed"}
            
        except Exception as e:
            self.logger.error(f"❌ Error checking month transition: {e}")
            
            # Output error for GitHub Actions
            print(f"::set-output name=status::error")
            print(f"::set-output name=error::{str(e)}")
            
            return {"success": False, "error": str(e)}
    
    def get_report_status_summary(self):
        """Get a summary of all monthly reports"""
        try:
            reports = []
            
            # Get current report info
            current_info = self.get_current_report_info()
            
            # Scan for all monthly reports
            for report_dir in self.base_dir.glob("ee-*-2025"):
                if report_dir.is_dir():
                    report_file = report_dir / "index.html"
                    if report_file.exists():
                        # Extract month info from directory name
                        dir_name = report_dir.name
                        match = re.match(r'ee-(\w+)-(\d{4})', dir_name)
                        if match:
                            month_name, year = match.groups()
                            month_str = f"{year}-{self.get_month_number(month_name):02d}"
                            
                            reports.append({
                                "month_str": month_str,
                                "month_name": month_name.title(),
                                "year": year,
                                "path": str(report_file),
                                "url": f"https://immiwatch.ca/reports/express-entry/{dir_name}/",
                                "is_current": current_info and current_info['month_str'] == month_str,
                                "exists": True
                            })
            
            # Sort by month
            reports.sort(key=lambda x: x['month_str'])
            
            return {
                "current_report": current_info,
                "all_reports": reports,
                "total_reports": len(reports)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error getting report summary: {e}")
            return None
    
    def get_month_number(self, month_name):
        """Get month number from month name"""
        months = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
        return months.get(month_name.lower(), 1)

def main():
    parser = argparse.ArgumentParser(description="Manage current monthly Express Entry reports")
    parser.add_argument("--create-current", action="store_true", help="Create current month's report")
    parser.add_argument("--get-current", action="store_true", help="Get current report information")
    parser.add_argument("--update-current", action="store_true", help="Update current report designation")
    parser.add_argument("--check-transition", action="store_true", help="Check for month transition")
    parser.add_argument("--status", action="store_true", help="Get status summary of all reports")
    parser.add_argument("--test", action="store_true", help="Test the system")
    
    args = parser.parse_args()
    
    manager = CurrentMonthlyReportManager()
    
    try:
        if args.create_current:
            result = manager.create_current_monthly_report()
            if result["success"]:
                print(f"✅ Created current report: {result['month_str']}")
            else:
                print(f"❌ Failed: {result['error']}")
                
        elif args.get_current:
            info = manager.get_current_report_info()
            if info:
                print(f"📋 Current report: {info['month_str']}")
                print(f"📁 Path: {info['local_path']}")
                print(f"🌐 URL: {info['report_url']}")
            else:
                print("❌ No current report found")
                
        elif args.update_current:
            month_str, month_info = manager.get_current_month_info()
            result = manager.update_current_report_designation(month_str, month_info)
            if result:
                print(f"✅ Updated current designation: {result['month_str']}")
            else:
                print("❌ Failed to update designation")
                
        elif args.check_transition:
            result = manager.check_and_create_next_month_report()
            if result["success"]:
                if result["status"] == "month_transition":
                    print(f"✅ Month transition: {result['new_month']}")
                else:
                    print("ℹ️ No transition needed")
            else:
                print(f"❌ Error: {result['error']}")
                
        elif args.status:
            summary = manager.get_report_status_summary()
            if summary:
                print(f"📊 Report Status Summary")
                print(f"Current: {summary['current_report']['month_str']}")
                print(f"Total Reports: {summary['total_reports']}")
                print("\nAll Reports:")
                for report in summary['all_reports']:
                    status = "🟢 CURRENT" if report['is_current'] else "⚪"
                    print(f"  {status} {report['month_name']} {report['year']} - {report['url']}")
            else:
                print("❌ Failed to get status")
                
        elif args.test:
            print("🧪 Testing current monthly report manager...")
            
            # Test current report creation
            result = manager.create_current_monthly_report()
            print(f"Create test: {'✅' if result['success'] else '❌'}")
            
            # Test current report info
            info = manager.get_current_report_info()
            print(f"Get info test: {'✅' if info else '❌'}")
            
            # Test status summary
            summary = manager.get_report_status_summary()
            print(f"Status test: {'✅' if summary else '❌'}")
            
            print("✅ Test completed")
            
        else:
            print("❌ Please specify an action: --create-current, --get-current, --update-current, --check-transition, --status, or --test")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 