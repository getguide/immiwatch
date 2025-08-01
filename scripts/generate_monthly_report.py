#!/usr/bin/env python3
"""
Monthly Express Entry Report Generator
=====================================

This script generates new monthly Express Entry reports by cloning the approved
template design and updating it with new month-specific data.

Usage:
    python3 scripts/generate_monthly_report.py YYYY-MM [--data-file data.json]

Example:
    python3 scripts/generate_monthly_report.py 2025-08
    python3 scripts/generate_monthly_report.py 2025-08 --data-file august_data.json
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path
import argparse

class MonthlyReportGenerator:
    def __init__(self):
        self.base_dir = Path("reports/express-entry")
        self.template_file = Path("scripts/monthly_report_template.html")
        self.output_dir = self.base_dir
        
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
        
        # Month names and emojis
        month_names = {
            1: ("January", "❄️ Foundation Month"),
            2: ("February", "🌸 French-Speaking Launch"),
            3: ("March", "🌱 Spring Expansion"),
            4: ("April", "🌷 Category Diversification"),
            5: ("May", "🌿 Healthcare Focus"),
            6: ("June", "☀️ Summer Acceleration"),
            7: ("July", "🌻 Mid-Year Review"),
            8: ("August", "🍂 Late Summer Push"),
            9: ("September", "🍁 Fall Strategy"),
            10: ("October", "🎃 Q4 Preparation"),
            11: ("November", "🍂 Pre-Year End"),
            12: ("December", "❄️ Year End Review")
        }
        
        month_name, month_emoji = month_names[month_num]
        return {
            "year": year,
            "month_num": month_num,
            "month_name": month_name,
            "month_emoji": month_emoji,
            "month_str": month_str,
            "directory": f"ee-{month_name.lower()}-{year}"
        }
    
    def load_template(self):
        """Load the template HTML file"""
        if not self.template_file.exists():
            raise FileNotFoundError(f"Template file not found: {self.template_file}")
        
        with open(self.template_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_data(self, data_file=None):
        """Load month-specific data"""
        if data_file and os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Default data structure - user can override with data file
        return {
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
            "executive_summary": "Monthly summary placeholder",
            "strategic_insights": [],
            "key_highlights": []
        }
    
    def get_month_specific_content(self, month_info):
        """Get month-specific content and variables"""
        month_name = month_info["month_name"]
        month_lower = month_name.lower()
        year = month_info["year"]
        
        # Month-specific content based on month
        month_content = {
            # Basic variables
            "MONTH_NAME": month_name,
            "MONTH_LOWER": month_lower,
            "YEAR": year,
            
            # Month-specific content
            "MONTH_EMOJI": self.get_month_emoji(month_info["month_num"]),
            "MONTH_STRATEGY": self.get_month_strategy(month_info["month_num"]),
            "MONTH_DESCRIPTION": self.get_month_description(month_info["month_num"]),
            "MONTH_KEYWORDS": f"{self.get_month_strategy(month_info['month_num'])}, immigration planning, Express Entry draws",
            "MONTH_FOCUS": self.get_month_focus(month_info["month_num"]),
            "CHANGE_LABEL": self.get_change_label(month_info["month_num"]),
            "EXECUTIVE_SUMMARY": self.get_executive_summary(month_info["month_num"]),
            "MONTH_STRATEGY_PURPOSE": self.get_strategy_purpose(month_info["month_num"]),
            
            # Status messages
            "FRENCH_STATUS": "Pending",
            "HEALTHCARE_STATUS": "Pending", 
            "STEM_STATUS": "Pending",
            "TRADE_STATUS": "Pending",
            "EDUCATION_STATUS": "Pending",
            "AGRICULTURE_STATUS": "Pending",
            "CEC_STATUS": "Pending",
            "PNP_STATUS": "Pending",
            "FSW_STATUS": "Pending",
            "FST_STATUS": "Pending",
            
            # Analysis content
            "MONTH_STRATEGY_TITLE": f"{month_name} Strategy",
            "MONTH_STRATEGY_DESCRIPTION": self.get_strategy_description(month_info["month_num"]),
            "CEC_ANALYSIS": self.get_cec_analysis(month_info["month_num"]),
            "CEC_POINT_1": "Initial month setup",
            "CEC_POINT_2": "Monitoring for draws",
            "CEC_POINT_3": "Strategic positioning",
            "PNP_ANALYSIS": self.get_pnp_analysis(month_info["month_num"]),
            "PNP_POINT_1": "Provincial coordination",
            "PNP_POINT_2": "Regional focus",
            "PNP_POINT_3": "Quality selection",
            "CATEGORY_ANALYSIS": self.get_category_analysis(month_info["month_num"]),
            "CATEGORY_POINT_1": "System preparation",
            "CATEGORY_POINT_2": "Strategic planning",
            "CATEGORY_POINT_3": "Optimization phase",
            
            # Navigation
            "PREVIOUS_MONTH": self.get_previous_month(month_info["month_num"]),
            "PREVIOUS_MONTH_LOWER": self.get_previous_month(month_info["month_num"]).lower(),
            "NEXT_MONTH": self.get_next_month(month_info["month_num"]),
            "NEXT_MONTH_LOWER": self.get_next_month(month_info["month_num"]).lower(),
            
            # Context
            "YTD_CONTEXT": self.get_ytd_context(month_info["month_num"]),
            "NEXT_MONTH_OUTLOOK": self.get_next_month_outlook(month_info["month_num"]),
            
            # Metrics
            "MONTH_VOLUME_REDUCTION": "0",
            "MONTH_PROGRAM_FOCUS": "0",
            "MONTH_STRATEGIC_NOTE": self.get_strategic_note(month_info["month_num"]),
            
            # Social sharing
            "SHARE_TEXT": f"Express Entry {month_name} {year} Analysis - Track immigration trends and insights",
            "SHARE_URL": f"https://immiwatch.ca/reports/express-entry/ee-{month_lower}-{year}/",
            "SHARE_SUBJECT": f"Express Entry {month_name} {year} Analysis",
            
            # Data targets (will be updated with actual data)
            "TOTAL_ITAS": "0",
            "CATEGORY_BASED": "0", 
            "CATEGORY_TOTAL": "0",
            "PROGRAM_BASED": "0",
            "PROGRAM_TOTAL": "0",
            "CHANGE_FROM_PREVIOUS": "0",
            "CHANGE_PERCENT": "0",
            "TOTAL_LABEL": "Total ITAs - New Month",
            "CEC_ITAS": "0",
            "CEC_PERCENT": "0",
            "PNP_ITAS": "0", 
            "PNP_PERCENT": "0",
            "FRENCH_ITAS": "0",
            "FRENCH_PERCENT": "0",
            "HEALTHCARE_ITAS": "0",
            "HEALTHCARE_PERCENT": "0",
            "STEM_ITAS": "0",
            "STEM_PERCENT": "0",
            "TRADE_ITAS": "0",
            "TRADE_PERCENT": "0",
            "EDUCATION_ITAS": "0",
            "EDUCATION_PERCENT": "0",
            "AGRICULTURE_ITAS": "0",
            "AGRICULTURE_PERCENT": "0",
            "FSW_ITAS": "0",
            "FSW_PERCENT": "0",
            "FST_ITAS": "0",
            "FST_PERCENT": "0",
            "STRATEGY_PURPOSE": f"{month_name} Strategic Focus"
        }
        
        return month_content
    
    def get_month_emoji(self, month_num):
        """Get month-specific emoji"""
        emojis = {
            1: "❄️", 2: "🌸", 3: "🌱", 4: "🌷", 5: "🌿", 6: "☀️",
            7: "🌻", 8: "🍂", 9: "🍁", 10: "🎃", 11: "🍂", 12: "❄️"
        }
        return emojis.get(month_num, "📊")
    
    def get_month_strategy(self, month_num):
        """Get month-specific strategy title"""
        strategies = {
            1: "Foundation Month", 2: "French-Speaking Launch", 3: "Spring Expansion",
            4: "Category Diversification", 5: "Healthcare Focus", 6: "Summer Acceleration",
            7: "Mid-Year Review", 8: "Late Summer Push", 9: "Fall Strategy",
            10: "Q4 Preparation", 11: "Pre-Year End", 12: "Year End Review"
        }
        return strategies.get(month_num, "Strategic Focus")
    
    def get_month_description(self, month_num):
        """Get month-specific description"""
        descriptions = {
            1: "Strategic foundation period with focused immigration planning and system optimization.",
            2: "French-speaking category launch with enhanced linguistic diversity initiatives.",
            3: "Spring expansion phase with increased category-based selections and program diversification.",
            4: "Category diversification period with balanced program and category-based approaches.",
            5: "Healthcare-focused month with targeted medical professional selections.",
            6: "Summer acceleration with increased volume and strategic category rotations.",
            7: "Mid-year strategic review with comprehensive immigration system assessment.",
            8: "Late summer push with focused program-based selections and strategic planning.",
            9: "Fall strategy implementation with renewed category-based initiatives.",
            10: "Q4 preparation phase with year-end immigration planning and optimization.",
            11: "Pre-year end consolidation with strategic program-based selections.",
            12: "Year-end review and strategic planning for upcoming immigration year."
        }
        return descriptions.get(month_num, "Strategic immigration month with focused selections.")
    
    def get_month_focus(self, month_num):
        """Get month-specific focus"""
        focuses = {
            1: "Strategic", 2: "Linguistic", 3: "Expansion", 4: "Diversification",
            5: "Healthcare", 6: "Acceleration", 7: "Review", 8: "Planning",
            9: "Strategy", 10: "Preparation", 11: "Consolidation", 12: "Review"
        }
        return focuses.get(month_num, "Strategic")
    
    def get_change_label(self, month_num):
        """Get month-specific change label"""
        return "Initial Month"
    
    def get_executive_summary(self, month_num):
        """Get month-specific executive summary"""
        summaries = {
            1: f"January {month_num} begins with strategic foundation building and system optimization, setting the stage for a comprehensive immigration year with focused program-based and category-based selections.",
            2: f"February {month_num} launches French-speaking initiatives with enhanced linguistic diversity programs, demonstrating Canada's commitment to bilingual immigration excellence.",
            3: f"March {month_num} represents spring expansion with increased category-based selections and strategic program diversification, building momentum for the immigration year.",
            4: f"April {month_num} focuses on category diversification with balanced program and category-based approaches, demonstrating refined immigration targeting strategies.",
            5: f"May {month_num} emphasizes healthcare-focused selections with targeted medical professional recruitment, addressing critical healthcare sector needs.",
            6: f"June {month_num} accelerates summer immigration with increased volume and strategic category rotations, maintaining momentum through peak activity periods.",
            7: f"July {month_num} conducts mid-year strategic review with comprehensive immigration system assessment and performance optimization.",
            8: f"August {month_num} implements late summer strategic planning with focused program-based selections and system optimization.",
            9: f"September {month_num} launches fall strategy with renewed category-based initiatives and strategic immigration planning.",
            10: f"October {month_num} prepares for Q4 with year-end immigration planning and strategic system optimization.",
            11: f"November {month_num} consolidates pre-year end with strategic program-based selections and comprehensive planning.",
            12: f"December {month_num} conducts year-end review and strategic planning for the upcoming immigration year."
        }
        return summaries.get(month_num, f"Strategic immigration month with focused selections and comprehensive planning.")
    
    def get_strategy_purpose(self, month_num):
        """Get month-specific strategy purpose"""
        purposes = {
            1: "Foundation Building", 2: "Linguistic Diversity", 3: "Spring Expansion",
            4: "Category Diversification", 5: "Healthcare Focus", 6: "Summer Acceleration",
            7: "Mid-Year Review", 8: "Strategic Planning", 9: "Fall Strategy",
            10: "Q4 Preparation", 11: "Year-End Consolidation", 12: "Annual Review"
        }
        return purposes.get(month_num, "Strategic Focus")
    
    def get_strategy_description(self, month_num):
        """Get month-specific strategy description"""
        return f"Strategic immigration planning with focused selections and comprehensive system optimization."
    
    def get_cec_analysis(self, month_num):
        """Get CEC analysis for the month"""
        return f"Canadian Experience Class candidates are positioned for strategic selections with focused program-based approaches."
    
    def get_pnp_analysis(self, month_num):
        """Get PNP analysis for the month"""
        return f"Provincial Nominee Program maintains strategic coordination with federal-provincial partnership focus."
    
    def get_category_analysis(self, month_num):
        """Get category analysis for the month"""
        return f"Category-based draws are strategically planned with system optimization and targeted selections."
    
    def get_previous_month(self, month_num):
        """Get previous month name"""
        months = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
        prev_month = month_num - 1 if month_num > 1 else 12
        return months[prev_month - 1]
    
    def get_next_month(self, month_num):
        """Get next month name"""
        months = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
        next_month = month_num + 1 if month_num < 12 else 1
        return months[next_month - 1]
    
    def get_ytd_context(self, month_num):
        """Get year-to-date context"""
        return f"Strategic immigration planning continues with comprehensive system optimization and focused selections."
    
    def get_next_month_outlook(self, month_num):
        """Get next month outlook"""
        next_month = self.get_next_month(month_num)
        return f"Following current strategic planning, {next_month} is expected to continue with focused immigration selections and system optimization."
    
    def get_strategic_note(self, month_num):
        """Get strategic note for the month"""
        return f"Strategic immigration planning demonstrates sophisticated system optimization and targeted selection approaches."

    def update_content(self, template_content, month_info, data):
        """Update template content with month-specific data"""
        content = template_content
        
        # Get month-specific content
        month_content = self.get_month_specific_content(month_info)
        
        # Replace all variables in template
        for variable, value in month_content.items():
            content = content.replace(f"{{{{{variable}}}}}", str(value))
        
        # Update statistics with actual data
        content = self.update_statistics(content, data)
        
        return content
    
    def update_meta_tags(self, content, month_info):
        """Update meta tags for the new month"""
        month_name = month_info["month_name"]
        year = month_info["year"]
        
        # Update title
        content = re.sub(
            r'<title>.*?</title>',
            f'<title>Express Entry {month_name} {year} - ImmiWatch</title>',
            content
        )
        
        # Update meta description
        content = re.sub(
            r'<meta name="description" content=".*?"',
            f'<meta name="description" content="Express Entry {month_name} {year} analysis with comprehensive immigration insights and strategic recommendations."',
            content
        )
        
        # Update Open Graph tags
        content = re.sub(
            r'<meta property="og:title" content=".*?"',
            f'<meta property="og:title" content="Express Entry {month_name} {year} Analysis"',
            content
        )
        
        content = re.sub(
            r'<meta property="og:description" content=".*?"',
            f'<meta property="og:description" content="Comprehensive Express Entry {month_name} {year} analysis with immigration insights and strategic recommendations."',
            content
        )
        
        return content
    
    def update_breadcrumbs(self, content, month_info):
        """Update breadcrumb navigation"""
        month_name = month_info["month_name"]
        year = month_info["year"]
        
        content = re.sub(
            r'Home › Reports › Express Entry › .*? ›',
            f'Home › Reports › Express Entry › {month_name} {year} ›',
            content
        )
        
        return content
    
    def update_header(self, content, month_info):
        """Update page header and title"""
        month_name = month_info["month_name"]
        month_emoji = month_info["month_emoji"]
        year = month_info["year"]
        
        # Update emoji and title
        content = re.sub(
            r'<h1>Express Entry .*?</h1>',
            f'<h1>Express Entry {month_name} {year}</h1>',
            content
        )
        
        # Update subtitle
        content = re.sub(
            r'<p class="subtitle">.*?</p>',
            f'<p class="subtitle">{month_emoji} {month_name} {year} analysis with strategic insights and immigration recommendations.</p>',
            content
        )
        
        return content
    
    def update_statistics(self, content, data):
        """Update the main statistics cards"""
        # Update total ITAs
        content = re.sub(
            r'<span class="stat-number" data-target="\d+">\d+</span>',
            f'<span class="stat-number" data-target="{data["total_itas"]}">{data["total_itas"]}</span>',
            content,
            count=1
        )
        
        # Update CEC ITAs
        content = re.sub(
            r'<span class="stat-number" data-target="\d+">\d+</span>',
            f'<span class="stat-number" data-target="{data["cec_itas"]}">{data["cec_itas"]}</span>',
            content,
            count=1
        )
        
        # Update PNP ITAs
        content = re.sub(
            r'<span class="stat-number" data-target="\d+">\d+</span>',
            f'<span class="stat-number" data-target="{data["pnp_itas"]}">{data["pnp_itas"]}</span>',
            content,
            count=1
        )
        
        return content
    
    def update_executive_summary(self, content, data):
        """Update executive summary"""
        content = re.sub(
            r'<p class="executive-summary">.*?</p>',
            f'<p class="executive-summary">{data["executive_summary"]}</p>',
            content
        )
        
        return content
    
    def update_key_highlights(self, content, data):
        """Update key highlights section"""
        # This would need more sophisticated parsing based on the actual HTML structure
        # For now, we'll use a simple replacement
        return content
    
    def update_program_table(self, content, data):
        """Update the program breakdown table"""
        # Calculate percentages
        total = data["total_itas"]
        if total > 0:
            cec_pct = round((data["cec_itas"] / total) * 100, 1)
            pnp_pct = round((data["pnp_itas"] / total) * 100, 1)
            fsw_pct = round((data["fsw_itas"] / total) * 100, 1)
            fst_pct = round((data["fst_itas"] / total) * 100, 1)
        else:
            cec_pct = pnp_pct = fsw_pct = fst_pct = 0
        
        # Update table data
        content = re.sub(
            r'<td>(\d+)</td>\s*<td>(\d+\.?\d*)%</td>\s*<td>.*?</td>',
            f'<td>{data["total_itas"]}</td>\n            <td>100%</td>\n            <td>Monthly Foundation</td>',
            content
        )
        
        return content
    
    def update_strategic_analysis(self, content, data):
        """Update strategic analysis section"""
        # This would need more sophisticated parsing
        return content
    
    def update_navigation_links(self, content, month_info):
        """Update navigation links to previous/next months"""
        month_num = month_info["month_num"]
        year = month_info["year"]
        
        # Calculate previous and next months
        if month_num == 1:
            prev_month = f"{int(year)-1}-12"
            prev_name = "December"
            prev_year = int(year) - 1
        else:
            prev_month = f"{year}-{month_num-1:02d}"
            prev_name = self.get_month_info(prev_month)["month_name"]
            prev_year = int(year)
        
        if month_num == 12:
            next_month = f"{int(year)+1}-01"
            next_name = "January"
            next_year = int(year) + 1
        else:
            next_month = f"{year}-{month_num+1:02d}"
            next_name = self.get_month_info(next_month)["month_name"]
            next_year = int(year)
        
        # Update navigation links
        content = re.sub(
            r'← .*? Report',
            f'← {prev_name} {prev_year} Report',
            content
        )
        
        content = re.sub(
            r'.*? Report →',
            f'{next_name} {next_year} Report →',
            content
        )
        
        return content
    
    def update_social_sharing(self, content, month_info):
        """Update social sharing meta tags"""
        month_name = month_info["month_name"]
        year = month_info["year"]
        
        # Update share text
        content = re.sub(
            r'Share This Report',
            f'Share {month_name} {year} Report',
            content
        )
        
        return content
    
    def generate_report(self, month_str, data_file=None):
        """Generate a new monthly report"""
        print(f"🎯 Generating Express Entry report for {month_str}...")
        
        # Validate month format
        if not self.validate_month_format(month_str):
            raise ValueError(f"Invalid month format: {month_str}. Use YYYY-MM format.")
        
        # Get month information
        month_info = self.get_month_info(month_str)
        print(f"📅 Month: {month_info['month_name']} {month_info['year']}")
        
        # Load template
        print("📄 Loading template...")
        template_content = self.load_template()
        
        # Load data
        print("📊 Loading data...")
        data = self.load_data(data_file)
        
        # Update content
        print("🔄 Updating content...")
        updated_content = self.update_content(template_content, month_info, data)
        
        # Create output directory
        output_dir = self.output_dir / month_info["directory"]
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Write output file
        output_file = output_dir / "index.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Report generated successfully!")
        print(f"📁 Location: {output_file}")
        print(f"🌐 URL: https://immiwatch.ca/reports/express-entry/{month_info['directory']}/")
        
        return output_file

def main():
    parser = argparse.ArgumentParser(description="Generate monthly Express Entry reports")
    parser.add_argument("month", help="Month in YYYY-MM format (e.g., 2025-08)")
    parser.add_argument("--data-file", help="JSON file with month-specific data")
    parser.add_argument("--template", help="Custom template file (default: ee-april-2025)")
    
    args = parser.parse_args()
    
    try:
        generator = MonthlyReportGenerator()
        if args.template:
            generator.template_file = Path(args.template)
        
        output_file = generator.generate_report(args.month, args.data_file)
        
        print("\n🎉 Report generation complete!")
        print(f"📝 Next steps:")
        print(f"   1. Review the generated report: {output_file}")
        print(f"   2. Update the data if needed")
        print(f"   3. Test the page locally")
        print(f"   4. Commit and push to GitHub")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 