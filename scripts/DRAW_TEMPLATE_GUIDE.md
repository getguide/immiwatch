# 🎯 Draw News Template Guide

## Overview
This is the **GOLD STANDARD** template for all draw-based news articles. It includes all the enhanced visual features, statistics cards, user impact sections, and next steps that make draw articles engaging and informative.

## Template File
- **File:** `scripts/draw_news_template.html`
- **Based on:** Enhanced CEC draw article (July 8, 2025)
- **Features:** All visual enhancements, animations, and user experience improvements

## Template Variables

### 🔧 Core Article Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `{{TITLE}}` | Article headline | "Express Entry CEC Draw: 3,000 ITAs Issued at CRS 518" |
| `{{DESCRIPTION}}` | Meta description | "Express Entry Canadian Experience Class draw issued 3,000 ITAs..." |
| `{{KEYWORDS}}` | Meta keywords | "Express Entry, CEC draw, 3000 ITAs, CRS 518, IRCC..." |
| `{{PUBLISH_DATE}}` | ISO date | "2025-07-08" |
| `{{PUBLISH_DATE_FORMATTED}}` | Human readable date | "July 8, 2025" |
| `{{PUBLISH_TIME}}` | ISO datetime | "2025-07-08T15:00:00Z" |
| `{{IMPACT_LEVEL}}` | Impact classification | "High" |
| `{{IMPACT_CLASS}}` | CSS class for impact | "high" or "critical" |
| `{{IMPACT_TEXT}}` | Display text | "High Impact" |
| `{{SOURCE}}` | Source attribution | "IRCC Official" |

### 🎨 Visual & Styling Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `{{HEADER_GRADIENT}}` | Header background gradient | "#059669 0%, #047857 100%" |
| `{{FAVICON_PATH}}` | Path to favicon | "../../../../../favicon.svg" |
| `{{CSS_PATH}}` | Path to CSS file | "../../../../../assets/css/shared-styles.css" |
| `{{OG_IMAGE}}` | Open Graph image URL | "https://immiwatch.ca/assets/images/express-entry-cec-draw.svg" |

### 📊 Draw Statistics Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `{{ITAS_ISSUED}}` | Number of ITAs | "3,000" |
| `{{CRS_CUTOFF}}` | CRS cutoff score | "518" |
| `{{DRAW_TYPE_ICON}}` | Icon for draw type | "🇨🇦" (CEC), "🌐" (General), "🏥" (Health) |
| `{{DRAW_TYPE_NAME}}` | Name of draw type | "CEC", "General", "Health" |
| `{{DRAW_DATE_FORMATTED}}` | Formatted draw date | "July 8" |
| `{{DRAW_SUMMARY}}` | Brief draw summary | "Canadian Experience Class: Targeted draw for candidates..." |

### 📝 Content Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `{{EXECUTIVE_SUMMARY}}` | Executive summary paragraph | "On July 8, 2025, IRCC conducted an Express Entry draw..." |
| `{{IMMEDIATE_EFFECTS}}` | Immediate effects description | "3,000 CEC candidates invited to apply for permanent residence..." |
| `{{STRATEGIC_IMPLICATIONS}}` | Strategic implications | "Program-specific draw strategy continues..." |

### 🎯 User Impact Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `{{USER_TYPE_1_ICON}}` | Icon for first user type | "🇨🇦" |
| `{{USER_TYPE_1_TITLE}}` | Title for first user type | "CEC Candidates" |
| `{{USER_TYPE_1_DESCRIPTION}}` | Description for first user type | "If you have Canadian work experience..." |
| `{{USER_TYPE_2_ICON}}` | Icon for second user type | "📋" |
| `{{USER_TYPE_2_TITLE}}` | Title for second user type | "Immigration Practitioners" |
| `{{USER_TYPE_2_DESCRIPTION}}` | Description for second user type | "Advise CEC clients to maintain..." |
| `{{USER_TYPE_3_ICON}}` | Icon for third user type | "🏢" |
| `{{USER_TYPE_3_TITLE}}` | Title for third user type | "Canadian Employers" |
| `{{USER_TYPE_3_DESCRIPTION}}` | Description for third user type | "This draw validates the importance..." |

### 📋 List Variables (HTML Content)

| Variable | Purpose | Format |
|----------|---------|--------|
| `{{QUICK_FACTS_LIST}}` | Quick facts bullet points | `<li>Fact 1</li><li>Fact 2</li>` |
| `{{NEXT_STEPS_LIST}}` | Numbered next steps | `<li><div class="step-number">1</div><strong>Step Title:</strong> Description</li>` |
| `{{DRAW_DETAILS_LIST}}` | Official draw details | `<li><strong>Draw Type:</strong> CEC-Only (Program-Specific)</li>` |
| `{{SOURCE_LINKS_LIST}}` | Source links | `<li><a href="URL">🔗 Link Text</a></li>` |
| `{{TAGS_LIST}}` | Related topic tags | `<a href="#" class="news-tag">Express Entry</a>` |
| `{{RELATED_NEWS_LIST}}` | Related news articles | `<a href="URL" class="related-item"><h4>Title</h4><div class="date">Date</div></a>` |

### 🔗 Navigation & Path Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `{{HOME_PATH}}` | Path to home page | "../../../../../" |
| `{{REPORTS_PATH}}` | Path to reports | "../../../../../reports/" |
| `{{TOOLS_PATH}}` | Path to tools | "../../../../../tools/" |
| `{{NEWS_PATH}}` | Path to news | "../../../../" |
| `{{DAILY_PATH}}` | Path to daily news | "../../../" |
| `{{DRAWS_PATH}}` | Path to draws | "../../" |
| `{{ABOUT_PATH}}` | Path to about | "../../../../../about/" |
| `{{NEWSLETTER_PATH}}` | Path to newsletter | "../../../../" |
| `{{BREADCRUMB_TITLE}}` | Breadcrumb title | "Express Entry CEC Draw" |

### 📤 Sharing Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `{{CANONICAL_URL}}` | Full article URL | "https://immiwatch.ca/news/daily/draws/2025-07-08/express-entry-cec-draw-3000-itas-518-crs/" |
| `{{SHARE_TITLE}}` | Title for social sharing | "Express Entry CEC Draw: 3,000 ITAs at CRS 518" |
| `{{KEYWORDS_ARRAY}}` | Keywords for structured data | `"Express Entry", "CEC draw", "3000 ITAs", "CRS 518"` |

### 📄 Article Content Variable

| Variable | Purpose | Format |
|----------|---------|--------|
| `{{ARTICLE_CONTENT}}` | Full article body content | Complete HTML content with `<h3>`, `<h4>`, `<p>` tags |

## Usage Examples

### Example 1: CEC Draw
```python
template_vars = {
    "TITLE": "Express Entry CEC Draw: 3,000 ITAs Issued at CRS 518",
    "ITAS_ISSUED": "3,000",
    "CRS_CUTOFF": "518",
    "DRAW_TYPE_ICON": "🇨🇦",
    "DRAW_TYPE_NAME": "CEC",
    "HEADER_GRADIENT": "#059669 0%, #047857 100%",
    # ... other variables
}
```

### Example 2: Health Draw
```python
template_vars = {
    "TITLE": "Historic Express Entry Health Draw: 4,000 ITAs Issued with 475 CRS Cutoff",
    "ITAS_ISSUED": "4,000",
    "CRS_CUTOFF": "475",
    "DRAW_TYPE_ICON": "🏥",
    "DRAW_TYPE_NAME": "Health",
    "HEADER_GRADIENT": "#dc2626 0%, #b91c1c 100%",
    # ... other variables
}
```

### Example 3: General Draw
```python
template_vars = {
    "TITLE": "Express Entry General Draw: 4,750 ITAs Issued at CRS 491",
    "ITAS_ISSUED": "4,750",
    "CRS_CUTOFF": "491",
    "DRAW_TYPE_ICON": "🌐",
    "DRAW_TYPE_NAME": "General",
    "HEADER_GRADIENT": "#059669 0%, #047857 100%",
    # ... other variables
}
```

## Template Features

### 🎨 Visual Enhancements
- **Statistics Card:** Prominent display of draw statistics
- **Quick Facts Box:** Yellow-themed box with key takeaways
- **User Impact Section:** Three user-type cards with personalized guidance
- **Next Steps Section:** Numbered steps with circular badges
- **Enhanced Typography:** Better visual hierarchy and readability
- **Mobile Responsive:** Optimized for all screen sizes

### 🎭 Interactive Elements
- **Hover Effects:** Cards lift and scale on hover
- **Animations:** Fade-in animations for new sections
- **Color Coding:** Different colors for different impact levels
- **Smooth Transitions:** All interactive elements have smooth transitions

### 📱 Mobile Optimization
- **Responsive Grid:** Statistics grid adapts to mobile
- **Touch-Friendly:** All interactive elements are touch-friendly
- **Readable Typography:** Optimized font sizes for mobile
- **Simplified Navigation:** Mobile menu with hamburger icon

## Implementation Notes

### File Structure
```
news/daily/draws/YYYY-MM-DD/article-slug/
└── index.html
```

### URL Structure
```
/news/daily/draws/YYYY-MM-DD/article-slug/
```

### SEO Optimization
- **Meta Tags:** Complete Open Graph and Twitter Card support
- **Structured Data:** JSON-LD schema markup
- **Canonical URLs:** Proper canonical URL structure
- **Breadcrumbs:** SEO-friendly breadcrumb navigation

### Performance
- **Optimized CSS:** Minimal, efficient styles
- **Fast Loading:** Optimized images and fonts
- **Caching:** Proper cache headers for static assets

## Next Steps

1. **Update Automation Script:** Modify `news_automation.py` to use this template
2. **Create Template Parser:** Build a function to replace template variables
3. **Test with Real Data:** Test the template with actual draw data
4. **Deploy and Monitor:** Deploy and monitor performance

This template represents the **GOLD STANDARD** for draw news articles and should be used for all future draw-based content. 