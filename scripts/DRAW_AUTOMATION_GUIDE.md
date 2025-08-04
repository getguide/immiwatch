# 🎯 Draw Automation System Guide

## Overview
The Draw Automation System is a specialized automation for Express Entry draw news articles. It uses the **GOLD STANDARD template** to create high-quality draw articles with enhanced visual features, AI-like analysis, and automatic updates to category pages.

## 🏗️ System Architecture

### Components
1. **`draw_automation.py`** - Main automation script
2. **`draw_news_template.html`** - GOLD STANDARD template
3. **`.github/workflows/draw_automation.yml`** - GitHub Actions workflow
4. **`airtable_draw_script.js`** - Airtable automation script
5. **`test_draw_automation.py`** - Test suite

### Workflow
```
Airtable → GitHub Repository Dispatch → GitHub Actions → Draw Automation → Article Creation → Page Updates → Slack Notification
```

## 🚀 Quick Start

### 1. Setup GitHub Actions
The workflow is already configured in `.github/workflows/draw_automation.yml` and will trigger on `draw_article` repository dispatch events.

### 2. Setup Airtable
Copy the `airtable_draw_script.js` content into your Airtable automation and configure the GitHub token.

### 3. Test the System
```bash
python scripts/test_draw_automation.py
```

## 📋 Required Airtable Fields

### Required Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `Headline` | Text | Article headline | "Express Entry CEC Draw: 3,000 ITAs Issued at CRS 518" |
| `Summary` | Text | Brief summary | "IRCC conducted a CEC-specific draw on July 8, 2025" |
| `invitation` | Number | Number of ITAs issued | 3000 |
| `cutoff` | Number | CRS cutoff score | 518 |
| `draw_type` | Single Select | Type of draw | CEC, Health, PNP, General, FSTP, FSWP |
| `date` | Date | Draw date (YYYY-MM-DD) | 2025-07-08 |

### Optional Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `source` | Text | Source attribution | "IRCC Official" |
| `impact_level` | Single Select | Impact classification | High, Critical, Moderate, Low |

## 🎯 Supported Draw Types

| Draw Type | Icon | Color Theme | Description |
|-----------|------|-------------|-------------|
| **CEC** | 🇨🇦 | Green | Canadian Experience Class |
| **Health** | 🏥 | Red | Healthcare Occupations |
| **PNP** | 🏛️ | Blue | Provincial Nominee Program |
| **General** | 🌐 | Green | All Programs |
| **FSTP** | 🔧 | Purple | Federal Skilled Trades Program |
| **FSWP** | 👔 | Green | Federal Skilled Worker Program |

## 🔧 Configuration

### GitHub Token Setup
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Create a new token with `repo` permissions
3. Add the token to your Airtable script: `const GITHUB_TOKEN = 'your_token_here';`

### Slack Webhook Setup
1. Create a Slack app and get the webhook URL
2. Add to GitHub repository secrets as `SLACK_WEBHOOK_URL`

### Environment Variables
```bash
# Required for GitHub Actions
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# Required for Airtable script
GITHUB_TOKEN=ghp_your_token_here
```

## 📊 Data Processing

### AI-Like Analysis
The system automatically generates:
- **Impact Level**: Based on ITA count (Critical: 4000+, High: 2000+, etc.)
- **Executive Summary**: Comprehensive draw analysis
- **User Impact**: Personalized guidance for different user types
- **Strategic Analysis**: Program-specific insights
- **Next Steps**: Actionable recommendations

### Content Generation
- **Statistics Card**: Prominent display of draw data
- **Quick Facts**: Key takeaways with checkmarks
- **User Impact Cards**: Three user types with personalized advice
- **Next Steps**: Numbered progression steps
- **Related News**: Links to relevant articles

## 🎨 Template Features

### Visual Enhancements
- **Statistics Grid**: ITAs, CRS, Draw Type, Date
- **Quick Facts Box**: Yellow-themed with checkmarks
- **User Impact Section**: Three user-type cards
- **Next Steps**: Numbered with circular badges
- **Enhanced Typography**: Better visual hierarchy

### Interactive Elements
- **Hover Effects**: Cards lift and scale
- **Animations**: Fade-in animations
- **Color Coding**: Different colors for impact levels
- **Mobile Responsive**: Optimized for all devices

## 📝 Usage Examples

### Example 1: CEC Draw
```javascript
// Airtable data
{
    "Headline": "Express Entry CEC Draw: 3,000 ITAs Issued at CRS 518",
    "Summary": "IRCC conducted a CEC-specific draw on July 8, 2025",
    "invitation": 3000,
    "cutoff": 518,
    "draw_type": "CEC",
    "date": "2025-07-08",
    "source": "IRCC Official"
}
```

### Example 2: Health Draw
```javascript
// Airtable data
{
    "Headline": "Historic Express Entry Health Draw: 4,000 ITAs Issued with 475 CRS Cutoff",
    "Summary": "IRCC conducted a healthcare-specific draw on July 22, 2025",
    "invitation": 4000,
    "cutoff": 475,
    "draw_type": "Health",
    "date": "2025-07-22",
    "source": "IRCC Official"
}
```

## 🔄 Automation Workflow

### 1. Airtable Trigger
- User adds draw data to Airtable
- Airtable automation triggers
- Script validates and cleans data

### 2. GitHub Repository Dispatch
- Script sends data to GitHub API
- Triggers `draw_article` repository dispatch
- GitHub Actions workflow starts

### 3. Article Creation
- Python script analyzes data
- Generates enhanced content
- Creates article using GOLD STANDARD template
- Updates category pages
- Sends Slack notification

### 4. Page Updates
- Updates `/news/daily/draws/` with new article card
- Updates `/news/daily/` Latest News section
- Updates article count in category cards

## 🧪 Testing

### Run Test Suite
```bash
python scripts/test_draw_automation.py
```

### Test Components
- ✅ Draw type configurations
- ✅ Impact level calculations
- ✅ Template variable replacement
- ✅ Full automation workflow

### Manual Testing
```bash
# Test with sample data
python scripts/draw_automation.py
```

## 🚨 Error Handling

### Validation Errors
- Missing required fields
- Invalid numeric values
- Invalid draw types
- Invalid date formats

### Processing Errors
- Template file not found
- Directory creation failed
- File write errors
- GitHub API errors

### Slack Notifications
- Success: Article URL, title, statistics
- Error: Detailed error message and context

## 📈 Monitoring

### Success Metrics
- Article creation success rate
- Page update accuracy
- Slack notification delivery
- GitHub Actions workflow success

### Logging
- Detailed logs in GitHub Actions
- Console output for debugging
- Error tracking and reporting

## 🔧 Troubleshooting

### Common Issues

#### 1. GitHub API Errors
```
GitHub API error: 401 - Bad credentials
```
**Solution**: Check GitHub token permissions and validity

#### 2. Template Not Found
```
FileNotFoundError: [Errno 2] No such file or directory: 'draw_news_template.html'
```
**Solution**: Ensure template file exists in scripts directory

#### 3. Slack Notification Failed
```
Failed to send Slack notification: 400 Bad Request
```
**Solution**: Check Slack webhook URL format and validity

#### 4. Invalid Draw Type
```
Invalid draw type: INVALID_TYPE. Valid types: CEC, Health, PNP, General, FSTP, FSWP
```
**Solution**: Use one of the supported draw types

### Debug Mode
```python
# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
```

## 🎯 Best Practices

### Data Quality
- Always validate draw data before processing
- Use consistent date formats (YYYY-MM-DD)
- Ensure numeric fields are valid integers
- Use supported draw types only

### Content Standards
- Follow the GOLD STANDARD template structure
- Maintain consistent visual design
- Ensure mobile responsiveness
- Optimize for SEO

### Automation Reliability
- Test with sample data before production
- Monitor GitHub Actions workflow success
- Set up proper error notifications
- Maintain backup procedures

## 🚀 Deployment

### Production Setup
1. Configure GitHub repository secrets
2. Set up Airtable automation with correct script
3. Test with sample draw data
4. Monitor initial deployments

### Maintenance
- Regular testing with sample data
- Monitor GitHub Actions workflow logs
- Update template as needed
- Backup automation scripts

## 📚 Additional Resources

- **Template Guide**: `DRAW_TEMPLATE_GUIDE.md`
- **Test Suite**: `test_draw_automation.py`
- **GitHub Actions**: `.github/workflows/draw_automation.yml`
- **Airtable Script**: `airtable_draw_script.js`

This system represents the **GOLD STANDARD** for draw news automation, providing professional-quality articles with enhanced user experience and comprehensive automation. 