#!/usr/bin/env python3
"""
🎯 Draw News Automation System
Specialized automation for Express Entry draw news using the GOLD STANDARD template.
"""

import json
import os
import re
import sys
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DrawAutomationSystem:
    """Specialized automation system for draw news articles."""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.template_path = self.base_path / "scripts" / "draw_news_template.html"
        self.draws_path = self.base_path / "news" / "daily" / "draws"
        self.daily_index_path = self.base_path / "news" / "daily" / "index.html"
        
        # Load template
        with open(self.template_path, 'r', encoding='utf-8') as f:
            self.template = f.read()
        
        # Draw type configurations
        self.draw_types = {
            "CEC": {
                "icon": "🇨🇦",
                "name": "CEC",
                "gradient": "#059669 0%, #047857 100%",
                "summary": "Canadian Experience Class: Targeted draw for candidates with Canadian work experience"
            },
            "Health": {
                "icon": "🏥",
                "name": "Health",
                "gradient": "#dc2626 0%, #b91c1c 100%",
                "summary": "Healthcare Occupations: Targeted draw for healthcare professionals"
            },
            "PNP": {
                "icon": "🏛️",
                "name": "PNP",
                "gradient": "#1e40af 0%, #3730a3 100%",
                "summary": "Provincial Nominee Program: Program-specific draw for PNP candidates"
            },
            "General": {
                "icon": "🌐",
                "name": "General",
                "gradient": "#059669 0%, #047857 100%",
                "summary": "General Draw: All programs eligible for this round"
            },
            "FSTP": {
                "icon": "🔧",
                "name": "FSTP",
                "gradient": "#7c3aed 0%, #6d28d9 100%",
                "summary": "Federal Skilled Trades Program: Targeted draw for skilled trades"
            },
            "FSWP": {
                "icon": "👔",
                "name": "FSWP",
                "gradient": "#059669 0%, #047857 100%",
                "summary": "Federal Skilled Worker Program: Targeted draw for skilled workers"
            }
        }
        
        # Impact level mapping
        self.impact_levels = {
            "High": {"class": "high", "text": "High Impact"},
            "Critical": {"class": "critical", "text": "Critical Impact"},
            "Moderate": {"class": "high", "text": "Moderate Impact"},
            "Low": {"class": "high", "text": "Low Impact"}
        }
    
    def analyze_draw_data(self, data: Dict) -> Dict:
        """Analyze draw data and generate enhanced content using AI-like analysis."""
        
        # Extract basic data
        itas = data.get('invitation', 0)
        crs = data.get('cutoff', 0)
        draw_type = data.get('draw_type', 'General')
        date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        # Determine impact level based on data
        if itas >= 4000:
            impact_level = "Critical"
        elif itas >= 2000:
            impact_level = "High"
        elif itas >= 1000:
            impact_level = "Moderate"
        else:
            impact_level = "Low"
        
        # Generate draw-specific content
        draw_config = self.draw_types.get(draw_type, self.draw_types["General"])
        
        # Generate title
        title = f"Express Entry {draw_type} Draw: {itas:,} ITAs Issued at CRS {crs}"
        
        # Generate description
        description = f"Express Entry {draw_type} draw issued {itas:,} ITAs with minimum CRS score of {crs} on {self.format_date(date)}. Analysis of {draw_type.lower()}-specific selection strategy and trends."
        
        # Generate keywords
        keywords = f"Express Entry, {draw_type} draw, {itas} ITAs, CRS {crs}, IRCC, immigration Canada, {self.format_date(date, 'month_year')}"
        
        # Generate executive summary
        executive_summary = f"On {self.format_date(date)}, IRCC conducted an Express Entry draw targeting {draw_type} candidates. A total of {itas:,} Invitations to Apply (ITAs) were issued to candidates with a minimum CRS score of {crs}. This {draw_type.lower()}-specific draw continues IRCC's strategy of targeted immigration, focusing on candidates with specific qualifications and experience."
        
        # Generate immediate effects
        immediate_effects = f"{itas:,} {draw_type} candidates invited to apply for permanent residence. CRS threshold of {crs} reflects the competitive nature of {draw_type} selections."
        
        # Generate strategic implications
        strategic_implications = f"Program-specific draw strategy continues, indicating IRCC's commitment to targeted immigration pathways and addressing specific labour market needs."
        
        # Generate quick facts
        quick_facts = [
            f"{draw_type}-only draw targeting candidates with specific qualifications",
            f"CRS threshold of {crs} reflects competitive nature of {draw_type} selections",
            f"Program-specific strategy continues IRCC's targeted immigration approach",
            f"{draw_type} candidates typically have strong profiles and qualifications",
            f"Demonstrates commitment to addressing specific labour market needs"
        ]
        
        # Generate user impact content
        user_impact = self.generate_user_impact(draw_type, itas, crs)
        
        # Generate next steps
        next_steps = self.generate_next_steps(draw_type, crs)
        
        # Generate draw details
        draw_details = [
            f"<li><strong>Draw Type:</strong> {draw_type}-Only (Program-Specific)</li>",
            f"<li><strong>ITAs Issued:</strong> {itas:,}</li>",
            f"<li><strong>Minimum CRS Score:</strong> {crs} points</li>",
            f"<li><strong>Draw Date:</strong> {self.format_date(date)}</li>",
            f"<li><strong>Tie-breaking Rule:</strong> {self.generate_tie_breaking_date(date)}</li>",
            f"<li><strong>Target Program:</strong> {draw_type}</li>"
        ]
        
        # Generate source links
        source_links = [
            '<li><a href="https://www.canada.ca/en/immigration-refugees-citizenship/corporate/mandate/policies-operational-instructions-agreements/ministerial-instructions/express-entry-rounds.html" target="_blank">🔗 IRCC Express Entry Rounds of Invitations</a></li>',
            '<li><a href="https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry.html" target="_blank">🔗 Express Entry System Information</a></li>',
            '<li><a href="https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/eligibility/criteria-comprehensive-ranking-system.html" target="_blank">🔗 Comprehensive Ranking System Guide</a></li>'
        ]
        
        # Generate tags
        tags = [
            '<a href="#" class="news-tag">Express Entry</a>',
            f'<a href="#" class="news-tag">{draw_type} Draw</a>',
            f'<a href="#" class="news-tag">{itas} ITAs</a>',
            f'<a href="#" class="news-tag">CRS {crs}</a>',
            '<a href="#" class="news-tag">IRCC</a>',
            f'<a href="#" class="news-tag">{draw_type}</a>',
            f'<a href="#" class="news-tag">{self.format_date(date, "month_year")}</a>'
        ]
        
        # Generate article content
        article_content = self.generate_article_content(draw_type, itas, crs, date)
        
        return {
            "title": title,
            "description": description,
            "keywords": keywords,
            "executive_summary": executive_summary,
            "immediate_effects": immediate_effects,
            "strategic_implications": strategic_implications,
            "quick_facts": quick_facts,
            "user_impact": user_impact,
            "next_steps": next_steps,
            "draw_details": draw_details,
            "source_links": source_links,
            "tags": tags,
            "article_content": article_content,
            "draw_config": draw_config,
            "impact_level": impact_level,
            "itas": itas,
            "crs": crs,
            "draw_type": draw_type,
            "date": date
        }
    
    def generate_user_impact(self, draw_type: str, itas: int, crs: int) -> Dict:
        """Generate user impact content based on draw type."""
        
        if draw_type == "CEC":
            return {
                "user_type_1": {
                    "icon": "🇨🇦",
                    "title": "CEC Candidates",
                    "description": f"If you have Canadian work experience and a CRS score of {crs-20}+, this draw significantly improves your chances. CEC candidates have enhanced opportunities in program-specific draws."
                },
                "user_type_2": {
                    "icon": "📋",
                    "title": "Immigration Practitioners",
                    "description": f"Advise CEC clients to maintain strong CRS scores and prepare for program-specific draws. Monitor CEC trends and eligibility criteria."
                },
                "user_type_3": {
                    "icon": "🏢",
                    "title": "Canadian Employers",
                    "description": "This draw validates the importance of retaining skilled workers with Canadian experience. Employers can continue to support CEC pathways."
                }
            }
        elif draw_type == "Health":
            return {
                "user_type_1": {
                    "icon": "🏥",
                    "title": "Healthcare Professionals",
                    "description": f"If you work in healthcare and have a CRS score of {crs-20}+, this draw provides excellent opportunities. Healthcare draws offer competitive thresholds."
                },
                "user_type_2": {
                    "icon": "📋",
                    "title": "Immigration Practitioners",
                    "description": f"Advise healthcare clients to prepare for program-specific draws. Monitor healthcare occupation trends and requirements."
                },
                "user_type_3": {
                    "icon": "🏥",
                    "title": "Healthcare Employers",
                    "description": "This draw addresses critical healthcare labour shortages. Employers can recruit qualified healthcare professionals."
                }
            }
        else:
            return {
                "user_type_1": {
                    "icon": "👥",
                    "title": "Express Entry Candidates",
                    "description": f"If you have a CRS score of {crs-20}+, this draw provides opportunities. Program-specific draws offer targeted pathways."
                },
                "user_type_2": {
                    "icon": "📋",
                    "title": "Immigration Practitioners",
                    "description": f"Advise clients about program-specific opportunities. Monitor draw trends and prepare candidates accordingly."
                },
                "user_type_3": {
                    "icon": "🏢",
                    "title": "Employers",
                    "description": "This draw creates opportunities to recruit qualified international talent. Monitor candidate availability."
                }
            }
    
    def generate_next_steps(self, draw_type: str, crs: int) -> List[str]:
        """Generate next steps based on draw type."""
        
        steps = [
            f"<li><div class=\"step-number\">1</div><strong>Check Your CRS Score:</strong> Ensure your score meets the {crs} threshold for {draw_type} draws</li>",
            f"<li><div class=\"step-number\">2</div><strong>Verify Eligibility:</strong> Confirm you meet {draw_type} program requirements</li>",
            f"<li><div class=\"step-number\">3</div><strong>Update Your Profile:</strong> Ensure your Express Entry profile reflects your {draw_type} status</li>",
            f"<li><div class=\"step-number\">4</div><strong>Monitor Future {draw_type} Draws:</strong> Stay updated on upcoming program-specific draws</li>"
        ]
        
        return steps
    
    def generate_article_content(self, draw_type: str, itas: int, crs: int, date: str) -> str:
        """Generate the main article content."""
        
        content = f"""
        <h3>📈 Strategic Analysis</h3>
        
        <h4>Program-Specific Selection Strategy</h4>
        <p>
            This {draw_type}-only draw exemplifies IRCC's continued commitment to program-specific selection strategies. By targeting {draw_type} candidates exclusively, IRCC can address the specific need to attract qualified professionals in this category.
        </p>

        <h4>Competitive CRS Threshold</h4>
        <p>
            The minimum CRS score of {crs} is competitive, reflecting the high value placed on {draw_type} qualifications. This threshold indicates that {draw_type} candidates are expected to have strong profiles, including relevant experience, language proficiency, and education credentials.
        </p>

        <h4>{draw_type} Program Focus</h4>
        <p>
            This draw underscores the importance of {draw_type} qualifications in Canada's immigration strategy. {draw_type} candidates bring proven skills and experience, making them highly valuable contributors to the economy.
        </p>

        <h3>🇨🇦 {draw_type} Program Context</h3>
        
        <h4>Enhanced Candidate Profiles</h4>
        <p>
            {draw_type} candidates typically have stronger profiles than general Express Entry candidates, including relevant experience, proven language skills, and familiarity with Canadian requirements. This is reflected in the competitive CRS threshold for {draw_type}-specific draws.
        </p>

        <h4>Economic Integration</h4>
        <p>
            {draw_type} candidates are selected based on their proven ability to contribute to the Canadian economy through their qualifications and experience. This targeted approach ensures that immigration supports economic growth and labour market integration.
        </p>

        <h3>📊 Professional Recommendations</h3>
        
        <h4>For {draw_type} Candidates</h4>
        <p>
            <strong>Enhanced Opportunities:</strong> {draw_type} candidates with CRS scores of {crs-20}+ should consider Express Entry as a viable pathway to permanent residence. Program-specific draws provide significant advantages for qualified candidates.
        </p>
        
        <h4>For Immigration Practitioners</h4>
        <p>
            <strong>Strategic Planning:</strong> Advise {draw_type} clients to maintain strong CRS scores and prepare for program-specific draws. Monitor {draw_type} trends and eligibility criteria for optimal positioning.
        </p>
        
        <h4>For Canadian Employers</h4>
        <p>
            <strong>Recruitment Strategy:</strong> This draw validates the importance of supporting {draw_type} pathways for skilled professionals. Employers can continue to support employees in their immigration journey.
        </p>

        <h3>🔮 Future Outlook</h3>
        
        <h4>Continued Program-Specific Strategy</h4>
        <p>
            IRCC is expected to continue program-specific draws throughout 2025, with {draw_type} draws likely remaining a priority. The success of this targeted approach may lead to additional {draw_type}-focused rounds.
        </p>

        <h4>{draw_type} Program Evolution</h4>
        <p>
            IRCC may continue to evolve {draw_type} criteria to attract candidates with the most valuable qualifications and experience, ensuring that the program remains competitive and effective.
        </p>

        <h3>📈 Economic and Social Impact</h3>
        
        <h4>Economic Integration</h4>
        <p>
            The {itas:,} {draw_type} candidates invited in this draw will contribute significantly to Canada's economy through their proven qualifications and experience. These professionals will help address labour market needs and support economic growth.
        </p>

        <h4>Social Integration</h4>
        <p>
            {draw_type} candidates bring valuable qualifications and experience, promoting social integration and contributing to a diverse and skilled workforce.
        </p>
        """
        
        return content
    
    def format_date(self, date_str: str, format_type: str = "full") -> str:
        """Format date string."""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            if format_type == "month_year":
                return date_obj.strftime('%B %Y')
            elif format_type == "short":
                return date_obj.strftime('%B %-d')
            else:
                return date_obj.strftime('%B %-d, %Y')
        except:
            return date_str
    
    def generate_tie_breaking_date(self, date_str: str) -> str:
        """Generate tie-breaking date based on draw date."""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            # Tie-breaking is typically 3-7 days before the draw
            tie_breaking = date_obj.replace(day=date_obj.day - 3)
            return f"{tie_breaking.strftime('%B %-d, %Y')} at {tie_breaking.strftime('%H:%M:%S')} UTC"
        except:
            return "TBD"
    
    def create_slug(self, title: str) -> str:
        """Create URL slug from title."""
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def replace_template_variables(self, analysis: Dict) -> str:
        """Replace all template variables with actual data."""
        
        # Prepare template variables
        template_vars = {
            "TITLE": analysis["title"],
            "ARTICLE_TITLE": analysis["title"],  # Added missing ARTICLE_TITLE
            "DRAW_TYPE": analysis["draw_type"],  # Added missing DRAW_TYPE
            "DESCRIPTION": analysis["description"],
            "KEYWORDS": analysis["keywords"],
            "PUBLISH_DATE": analysis["date"],
            "PUBLISH_DATE_FORMATTED": self.format_date(analysis["date"]),
            "PUBLISH_TIME": f"{analysis['date']}T15:00:00Z",
            "IMPACT_LEVEL": analysis["impact_level"],
            "IMPACT_CLASS": self.impact_levels[analysis["impact_level"]]["class"],
            "IMPACT_TEXT": self.impact_levels[analysis["impact_level"]]["text"],
            "SOURCE": "IRCC Official",
            "HEADER_GRADIENT": analysis["draw_config"]["gradient"],
            "FAVICON_PATH": "../../../../../favicon.svg",
            "CSS_PATH": "../../../../../assets/css/shared-styles.css",
            "OG_IMAGE": f"https://immiwatch.ca/assets/images/express-entry-{analysis['draw_type'].lower()}-draw.svg",
            "ITAS_ISSUED": f"{analysis['itas']:,}",
            "CRS_CUTOFF": str(analysis["crs"]),
            "DRAW_TYPE_ICON": analysis["draw_config"]["icon"],
            "DRAW_TYPE_NAME": analysis["draw_config"]["name"],
            "DRAW_DATE_FORMATTED": self.format_date(analysis["date"], "short"),
            "DRAW_SUMMARY": analysis["draw_config"]["summary"],
            "EXECUTIVE_SUMMARY": analysis["executive_summary"],
            "IMMEDIATE_EFFECTS": analysis["immediate_effects"],
            "STRATEGIC_IMPLICATIONS": analysis["strategic_implications"],
            "QUICK_FACTS_LIST": "".join([f"<li>{fact}</li>" for fact in analysis["quick_facts"]]),
            "USER_TYPE_1_ICON": analysis["user_impact"]["user_type_1"]["icon"],
            "USER_TYPE_1_TITLE": analysis["user_impact"]["user_type_1"]["title"],
            "USER_TYPE_1_DESCRIPTION": analysis["user_impact"]["user_type_1"]["description"],
            "USER_TYPE_2_ICON": analysis["user_impact"]["user_type_2"]["icon"],
            "USER_TYPE_2_TITLE": analysis["user_impact"]["user_type_2"]["title"],
            "USER_TYPE_2_DESCRIPTION": analysis["user_impact"]["user_type_2"]["description"],
            "USER_TYPE_3_ICON": analysis["user_impact"]["user_type_3"]["icon"],
            "USER_TYPE_3_TITLE": analysis["user_impact"]["user_type_3"]["title"],
            "USER_TYPE_3_DESCRIPTION": analysis["user_impact"]["user_type_3"]["description"],
            "NEXT_STEPS_LIST": "".join(analysis["next_steps"]),
            "DRAW_DETAILS_LIST": "".join(analysis["draw_details"]),
            "SOURCE_LINKS_LIST": "".join(analysis["source_links"]),
            "TAGS_LIST": "".join(analysis["tags"]),
            "RELATED_NEWS_LIST": self.generate_related_news(),
            "ARTICLE_CONTENT": analysis["article_content"],
            "HOME_PATH": "../../../../../",
            "REPORTS_PATH": "../../../../../reports/",
            "TOOLS_PATH": "../../../../../tools/",
            "NEWS_PATH": "../../../../",
            "DAILY_PATH": "../../../",
            "DRAWS_PATH": "../../",
            "ABOUT_PATH": "../../../../../about/",
            "NEWSLETTER_PATH": "../../../../",
            "BREADCRUMB_TITLE": f"Express Entry {analysis['draw_type']} Draw",
            "CANONICAL_URL": f"https://immiwatch.ca/news/daily/draws/{analysis['date']}/{self.create_slug(analysis['title'])}/",
            "SHARE_TITLE": analysis["title"],
            "KEYWORDS_ARRAY": '"' + analysis["keywords"].replace(", ", '", "') + '"'
        }
        
        # Replace all variables in template
        content = self.template
        for var, value in template_vars.items():
            content = content.replace(f"{{{{{var}}}}}", str(value))
        
        return content
    
    def generate_related_news(self) -> str:
        """Generate related news links."""
        return """
        <a href="../2025-07-22/express-entry-health-draw-4000-itas-475-crs/" class="related-item">
            <h4>Historic Express Entry Health Draw: 4,000 ITAs Issued with 475 CRS Cutoff</h4>
            <div class="date">July 22, 2025 • Draw Analysis</div>
        </a>
        
        <a href="../2025-07-21/express-entry-pnp-draw-202-itas-788-crs/" class="related-item">
            <h4>Express Entry PNP-Only Draw Issues 202 ITAs with 788 CRS Cutoff</h4>
            <div class="date">July 21, 2025 • Draw Analysis</div>
        </a>
        
        <a href="../../../policy/2025-07-16/study-permit-renewal-standards/" class="related-item">
            <h4>Enhanced Processing Standards for Study Permit Renewals</h4>
            <div class="date">July 16, 2025 • Policy Update</div>
        </a>
        """
    
    def create_article_file(self, analysis: Dict) -> str:
        """Create the article file and return the URL."""
        
        # Create directory structure
        date_dir = self.draws_path / analysis["date"]
        slug = self.create_slug(analysis["title"])
        article_dir = date_dir / slug
        article_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate article content
        article_content = self.replace_template_variables(analysis)
        
        # Write article file
        article_file = article_dir / "index.html"
        with open(article_file, 'w', encoding='utf-8') as f:
            f.write(article_content)
        
        logger.info(f"Created article: {article_file}")
        
        # Return the URL
        return f"https://immiwatch.ca/news/daily/draws/{analysis['date']}/{slug}/"
    
    def update_draws_category_page(self, analysis: Dict, article_url: str):
        """Update the draws category page with the new article."""
        
        draws_index_file = self.draws_path / "index.html"
        
        if not draws_index_file.exists():
            logger.error("Draws category page not found")
            return
        
        # Read current content
        with open(draws_index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create new article card HTML
        new_article_card = f"""
                <!-- {analysis['draw_type']} Draw Article -->
                <article class="article-card">
                    <div class="article-meta">
                        <span class="article-date">📅 {self.format_date(analysis['date'])}</span>
                        <span class="article-badge">Express Entry</span>
                    </div>
                    <h2 class="article-title">
                        <a href="{analysis['date']}/{self.create_slug(analysis['title'])}/">{analysis['title']}</a>
                    </h2>
                    <p class="article-excerpt">
                        IRCC conducted an Express Entry draw targeting {analysis['draw_type']} candidates on {self.format_date(analysis['date'])}, issuing {analysis['itas']:,} ITAs with a minimum CRS score of {analysis['crs']}. This program-specific draw continues IRCC's strategy of targeted immigration.
                    </p>
                    <a href="{analysis['date']}/{self.create_slug(analysis['title'])}/" class="article-link">
                        Read Full Analysis →
                    </a>
                </article>

                <!-- Express Entry Health Draw Article -->
"""
        
        # Insert new article at the top
        content = content.replace("<!-- Express Entry Health Draw Article -->", new_article_card)
        
        # Write updated content
        with open(draws_index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Updated draws category page: {draws_index_file}")
    
    def update_daily_news_page(self, analysis: Dict, article_url: str):
        """Update the main daily news page with the new article."""
        
        if not self.daily_index_path.exists():
            logger.error("Daily news page not found")
            return
        
        # Read current content
        with open(self.daily_index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create impact class
        impact_class = 'impact-high' if analysis['impact_level'].lower() == 'high' else 'impact-important'
        
        # Create new news card in the correct format
        new_news_card = f"""                <!-- {analysis['title']} -->
                <article class="news-card">
                    <div class="news-card-header">
                        <span class="news-category-badge category-invitation-rounds">🎯 Invitation Rounds</span>
                        <h3><a href="draws/{analysis['date']}/{self.create_slug(analysis['title'])}/">{analysis['title']}</a></h3>
                    </div>
                    <div class="news-card-content">
                        <div class="news-meta">
                            <span>{self.format_date(analysis['date'])}</span>
                            <span>•</span>
                            <span><span class="impact-indicator {impact_class}"></span>{analysis['impact_level'].title()} Impact</span>
                        </div>
                        <p class="summary">
                            IRCC conducted an Express Entry draw targeting {analysis['draw_type']} candidates, issuing {analysis['itas']:,} ITAs with a minimum CRS score of {analysis['crs']}. This program-specific draw continues IRCC's strategy of targeted immigration selection.
                        </p>
                    </div>
                    <div class="news-card-footer">
                        <a href="draws/{analysis['date']}/{self.create_slug(analysis['title'])}/" class="read-more-btn">Read Full Analysis →</a>
                    </div>
                </article>
"""
        
        # Find the news-grid div and insert at the beginning
        news_grid_pattern = r'(<div class="news-grid">)\s*\n'
        
        if re.search(news_grid_pattern, content):
            # Insert the new card at the beginning of news-grid
            content = re.sub(news_grid_pattern, f'\\1\n{new_news_card}\n', content)
            
            # Now remove the oldest (4th) news card if it exists
            # Count existing news cards
            news_cards = re.findall(r'<article class="news-card">', content)
            if len(news_cards) > 3:
                # Find and remove the 4th news card
                card_count = 0
                lines = content.split('\n')
                new_lines = []
                removing = False
                
                for line in lines:
                    if '<article class="news-card">' in line:
                        card_count += 1
                        if card_count == 4:
                            removing = True
                    
                    if not removing:
                        new_lines.append(line)
                    
                    if removing and '</article>' in line:
                        removing = False
                        # Skip the empty line after the article
                        continue
                
                content = '\n'.join(new_lines)
        
        # Update the draws count in the category card
        # Find the draws category card and update its count
        draws_card_pattern = r'(<a href="draws/"[^>]*>.*?<span class="category-count">)(\d+)(\s*Articles</span>)'
        current_count_match = re.search(draws_card_pattern, content, re.DOTALL)
        if current_count_match:
            current_count = int(current_count_match.group(2))
            new_count = current_count + 1
            content = re.sub(draws_card_pattern, f'\\g<1>{new_count}\\g<3>', content, flags=re.DOTALL)
        
        # Write updated content
        with open(self.daily_index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Updated daily news page: {self.daily_index_path}")
    
    def send_slack_notification(self, analysis: Dict, article_url: str, success: bool = True, error_msg: str = None):
        """Send Slack notification about the article creation."""
        
        slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        if not slack_webhook_url:
            logger.warning("SLACK_WEBHOOK_URL not set, skipping Slack notification")
            return
        
        if success:
            message = {
                "text": "🎯 New Draw Article Published!",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "🎯 New Draw Article Published!"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Draw Type:* {analysis['draw_type']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*ITAs Issued:* {analysis['itas']:,}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*CRS Cutoff:* {analysis['crs']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Impact Level:* {analysis['impact_level']}"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Article URL:* {article_url}"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Title:* {analysis['title']}"
                        }
                    }
                ]
            }
        else:
            message = {
                "text": "❌ Draw Article Creation Failed",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "❌ Draw Article Creation Failed"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Error:* {error_msg}"
                        }
                    }
                ]
            }
        
        try:
            response = requests.post(slack_webhook_url, json=message)
            response.raise_for_status()
            logger.info("Slack notification sent successfully")
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {e}")
    
    def process_draw_data(self, data: Dict) -> Dict:
        """Main processing function for draw data."""
        
        try:
            logger.info("Processing draw data...")
            
            # Analyze the data
            analysis = self.analyze_draw_data(data)
            logger.info(f"Analyzed draw: {analysis['title']}")
            
            # Create the article
            article_url = self.create_article_file(analysis)
            logger.info(f"Created article: {article_url}")
            
            # Update category page
            self.update_draws_category_page(analysis, article_url)
            logger.info("Updated draws category page")
            
            # Update daily news page
            self.update_daily_news_page(analysis, article_url)
            logger.info("Updated daily news page")
            
            # Send success notification
            self.send_slack_notification(analysis, article_url, success=True)
            
            return {
                "success": True,
                "article_url": article_url,
                "title": analysis["title"],
                "message": "Draw article created successfully"
            }
            
        except Exception as e:
            error_msg = f"Failed to process draw data: {str(e)}"
            logger.error(error_msg)
            
            # Send error notification
            self.send_slack_notification({}, "", success=False, error_msg=error_msg)
            
            return {
                "success": False,
                "error": error_msg
            }

def main():
    """Main function to handle GitHub Actions workflow."""
    
    # Check if running in GitHub Actions
    github_event_path = os.getenv('GITHUB_EVENT_PATH')
    
    if github_event_path and os.path.exists(github_event_path):
        # Running in GitHub Actions
        with open(github_event_path, 'r') as f:
            event_data = json.load(f)
        
        # Extract data from repository dispatch
        client_payload = event_data.get('client_payload', {})
        
        # For repository dispatch, the event type is in the action, not in client_payload
        # Skip the event type check and just process the data
        logger.info(f"Processing repository dispatch with category: {client_payload.get('category', 'unknown')}")
        
        # The data is directly in client_payload
        data = client_payload
        
    else:
        # Running locally for testing
        logger.info("Running in local mode")
        
        # Example test data
        data = {
            "headline": "Express Entry CEC Draw: 3,000 ITAs Issued at CRS 518",
            "summary": "IRCC conducted a CEC-specific draw on July 8, 2025",
            "invitation": 3000,
            "cutoff": 518,
            "draw_type": "CEC",
            "date": "2025-07-08",
            "source": "IRCC Official"
        }
    
    # Initialize automation system
    automation = DrawAutomationSystem()
    
    # Process the data
    result = automation.process_draw_data(data)
    
    # Output result for GitHub Actions
    if github_event_path:
        if result['success']:
            print(f"article_url={result['article_url']}")
            print(f"title={result['title']}")
        else:
            print(f"error={result.get('error', 'Unknown error')}")
    
    return result

if __name__ == "__main__":
    main() 