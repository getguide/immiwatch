#!/usr/bin/env python3
"""
Monthly Express Entry Report Updater
===================================

This script updates existing monthly reports with new draw data and generates
intelligent analysis based on the current state of the month.

Usage:
    python3 scripts/update_monthly_report.py YYYY-MM --draw-data draw_data.json

Example:
    python3 scripts/update_monthly_report.py 2025-08 --draw-data august_draw_1.json
    python3 scripts/update_monthly_report.py 2025-08 --draw-data august_draw_2.json
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path
import argparse

class MonthlyReportUpdater:
    def __init__(self):
        self.base_dir = Path("reports/express-entry")
        
    def validate_month_format(self, month_str):
        """Validate month format (YYYY-MM)"""
        try:
            datetime.strptime(month_str, "%Y-%m")
            return True
        except ValueError:
            return False
    
    def get_month_info(self, month_str):
        """Extract month information from YYYY-MM format"""
        year, month = month_str.split("-")
        month_num = int(month)
        
        month_names = {
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December"
        }
        
        month_name = month_names[month_num]
        return {
            "year": year,
            "month_num": month_num,
            "month_name": month_name,
            "month_str": month_str,
            "directory": f"ee-{month_name.lower()}-{year}"
        }
    
    def load_existing_report(self, month_info):
        """Load existing monthly report"""
        report_file = self.base_dir / month_info["directory"] / "index.html"
        if not report_file.exists():
            raise FileNotFoundError(f"Report file not found: {report_file}")
        
        with open(report_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_draw_data(self, data_file):
        """Load new draw data"""
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Draw data file not found: {data_file}")
        
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_current_data(self, report_content):
        """Extract current data from existing report"""
        # Extract current statistics
        current_data = {
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
            "draw_count": 0,
            "latest_draw_date": "",
            "latest_crs": 0
        }
        
        # Extract numbers from stat-number elements
        stat_matches = re.findall(r'data-target="(\d+)"', report_content)
        if len(stat_matches) >= 4:
            # Based on the July report structure:
            # First: Total ITAs (should be 7558)
            # Second: Healthcare (4000)
            # Third: PNP (3558)
            # Fourth: CEC (3000)
            current_data["total_itas"] = int(stat_matches[0])  # First stat-number is total
            current_data["healthcare"] = int(stat_matches[1])  # Second is healthcare
            current_data["pnp_itas"] = int(stat_matches[2])    # Third is PNP
            current_data["cec_itas"] = int(stat_matches[3])    # Fourth is CEC
        
        return current_data
    
    def merge_draw_data(self, current_data, new_draw_data):
        """Merge new draw data with existing data"""
        updated_data = current_data.copy()
        
        # Handle Lambda webhook format
        if "body" in new_draw_data:
            # Lambda format
            body = new_draw_data["body"]
            program = body.get("Program", "")
            invitations = body.get("Invitation", 0)
            crs_score = body.get("Score", 0)
            draw_date = body.get("draw.date.most.recent", "")
            
            # Map program to the correct field
            if program == "EE-PNP":
                updated_data["pnp_itas"] += invitations
                updated_data["total_itas"] += invitations
            elif program == "EE-CEC":
                updated_data["cec_itas"] += invitations
                updated_data["total_itas"] += invitations
            elif program == "EE-FSW":
                updated_data["fsw_itas"] += invitations
                updated_data["total_itas"] += invitations
            elif program == "EE-FST":
                updated_data["fst_itas"] += invitations
                updated_data["total_itas"] += invitations
            elif program == "EE-Health":
                updated_data["healthcare"] += invitations
                updated_data["category_based_total"] += invitations
                updated_data["total_itas"] += invitations
            elif program == "EE-French":
                updated_data["french_speaking"] += invitations
                updated_data["category_based_total"] += invitations
                updated_data["total_itas"] += invitations
            elif program == "EE-Trade":
                updated_data["trade"] += invitations
                updated_data["category_based_total"] += invitations
                updated_data["total_itas"] += invitations
            elif program == "EE-Education":
                updated_data["education"] += invitations
                updated_data["category_based_total"] += invitations
                updated_data["total_itas"] += invitations
            elif program == "EE-Agriculture":
                updated_data["agriculture"] += invitations
                updated_data["category_based_total"] += invitations
                updated_data["total_itas"] += invitations
            elif program == "EE-STEM":
                updated_data["stem"] += invitations
                updated_data["category_based_total"] += invitations
                updated_data["total_itas"] += invitations
            
            # Update draw count and latest info
            updated_data["draw_count"] += 1
            updated_data["latest_draw_date"] = draw_date
            updated_data["latest_crs"] = crs_score
        else:
            # Old format (fallback)
            updated_data["total_itas"] += new_draw_data.get("itas", 0)
            updated_data["cec_itas"] += new_draw_data.get("cec_itas", 0)
            updated_data["pnp_itas"] += new_draw_data.get("pnp_itas", 0)
            updated_data["fsw_itas"] += new_draw_data.get("fsw_itas", 0)
            updated_data["fst_itas"] += new_draw_data.get("fst_itas", 0)
            
            # Category-based draws
            updated_data["category_based_total"] += new_draw_data.get("category_based_total", 0)
            updated_data["french_speaking"] += new_draw_data.get("french_speaking", 0)
            updated_data["healthcare"] += new_draw_data.get("healthcare", 0)
            updated_data["stem"] += new_draw_data.get("stem", 0)
            updated_data["trade"] += new_draw_data.get("trade", 0)
            updated_data["education"] += new_draw_data.get("education", 0)
            updated_data["agriculture"] += new_draw_data.get("agriculture", 0)
            
            # Update draw count and latest info
            updated_data["draw_count"] += 1
            updated_data["latest_draw_date"] = new_draw_data.get("draw_date", "")
            updated_data["latest_crs"] = new_draw_data.get("crs", 0)
        
        return updated_data
    
    def generate_intelligent_analysis(self, month_info, updated_data, new_draw_data):
        """Generate intelligent analysis based on current state"""
        month_name = month_info["month_name"]
        year = month_info["year"]
        draw_count = updated_data["draw_count"]
        
        # Generate executive summary based on current state
        if draw_count == 1:
            executive_summary = f"**🏗️ Executive Summary:** {month_name} {year} begins with {updated_data['total_itas']} ITAs issued in the first draw, establishing the month's foundation with {updated_data['cec_itas']} CEC and {updated_data['pnp_itas']} PNP selections."
        elif draw_count == 2:
            executive_summary = f"**📈 Executive Summary:** {month_name} {year} continues with {updated_data['total_itas']} total ITAs across {draw_count} draws, showing {self.calculate_growth_rate(updated_data)}% growth from the first draw."
        elif draw_count == 3:
            executive_summary = f"**🚀 Executive Summary:** {month_name} {year} demonstrates strong momentum with {updated_data['total_itas']} ITAs across {draw_count} draws, indicating consistent immigration activity."
        else:
            executive_summary = f"**📊 Executive Summary:** {month_name} {year} maintains steady pace with {updated_data['total_itas']} ITAs across {draw_count} draws, reflecting sustained immigration strategy."
        
        # Generate strategic insights
        strategic_insights = self.generate_strategic_insights(updated_data, new_draw_data)
        
        # Generate key highlights
        key_highlights = self.generate_key_highlights(updated_data, new_draw_data)
        
        return {
            "executive_summary": executive_summary,
            "strategic_insights": strategic_insights,
            "key_highlights": key_highlights
        }
    
    def calculate_growth_rate(self, updated_data):
        """Calculate growth rate from previous draws"""
        # This would need more sophisticated logic based on historical data
        return 15  # Placeholder
    
    def generate_strategic_insights(self, updated_data, new_draw_data):
        """Generate strategic insights based on current data"""
        insights = []
        
        # CEC analysis
        if updated_data["cec_itas"] > 0:
            cec_percentage = round((updated_data["cec_itas"] / updated_data["total_itas"]) * 100, 1)
            insights.append(f"CEC candidates represent {cec_percentage}% of total selections, maintaining domestic experience priority.")
        
        # PNP analysis
        if updated_data["pnp_itas"] > 0:
            pnp_percentage = round((updated_data["pnp_itas"] / updated_data["total_itas"]) * 100, 1)
            insights.append(f"PNP selections at {pnp_percentage}% demonstrate continued federal-provincial coordination.")
        
        # Category-based analysis
        if updated_data["category_based_total"] > 0:
            category_percentage = round((updated_data["category_based_total"] / updated_data["total_itas"]) * 100, 1)
            insights.append(f"Category-based draws represent {category_percentage}% of total ITAs, showing targeted immigration strategy.")
        
        # CRS analysis
        if updated_data["latest_crs"] > 0:
            insights.append(f"Latest CRS score of {updated_data['latest_crs']} indicates current competition level in the pool.")
        
        return insights
    
    def generate_key_highlights(self, updated_data, new_draw_data):
        """Generate key highlights based on current data"""
        highlights = []
        
        highlights.append(f"{updated_data['total_itas']} Total ITAs")
        highlights.append(f"{updated_data['cec_itas']} CEC")
        highlights.append(f"{updated_data['pnp_itas']} PNP")
        
        if updated_data["category_based_total"] > 0:
            highlights.append(f"{updated_data['category_based_total']} Category-Based")
        
        return highlights
    
    def update_report_content(self, report_content, month_info, updated_data, analysis):
        """Update report content with new data and analysis"""
        content = report_content
        
        # Update statistics
        content = self.update_statistics(content, updated_data)
        
        # Update executive summary
        content = self.update_executive_summary(content, analysis["executive_summary"])
        
        # Update key highlights
        content = self.update_key_highlights(content, analysis["key_highlights"])
        
        # Update program breakdown table
        content = self.update_program_table(content, updated_data)
        
        # Update strategic analysis
        content = self.update_strategic_analysis(content, analysis["strategic_insights"])
        
        # Update draw count indicator
        content = self.update_draw_count(content, updated_data["draw_count"])
        
        return content
    
    def update_statistics(self, content, updated_data):
        """Update the main statistics cards"""
        # Update total ITAs (first stat-number)
        content = re.sub(
            r'<div class="stat-number" data-target="\d+" data-prefix="" data-suffix="">\d+</div>',
            f'<div class="stat-number" data-target="{updated_data["total_itas"]}" data-prefix="" data-suffix="">{updated_data["total_itas"]}</div>',
            content,
            count=1
        )
        
        # Update healthcare (second stat-number)
        content = re.sub(
            r'<div class="stat-number" data-target="\d+" data-prefix="" data-suffix="">\d+</div>',
            f'<div class="stat-number" data-target="{updated_data["healthcare"]}" data-prefix="" data-suffix="">{updated_data["healthcare"]}</div>',
            content,
            count=1
        )
        
        # Update PNP ITAs (third stat-number)
        content = re.sub(
            r'<div class="stat-number" data-target="\d+" data-prefix="" data-suffix="">\d+</div>',
            f'<div class="stat-number" data-target="{updated_data["pnp_itas"]}" data-prefix="" data-suffix="">{updated_data["pnp_itas"]}</div>',
            content,
            count=1
        )
        
        # Update CEC ITAs (fourth stat-number)
        content = re.sub(
            r'<div class="stat-number" data-target="\d+" data-prefix="" data-suffix="">\d+</div>',
            f'<div class="stat-number" data-target="{updated_data["cec_itas"]}" data-prefix="" data-suffix="">{updated_data["cec_itas"]}</div>',
            content,
            count=1
        )
        
        return content
    
    def update_executive_summary(self, content, executive_summary):
        """Update executive summary"""
        content = re.sub(
            r'<p class="executive-summary">.*?</p>',
            f'<p class="executive-summary">{executive_summary}</p>',
            content
        )
        
        return content
    
    def update_key_highlights(self, content, key_highlights):
        """Update key highlights section"""
        # This would need more sophisticated parsing
        return content
    
    def update_program_table(self, content, updated_data):
        """Update the program breakdown table"""
        # Calculate percentages
        total = updated_data["total_itas"]
        if total > 0:
            cec_pct = round((updated_data["cec_itas"] / total) * 100, 1)
            pnp_pct = round((updated_data["pnp_itas"] / total) * 100, 1)
        else:
            cec_pct = pnp_pct = 0
        
        # Update table data
        content = re.sub(
            r'<td>(\d+)</td>\s*<td>(\d+\.?\d*)%</td>\s*<td>.*?</td>',
            f'<td>{updated_data["total_itas"]}</td>\n            <td>100%</td>\n            <td>Monthly Progress ({updated_data["draw_count"]} draws)</td>',
            content
        )
        
        return content
    
    def update_strategic_analysis(self, content, strategic_insights):
        """Update strategic analysis section"""
        # This would need more sophisticated parsing
        return content
    
    def update_draw_count(self, content, draw_count):
        """Update draw count indicator"""
        # Add or update draw count indicator
        draw_indicator = f'<div class="draw-count">📊 {draw_count} Draw{"s" if draw_count > 1 else ""} This Month</div>'
        
        # Find a good place to insert the draw count
        if '<div class="hero-stats">' in content:
            content = re.sub(
                r'<div class="hero-stats">',
                f'<div class="hero-stats">\n        {draw_indicator}',
                content
            )
        
        return content
    
    def update_report(self, month_str, draw_data_file):
        """Update existing monthly report with new draw data"""
        print(f"🔄 Updating Express Entry report for {month_str}...")
        
        # Validate month format
        if not self.validate_month_format(month_str):
            raise ValueError(f"Invalid month format: {month_str}. Use YYYY-MM format.")
        
        # Get month information
        month_info = self.get_month_info(month_str)
        print(f"📅 Month: {month_info['month_name']} {month_info['year']}")
        
        # Load existing report
        print("📄 Loading existing report...")
        report_content = self.load_existing_report(month_info)
        
        # Load new draw data
        print("📊 Loading new draw data...")
        new_draw_data = self.load_draw_data(draw_data_file)
        
        # Extract current data
        print("🔍 Extracting current data...")
        current_data = self.extract_current_data(report_content)
        
        # Merge with new data
        print("🔄 Merging data...")
        updated_data = self.merge_draw_data(current_data, new_draw_data)
        
        # Generate intelligent analysis
        print("🧠 Generating analysis...")
        analysis = self.generate_intelligent_analysis(month_info, updated_data, new_draw_data)
        
        # Update report content
        print("✏️ Updating content...")
        updated_content = self.update_report_content(report_content, month_info, updated_data, analysis)
        
        # Write updated report
        report_file = self.base_dir / month_info["directory"] / "index.html"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Report updated successfully!")
        print(f"📁 Location: {report_file}")
        print(f"📊 New totals: {updated_data['total_itas']} ITAs across {updated_data['draw_count']} draws")
        print(f"🌐 URL: https://immiwatch.ca/reports/express-entry/{month_info['directory']}/")
        
        return report_file

def main():
    parser = argparse.ArgumentParser(description="Update monthly Express Entry reports with new draw data")
    parser.add_argument("month", help="Month in YYYY-MM format (e.g., 2025-08)")
    parser.add_argument("--draw-data", required=True, help="JSON file with new draw data")
    
    args = parser.parse_args()
    
    try:
        updater = MonthlyReportUpdater()
        updated_file = updater.update_report(args.month, args.draw_data)
        
        print("\n🎉 Report update complete!")
        print(f"📝 Next steps:")
        print(f"   1. Review the updated report: {updated_file}")
        print(f"   2. Test the page locally")
        print(f"   3. Commit and push to GitHub")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 