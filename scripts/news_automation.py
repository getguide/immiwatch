#!/usr/bin/env python3
"""
ImmiWatch News Automation System
The Future of Immigration News Publishing

This system automates the entire news publishing workflow:
1. Process JSON data from Airtable
2. Generate professional news articles
3. Update all relevant pages (counts, latest news, etc.)
4. Send Slack notifications
5. Handle errors with draft creation
"""

import json
import os
import re
import sys
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib
import urllib.parse

class NewsAutomationSystem:
    """The most advanced news automation system on Earth"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.news_path = self.base_path / "news"
        self.assets_path = self.base_path / "assets"
        self.slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
        
                            # Category configurations
                    self.categories = {
                        'policy-announcements': {'icon': '📢', 'color': '#1e40af', 'name': 'Policy Announcements'},
                        'program-delivery': {'icon': '🏛️', 'color': '#ea580c', 'name': 'Program Delivery Updates'},
                        'invitation-rounds': {'icon': '🎯', 'color': '#059669', 'name': 'Invitation Rounds'},
                        'atip-insights': {'icon': '📊', 'color': '#0d9488', 'name': 'ATIP Insights'},
                        'legal-decisions': {'icon': '⚖️', 'color': '#7c3aed', 'name': 'Legal Decisions'},
                        'system-notices': {'icon': '🔧', 'color': '#6b7280', 'name': 'System Notices'},
                        'form-changes': {'icon': '📄', 'color': '#3b82f6', 'name': 'Form Changes'},
                        'deadline-alerts': {'icon': '⏰', 'color': '#dc2626', 'name': 'Deadline Alerts'},
                        'statistical-reports': {'icon': '📈', 'color': '#0d9488', 'name': 'Statistical Reports'},
                        'scam-alerts': {'icon': '🚨', 'color': '#dc2626', 'name': 'Scam Alerts'},
                        'other': {'icon': '📋', 'color': '#6b7280', 'name': 'Other Updates'}
                    }
        
        # Impact level configurations
        self.impact_levels = {
            'critical': {'color': '#dc2626', 'label': 'Critical Impact'},
            'high': {'color': '#dc2626', 'label': 'High Impact'},
            'moderate': {'color': '#ea580c', 'label': 'Important Impact'},
            'low': {'color': '#059669', 'label': 'Medium Impact'},
            'informational': {'color': '#6b7280', 'label': 'Low Impact'}
        }

    def process_airtable_data(self, json_data: Dict) -> Dict:
        """Process and validate Airtable JSON data"""
        try:
            # Validate required fields
            required_fields = ['headline', 'summary', 'date_of_update', 'category', 'impact']
            missing_fields = [field for field in required_fields if field not in json_data]
            
            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")
            
            # Process and enhance data
            processed_data = {
                'headline': json_data['headline'].strip(),
                'summary': json_data['summary'].strip(),
                'date_of_update': json_data['date_of_update'],
                'category': json_data['category'].lower(),
                'impact': json_data['impact'].lower(),
                'urgency_level': json_data.get('urgency_level', 'informational'),
                'program_affected': json_data.get('program_affected', []),
                'source': json_data.get('source', 'IRCC'),
                'source_url': json_data.get('source_url', ''),
                'week_of_year': json_data.get('week_of_year'),
                'year': json_data.get('year', datetime.now().year),
                'cutoff': json_data.get('cutoff'),
                'invitation': json_data.get('invitation')
            }
            
            # Generate slug from headline
            processed_data['slug'] = self.generate_slug(processed_data['headline'])
            
            # Validate category
            if processed_data['category'] not in self.categories:
                raise ValueError(f"Invalid category: {processed_data['category']}")
            
            return processed_data
            
        except Exception as e:
            self.handle_error(f"Data processing error: {str(e)}", json_data)
            return None

    def generate_slug(self, headline: str) -> str:
        """Generate URL-friendly slug from headline"""
        # Convert to lowercase and replace spaces with hyphens
        slug = re.sub(r'[^\w\s-]', '', headline.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')

    def generate_article_content(self, data: Dict) -> str:
        """Generate complete article HTML content"""
        
        # Parse date
        date_obj = datetime.strptime(data['date_of_update'], '%Y-%m-%d')
        formatted_date = date_obj.strftime('%B %d, %Y')
        
        # Generate meta description
        meta_description = self.generate_meta_description(data)
        
        # Generate keywords
        keywords = self.generate_keywords(data)
        
        # Generate detailed analysis
        detailed_analysis = self.generate_detailed_analysis(data)
        
        # Generate image path
        image_path = self.generate_image_path(data)
        
        # Category info
        category_info = self.categories[data['category']]
        impact_info = self.impact_levels[data['impact']]
        
        # Generate HTML template
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2573Q8G1WD"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-2573Q8G1WD');
</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- DYNAMIC META TAGS -->
    <title>{data['headline']} | ImmiWatch Immigration News</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{keywords}">
    
    <!-- ARTICLE META -->
    <meta name="author" content="ImmiWatch Editorial Team">
    <meta name="publish-date" content="{data['date_of_update']}">
    <meta name="article-category" content="{category_info['name']}">
    <meta name="article-impact" content="{impact_info['label']}">
    <meta name="article-source" content="{data['source']}">
    
    <!-- OPEN GRAPH -->
    <meta property="og:title" content="{data['headline']}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://immiwatch.ca/news/daily/{data['category']}/{data['date_of_update']}/{data['slug']}/">
    <meta property="og:image" content="https://immiwatch.ca{image_path}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:site_name" content="ImmiWatch">
    <meta property="article:published_time" content="{data['date_of_update']}T15:00:00Z">
    <meta property="article:author" content="ImmiWatch Editorial Team">
    <meta property="article:section" content="{category_info['name']}">
    
    <!-- TWITTER CARDS -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{data['headline']}">
    <meta name="twitter:description" content="{meta_description}">
    <meta name="twitter:image" content="https://immiwatch.ca{image_path}">
    
    <!-- STRUCTURED DATA -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": "{data['headline']}",
        "description": "{meta_description}",
        "datePublished": "{data['date_of_update']}T15:00:00Z",
        "dateModified": "{data['date_of_update']}T15:00:00Z",
        "author": {{
            "@type": "Organization",
            "name": "ImmiWatch Editorial Team"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "ImmiWatch",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://immiwatch.ca/favicon.svg"
            }}
        }},
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "https://immiwatch.ca/news/daily/{data['category']}/{data['date_of_update']}/{data['slug']}/"
        }},
        "articleSection": "{category_info['name']}",
        "keywords": {json.dumps(keywords.split(', '))}
    }}
    </script>
    
    <!-- FAVICON -->
    <link rel="icon" type="image/svg+xml" href="../../../../../favicon.svg?v=3&t=1737962580">
    <link rel="apple-touch-icon" href="../../../../../favicon.svg?v=3&t=1737962580">
    
    <!-- STYLESHEETS -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../../../../assets/css/shared-styles.css">
    
    <style>
        /* NEWS ARTICLE SPECIFIC STYLES */
        .news-header {{
            background: linear-gradient(135deg, {category_info['color']} 0%, {self.darken_color(category_info['color'])} 100%);
            color: white;
            padding: 2rem 0;
        }}
        
        .news-category {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.875rem;
            font-weight: 500;
            margin-bottom: 1rem;
        }}
        
        .news-title {{
            font-size: 2.5rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 1rem;
        }}
        
        .news-meta {{
            display: flex;
            align-items: center;
            gap: 2rem;
            font-size: 0.875rem;
            opacity: 0.8;
            flex-wrap: wrap;
        }}
        
        .news-meta-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .impact-level {{
            font-weight: 600;
            color: {impact_info['color']};
        }}
        
        .news-content {{
            max-width: 800px;
            margin: 0 auto;
            padding: 3rem 0;
        }}
        
        .news-article {{
            background: white;
            border-radius: var(--border-radius-xl);
            padding: 2rem;
            box-shadow: var(--shadow-lg);
        }}
        
        .news-summary {{
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
            border-left: 4px solid var(--green-500);
            padding: 1.5rem;
            margin: 2rem 0;
            border-radius: 0.5rem;
        }}
        
        .impact-assessment {{
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
            border-left: 4px solid var(--yellow-500);
            padding: 1.5rem;
            margin: 2rem 0;
            border-radius: 0.5rem;
        }}
        
        .news-content h3 {{
            color: var(--gray-800);
            font-size: 1.75rem;
            font-weight: 600;
            margin: 2rem 0 1rem;
        }}
        
        .news-content h4 {{
            color: var(--gray-700);
            font-size: 1.5rem;
            font-weight: 600;
            margin: 1.5rem 0 1rem;
        }}
        
        .news-content p {{
            color: var(--gray-600);
            line-height: 1.7;
            margin-bottom: 1.5rem;
            font-size: 1.1rem;
        }}
        
        .news-content ul, .news-content ol {{
            color: var(--gray-600);
            line-height: 1.7;
            margin-bottom: 1.5rem;
            padding-left: 1.5rem;
        }}
        
        .news-content li {{
            margin-bottom: 0.5rem;
        }}
        
        .draw-details {{
            background: var(--gray-100);
            padding: 1.5rem;
            border-radius: var(--border-radius-md);
            margin: 1.5rem 0;
        }}
        
        .draw-details h5 {{
            margin: 0 0 1rem 0;
            color: var(--gray-800);
            font-size: 1.1rem;
            font-weight: 600;
        }}
        
        .draw-details ul {{
            margin: 0;
            padding-left: 1.2rem;
        }}
        
        .draw-details li {{
            margin-bottom: 0.5rem;
            color: var(--gray-600);
        }}
        
        .source-links {{
            background: var(--blue-50);
            border: 1px solid var(--blue-200);
            padding: 1.5rem;
            border-radius: var(--border-radius-md);
            margin: 2rem 0;
        }}
        
        .source-links h4 {{
            margin: 0 0 1rem 0;
            color: var(--blue-800);
        }}
        
        .source-links a {{
            color: var(--blue-600);
            text-decoration: none;
            font-weight: 500;
        }}
        
        .source-links a:hover {{
            text-decoration: underline;
        }}
        
        .related-news {{
            background: var(--gray-50);
            padding: 2rem;
            border-radius: var(--border-radius-lg);
            margin: 3rem 0;
        }}
        
        .related-news h3 {{
            margin: 0 0 1.5rem 0;
            color: var(--gray-800);
        }}
        
        .related-news a {{
            color: var(--primary-600);
            text-decoration: none;
            font-weight: 500;
        }}
        
        .related-news a:hover {{
            text-decoration: underline;
        }}
        
        @media (max-width: 768px) {{
            .news-title {{
                font-size: 2rem;
            }}
            
            .news-meta {{
                flex-direction: column;
                align-items: flex-start;
                gap: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar" id="navbar">
        <div class="nav-content">
            <div class="logo">
                <div class="logo-icon"></div>
                <div class="logo-text">
                    <span class="logo-main">ImmiWatch</span>
                    <span class="logo-subtitle">By Lexpoint.io</span>
                </div>
            </div>
            
            <ul class="nav-menu">
                <li><a href="../../../../../" class="nav-link">Home</a></li>
                <li><a href="../../../../../reports/" class="nav-link">Reports</a></li>
                <li><a href="../../../../../tools/" class="nav-link">Navigators</a></li>
                <li><a href="../../../../" class="nav-link active">News</a></li>
                <li><a href="../../../../../about/" class="nav-link">About</a></li>
                <li><a href="https://intake.immigratic.com/t/eELGpk1aGhus" target="_blank" class="nav-link nav-cta">Get Started</a></li>
            </ul>
            
            <button class="mobile-menu-btn">
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
            </button>
        </div>
    </nav>

    <!-- Breadcrumb -->
    <div class="breadcrumb">
        <div class="container">
            <div class="breadcrumb-content">
                <a href="../../../../../" class="breadcrumb-link">Home</a>
                <span>›</span>
                <a href="../../../../" class="breadcrumb-link">News</a>
                <span>›</span>
                <a href="../../" class="breadcrumb-link">Daily News</a>
                <span>›</span>
                <a href="../" class="breadcrumb-link">{category_info['name']}</a>
                <span>›</span>
                <span>{data['headline']}</span>
            </div>
        </div>
    </div>

    <!-- News Header -->
    <section class="news-header">
        <div class="container">
            <div class="news-category">{category_info['icon']} {category_info['name']}</div>
            <h1 class="news-title">{data['headline']}</h1>
            <div class="news-meta">
                <div class="news-meta-item">
                    <span>📅</span>
                    <span>{formatted_date}</span>
                </div>
                <div class="news-meta-item">
                    <span>🎯</span>
                    <span class="impact-level">{impact_info['label']}</span>
                </div>
                <div class="news-meta-item">
                    <span>📰</span>
                    <span>{data['source']}</span>
                </div>
                <div class="news-meta-item">
                    <span>⏱️</span>
                    <span>5 min read</span>
                </div>
            </div>
        </div>
    </section>

    <!-- News Content -->
    <section class="news-content">
        <div class="container">
            <article class="news-article">
                <div class="news-summary">
                    <h3>📋 Executive Summary</h3>
                    <p>{data['summary']}</p>
                </div>

                <div class="impact-assessment">
                    <h3>🎯 Impact Assessment</h3>
                    <p>This development has <strong>{impact_info['label'].lower()}</strong> implications for Canadian immigration programs and applicants. The changes will affect {', '.join(data['program_affected']) if data['program_affected'] else 'multiple immigration programs'}.</p>
                </div>

                {self.generate_draw_details(data) if data['category'] == 'draws' and data.get('cutoff') and data.get('invitation') else ''}

                <h3>📊 Detailed Analysis</h3>
                {detailed_analysis}

                {self.generate_source_section(data) if data.get('source_url') else ''}

                <div class="related-news">
                    <h3>📰 Related News</h3>
                    <p>Stay informed with our comprehensive coverage of Canadian immigration developments:</p>
                    <ul>
                        <li><a href="../../">Browse all {category_info['name']}</a></li>
                        <li><a href="../../../../">View latest immigration news</a></li>
                        <li><a href="../../../../../news/digest/">Read weekly newsletters</a></li>
                    </ul>
                </div>

                <div style="text-align: center; margin-top: 3rem;">
                    <a href="https://intake.immigratic.com/t/eELGpk1aGhus" target="_blank" class="btn btn-primary">📧 Subscribe to Weekly Newsletter</a>
                    <p style="margin-top: 1rem; color: var(--gray-600);">Get all immigration news delivered weekly with comprehensive analysis</p>
                </div>
            </article>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-logo">ImmiWatch Data Studio</div>
                <p class="footer-description">
                    Professional Canada immigration analytics and insights. A premium product by Lexpoint.io, delivering data-driven immigration intelligence since 2025.
                </p>
                
                <div class="footer-links">
                    <a href="../../../../../reports/" class="footer-link">Reports</a>
                    <a href="../../../../../tools/" class="footer-link">Navigators</a>
                    <a href="https://intake.immigratic.com/t/eELGpk1aGhus" target="_blank" class="footer-link">Newsletter</a>
                    <a href="#" class="footer-link">Immigration News</a>
                    <a href="../../../../../about/" class="footer-link">About</a>
                    <a href="mailto:hi@lexpoint.io" class="footer-link">Contact</a>
                </div>
                
                <div class="footer-bottom">
                    <p>&copy; 2025 ImmiWatch Data Studio - Part of Lexpoint.io</p>
                    <p style="margin-top: 0.5rem; font-size: 0.875rem;">
                        Professional Immigration Analytics | 
                        <a href="mailto:hi@lexpoint.io" style="color: var(--primary-400);">hi@lexpoint.io</a>
                    </p>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Navbar scroll effect
        window.addEventListener('scroll', function() {{
            const navbar = document.getElementById('navbar');
            if (window.scrollY > 50) {{
                navbar.classList.add('scrolled');
            }} else {{
                navbar.classList.remove('scrolled');
            }}
        }});

        // Mobile menu functionality
        document.addEventListener('DOMContentLoaded', function() {{
            const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
            const navMenu = document.querySelector('.nav-menu');
            const body = document.body;
            
            if (mobileMenuBtn && navMenu) {{
                mobileMenuBtn.addEventListener('click', function() {{
                    navMenu.classList.toggle('active');
                    mobileMenuBtn.classList.toggle('active');
                    body.classList.toggle('menu-open');
                }});
            }}
        }});
    </script>
</body>
</html>"""
        
        return html_content

    def generate_meta_description(self, data: Dict) -> str:
        """Generate SEO-optimized meta description"""
        base_desc = data['summary'][:120]
        if len(data['summary']) > 120:
            base_desc += "..."
        return base_desc

    def generate_keywords(self, data: Dict) -> str:
        """Generate SEO keywords"""
        keywords = []
        
        # Add category-specific keywords
        if data['category'] == 'draws':
            keywords.extend(['Express Entry', 'CRS', 'ITAs', 'immigration draw'])
        elif data['category'] == 'policy':
            keywords.extend(['immigration policy', 'IRCC', 'government announcement'])
        elif data['category'] == 'legal':
            keywords.extend(['immigration law', 'legal decision', 'federal court'])
        
        # Add program-specific keywords
        if data.get('program_affected'):
            keywords.extend(data['program_affected'])
        
        # Add common keywords
        keywords.extend(['Canada immigration', 'immigration news', 'ImmiWatch'])
        
        return ', '.join(keywords)

    def generate_detailed_analysis(self, data: Dict) -> str:
        """Generate detailed analysis content"""
        analysis = f"""
                <p>{data['summary']}</p>
                
                <h4>Strategic Implications</h4>
                <p>This development represents a significant shift in Canada's immigration strategy, particularly affecting {', '.join(data['program_affected']) if data['program_affected'] else 'multiple immigration programs'}. The {data['impact']} impact level indicates that this change will have substantial implications for both applicants and immigration practitioners.</p>
                
                <h4>Key Considerations</h4>
                <ul>
                    <li><strong>Timing:</strong> This update was announced on {data['date_of_update']}, providing immediate guidance for affected parties.</li>
                    <li><strong>Scope:</strong> The changes impact {', '.join(data['program_affected']) if data['program_affected'] else 'various immigration programs'}.</li>
                    <li><strong>Source:</strong> Official information from {data['source']} ensures reliability and accuracy.</li>
                </ul>
                
                <h4>Professional Recommendations</h4>
                <p>Immigration practitioners should review their current client portfolios and assess how these changes may affect ongoing applications. Applicants should consult with qualified professionals to understand the specific implications for their individual circumstances.</p>
        """
        return analysis

    def generate_draw_details(self, data: Dict) -> str:
        """Generate draw-specific details for invitation rounds"""
        if data['category'] == 'draws' and data.get('cutoff') and data.get('invitation'):
            return f"""
                <div class="draw-details">
                    <h5>Draw Details:</h5>
                    <ul>
                        <li><strong>ITAs Issued:</strong> {data['invitation']:,}</li>
                        <li><strong>CRS Cutoff:</strong> {data['cutoff']}</li>
                        <li><strong>Draw Date:</strong> {data['date_of_update']}</li>
                        <li><strong>Program:</strong> {', '.join(data['program_affected']) if data['program_affected'] else 'Express Entry'}</li>
                    </ul>
                </div>
            """
        return ""

    def generate_source_section(self, data: Dict) -> str:
        """Generate source links section"""
        if data.get('source_url'):
            return f"""
                <div class="source-links">
                    <h4>📚 Official Sources</h4>
                    <p>For more information, please refer to the official announcement:</p>
                    <ul>
                        <li><a href="{data['source_url']}" target="_blank" rel="noopener noreferrer">Official {data['source']} Announcement</a></li>
                    </ul>
                </div>
            """
        return ""

    def generate_image_path(self, data: Dict) -> str:
        """Generate image path for the article"""
        category = data['category']
        slug = data['slug']
        date = data['date_of_update']
        return f"/assets/images/{category}-{slug}.svg"

    def darken_color(self, hex_color: str) -> str:
        """Darken a hex color for gradient"""
        # Simple darkening - in production, use proper color manipulation
        return hex_color

    def create_article_directory(self, data: Dict) -> Path:
        """Create article directory structure"""
        article_path = self.news_path / "daily" / data['category'] / data['date_of_update'] / data['slug']
        article_path.mkdir(parents=True, exist_ok=True)
        return article_path

    def write_article_file(self, article_path: Path, content: str) -> bool:
        """Write article HTML file"""
        try:
            with open(article_path / "index.html", "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing article file: {e}")
            return False

    def update_page_counts(self, data: Dict) -> bool:
        """Update article counts on relevant pages"""
        try:
            # Update daily news index page
            self.update_daily_news_index(data)
            
            # Update main news page
            self.update_main_news_page(data)
            
            # Update category index page
            self.update_category_index(data)
            
            return True
        except Exception as e:
            print(f"Error updating page counts: {e}")
            return False

    def update_daily_news_index(self, data: Dict):
        """Update the daily news index page with new article"""
        index_path = self.news_path / "daily" / "index.html"
        if not index_path.exists():
            return
        
        # Read current content
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Update category count
        category_name = self.categories[data['category']]['name']
        count_pattern = rf'<span class="category-count">(\d+) Articles</span>'
        match = re.search(count_pattern, content)
        if match:
            current_count = int(match.group(1))
            new_count = current_count + 1
            content = re.sub(count_pattern, f'<span class="category-count">{new_count} Articles</span>', content)
        
        # Add to latest news section
        latest_news_pattern = r'(<div class="news-grid">)'
        new_article_html = self.generate_latest_news_html(data)
        content = re.sub(latest_news_pattern, r'\1\n' + new_article_html, content)
        
        # Write updated content
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)

    def generate_latest_news_html(self, data: Dict) -> str:
        """Generate HTML for latest news section"""
        category_info = self.categories[data['category']]
        impact_info = self.impact_levels[data['impact']]
        
        return f"""
                <!-- {data['headline']} -->
                <article class="news-card">
                    <div class="news-card-header">
                        <span class="news-category-badge category-{data['category']}">{category_info['icon']} {category_info['name']}</span>
                        <h3><a href="{data['category']}/{data['date_of_update']}/{data['slug']}/">{data['headline']}</a></h3>
                    </div>
                    <div class="news-card-content">
                        <div class="news-meta">
                            <span>{data['date_of_update']}</span>
                            <span>•</span>
                            <span><span class="impact-indicator impact-{data['impact']}"></span>{impact_info['label']}</span>
                        </div>
                        <p class="summary">
                            {data['summary']}
                        </p>
                    </div>
                    <div class="news-card-footer">
                        <a href="{data['category']}/{data['date_of_update']}/{data['slug']}/" class="read-more-btn">Read Full Analysis →</a>
                    </div>
                </article>"""

    def update_main_news_page(self, data: Dict):
        """Update the main news page with new article"""
        index_path = self.news_path / "index.html"
        if not index_path.exists():
            return
        
        # Read current content
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Add to recent news section
        recent_news_pattern = r'(<div class="recent-news">\s*<h3>🔥 Recent News</h3>)'
        new_article_html = self.generate_recent_news_html(data)
        content = re.sub(recent_news_pattern, r'\1\n' + new_article_html, content)
        
        # Write updated content
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)

    def generate_recent_news_html(self, data: Dict) -> str:
        """Generate HTML for recent news section"""
        category_info = self.categories[data['category']]
        
        return f"""
                    <div class="news-item">
                        <div class="news-item-title">
                            <a href="daily/{data['category']}/{data['date_of_update']}/{data['slug']}/">{data['headline']}</a>
                        </div>
                        <div class="news-item-meta">
                            <span class="news-category-badge">{category_info['name']}</span>
                            <span>{data['date_of_update']}</span>
                        </div>
                    </div>"""

    def update_category_index(self, data: Dict):
        """Update the category index page"""
        category_index_path = self.news_path / "daily" / data['category'] / "index.html"
        if not category_index_path.exists():
            return
        
        # Read current content
        with open(category_index_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Add new article to the list
        article_list_pattern = r'(<div class="news-list">)'
        new_article_html = self.generate_category_article_html(data)
        content = re.sub(article_list_pattern, r'\1\n' + new_article_html, content)
        
        # Write updated content
        with open(category_index_path, "w", encoding="utf-8") as f:
            f.write(content)

    def generate_category_article_html(self, data: Dict) -> str:
        """Generate HTML for category article list"""
        impact_info = self.impact_levels[data['impact']]
        
        return f"""
                <article class="news-item">
                    <div class="news-meta">
                        <span>📅 {data['date_of_update']}</span>
                        <span class="impact-badge impact-{data['impact']}">{impact_info['label']}</span>
                        <span>🇨🇦 {data['source']}</span>
                    </div>
                    <h4><a href="{data['date_of_update']}/{data['slug']}/" style="color: var(--gray-900); text-decoration: none;">{data['headline']}</a></h4>
                    <p>{data['summary']}</p>
                    <a href="{data['date_of_update']}/{data['slug']}/" style="color: var(--primary-600); text-decoration: none; font-weight: 600; display: inline-block; margin-top: 1rem;">📖 Read Full Analysis →</a>
                </article>"""

    def send_slack_notification(self, data: Dict, article_url: str, success: bool = True):
        """Send Slack notification about article publication"""
        if not self.slack_webhook:
            print("No Slack webhook configured")
            return
        
        if success:
            message = {
                "text": "🎉 New Article Published!",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "🎉 New Article Published!"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{data['headline']}*\n\n{data['summary']}"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Category:*\n{self.categories[data['category']]['name']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Impact:*\n{self.impact_levels[data['impact']]['label']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Date:*\n{data['date_of_update']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Source:*\n{data['source']}"
                            }
                        ]
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "View Article"
                                },
                                "url": article_url,
                                "style": "primary"
                            }
                        ]
                    }
                ]
            }
        else:
            message = {
                "text": "⚠️ Article Draft Created",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "⚠️ Article Draft Created"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{data['headline']}*\n\nArticle was created as draft due to missing or invalid data. Please review and publish manually."
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Draft Location:*\n`/news/daily/drafts/{data['date_of_update']}/{data['slug']}/`"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Issue:*\nMissing required fields or validation error"
                            }
                        ]
                    }
                ]
            }
        
        try:
            response = requests.post(self.slack_webhook, json=message)
            response.raise_for_status()
            print("Slack notification sent successfully")
        except Exception as e:
            print(f"Error sending Slack notification: {e}")

    def handle_error(self, error_message: str, data: Dict):
        """Handle errors by creating draft and sending notification"""
        print(f"Error: {error_message}")
        
        # Create draft directory
        draft_path = self.news_path / "daily" / "drafts" / data.get('date_of_update', 'unknown') / data.get('slug', 'unknown')
        draft_path.mkdir(parents=True, exist_ok=True)
        
        # Create error report
        error_report = f"""
# Article Draft - Error Report

## Error Details
{error_message}

## Original Data
{json.dumps(data, indent=2)}

## Required Actions
1. Review the error message above
2. Fix the data in Airtable
3. Re-run the automation
4. Delete this draft once published

## Draft Location
{draft_path}
        """
        
        with open(draft_path / "ERROR_REPORT.md", "w", encoding="utf-8") as f:
            f.write(error_report)
        
        # Send Slack notification
        self.send_slack_notification(data, str(draft_path), success=False)

    def publish_article(self, json_data: Dict) -> bool:
        """Main method to publish an article from Airtable data"""
        try:
            # Process and validate data
            data = self.process_airtable_data(json_data)
            if not data:
                return False
            
            # Generate article content
            content = self.generate_article_content(data)
            
            # Create directory structure
            article_path = self.create_article_directory(data)
            
            # Write article file
            if not self.write_article_file(article_path, content):
                return False
            
            # Update page counts and links
            if not self.update_page_counts(data):
                return False
            
            # Generate article URL
            article_url = f"https://immiwatch.ca/news/daily/{data['category']}/{data['date_of_update']}/{data['slug']}/"
            
            # Send success notification
            self.send_slack_notification(data, article_url, success=True)
            
            print(f"✅ Article published successfully: {article_url}")
            return True
            
        except Exception as e:
            self.handle_error(f"Publication error: {str(e)}", json_data)
            return False

def main():
    """Main function to run the automation system"""
    try:
        # Check if running in GitHub Actions (with repository dispatch)
        if os.getenv('GITHUB_EVENT_PATH'):
            # Read from GitHub event
            with open(os.getenv('GITHUB_EVENT_PATH'), 'r') as f:
                event_data = json.load(f)
            
            # Extract data from GitHub event
            if event_data.get('event_type') == 'news_article':
                json_data = event_data.get('client_payload', {})
                print(f"📥 Received news data from GitHub: {json.dumps(json_data, indent=2)}")
            else:
                print(f"❌ Unexpected event type: {event_data.get('event_type')}")
                sys.exit(1)
        else:
            # Local testing mode
            if len(sys.argv) != 2:
                print("Usage: python news_automation.py <json_file>")
                sys.exit(1)
            
            json_file = sys.argv[1]
            
            # Read JSON data
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        
        # Initialize and run automation system
        automation = NewsAutomationSystem()
        success = automation.publish_article(json_data)
        
        if success:
            print("🎉 Article published successfully!")
            
            # Output for GitHub Actions
            if os.getenv('GITHUB_OUTPUT'):
                with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
                    f.write(f"success=true\n")
                    f.write(f"article_url=https://immiwatch.ca/news/daily/{json_data.get('category', '')}/{json_data.get('date_of_update', '')}/{automation.generate_slug(json_data.get('headline', ''))}/\n")
                    f.write(f"slug={automation.generate_slug(json_data.get('headline', ''))}\n")
            
            sys.exit(0)
        else:
            print("❌ Article publication failed. Check draft folder for details.")
            
            # Output for GitHub Actions
            if os.getenv('GITHUB_OUTPUT'):
                with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
                    f.write(f"success=false\n")
                    f.write(f"error=Article publication failed\n")
            
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Output for GitHub Actions
        if os.getenv('GITHUB_OUTPUT'):
            with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
                f.write(f"success=false\n")
                f.write(f"error={str(e)}\n")
        
        sys.exit(1)

if __name__ == "__main__":
    main() 