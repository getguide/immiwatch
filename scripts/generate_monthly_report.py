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
        self.template_file = self.base_dir / "ee-april-2025" / "index.html"
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
    
    def update_content(self, template_content, month_info, data):
        """Update template content with month-specific information"""
        content = template_content
        
        # Update meta tags
        content = self.update_meta_tags(content, month_info)
        
        # Update navigation breadcrumbs
        content = self.update_breadcrumbs(content, month_info)
        
        # Update page title and header
        content = self.update_header(content, month_info)
        
        # Update statistics
        content = self.update_statistics(content, data)
        
        # Update executive summary
        content = self.update_executive_summary(content, data)
        
        # Update key highlights
        content = self.update_key_highlights(content, data)
        
        # Update program breakdown table
        content = self.update_program_table(content, data)
        
        # Update strategic analysis
        content = self.update_strategic_analysis(content, data)
        
        # Update navigation links
        content = self.update_navigation_links(content, month_info)
        
        # Update social sharing
        content = self.update_social_sharing(content, month_info)
        
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