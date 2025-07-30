# 📊 Monthly Express Entry Report Generator

## 🎯 **Overview**

The Monthly Express Entry Report Generator is an automated system that creates new monthly reports by cloning the approved template design and updating it with month-specific data. This ensures **consistency, efficiency, and professional quality** across all monthly reports.

## 🚀 **Quick Start**

### **Generate a New Monthly Report**

```bash
# Basic generation (uses default data)
python3 scripts/generate_monthly_report.py 2025-08

# With custom data file
python3 scripts/generate_monthly_report.py 2025-08 --data-file august_data.json

# With custom template
python3 scripts/generate_monthly_report.py 2025-08 --template reports/express-entry/ee-july-2025/index.html
```

### **Example: Create August 2025 Report**

```bash
# 1. Create data file
cp scripts/monthly_report_data_template.json august_2025_data.json

# 2. Edit the data file with August 2025 data
# 3. Generate the report
python3 scripts/generate_monthly_report.py 2025-08 --data-file august_2025_data.json

# 4. Review and test
# 5. Commit and push
```

## 📋 **System Architecture**

### **Template-Based Design**
- **Base Template**: `reports/express-entry/ee-april-2025/index.html`
- **Consistent Design**: All reports maintain the same professional layout
- **Automated Updates**: Month-specific content automatically generated
- **Quality Assurance**: Built-in validation and error handling

### **Data Structure**
```json
{
  "total_itas": 5000,
  "cec_itas": 3000,
  "pnp_itas": 1000,
  "fsw_itas": 0,
  "fst_itas": 0,
  "category_based_total": 1000,
  "french_speaking": 500,
  "healthcare": 300,
  "stem": 0,
  "trade": 0,
  "education": 200,
  "agriculture": 0,
  "executive_summary": "August 2025 analysis...",
  "strategic_insights": ["Insight 1", "Insight 2"],
  "key_highlights": ["Highlight 1", "Highlight 2"]
}
```

## 🔧 **Features**

### **Automatic Content Updates**
- ✅ **Meta Tags**: Title, description, Open Graph tags
- ✅ **Navigation**: Breadcrumbs, previous/next month links
- ✅ **Statistics**: ITA numbers with animation support
- ✅ **Executive Summary**: Month-specific analysis
- ✅ **Program Tables**: Updated with new data
- ✅ **Social Sharing**: Month-specific share text
- ✅ **Strategic Analysis**: Updated insights and recommendations

### **Smart Month Handling**
- ✅ **Month Names**: Automatic month name generation
- ✅ **Emojis**: Month-specific emojis (❄️ January, 🌸 February, etc.)
- ✅ **Navigation Links**: Automatic previous/next month calculation
- ✅ **URL Generation**: Proper directory structure
- ✅ **Year Transitions**: Handles year-end and year-beginning

### **Quality Assurance**
- ✅ **Data Validation**: Ensures data format is correct
- ✅ **Template Validation**: Checks template file exists
- ✅ **Error Handling**: Graceful error messages
- ✅ **Progress Reporting**: Clear status updates

## 📊 **Data Template**

### **Required Fields**
```json
{
  "total_itas": 5000,           // Total ITAs issued
  "cec_itas": 3000,             // Canadian Experience Class
  "pnp_itas": 1000,             // Provincial Nominee Program
  "fsw_itas": 0,                // Federal Skilled Worker
  "fst_itas": 0,                // Federal Skilled Trades
  "category_based_total": 1000, // Total category-based ITAs
  "french_speaking": 500,        // French-speaking category
  "healthcare": 300,             // Healthcare category
  "stem": 0,                    // STEM category
  "trade": 0,                   // Trade category
  "education": 200,              // Education category
  "agriculture": 0,              // Agriculture category
  "executive_summary": "Your executive summary here...",
  "strategic_insights": ["Insight 1", "Insight 2"],
  "key_highlights": ["Highlight 1", "Highlight 2"]
}
```

### **Optional Fields**
```json
{
  "month_comparison": {
    "previous_month": "2025-07",
    "growth_percentage": 15.5,
    "key_changes": ["Change 1", "Change 2"]
  },
  "category_analysis": {
    "french_speaking_impact": "Analysis text...",
    "healthcare_focus": "Healthcare analysis...",
    "stem_trade_status": "STEM/Trade status..."
  },
  "predictions": {
    "next_month_outlook": "Prediction text...",
    "trend_analysis": "Trend analysis...",
    "strategic_recommendations": ["Rec 1", "Rec 2"]
  }
}
```

## 🎯 **Usage Examples**

### **Example 1: Quick Generation**
```bash
# Generate August 2025 with default data
python3 scripts/generate_monthly_report.py 2025-08
```

### **Example 2: Custom Data**
```bash
# 1. Create data file
cp scripts/monthly_report_data_template.json august_data.json

# 2. Edit august_data.json with actual data
# 3. Generate report
python3 scripts/generate_monthly_report.py 2025-08 --data-file august_data.json
```

### **Example 3: Custom Template**
```bash
# Use July 2025 as template instead of April
python3 scripts/generate_monthly_report.py 2025-08 --template reports/express-entry/ee-july-2025/index.html
```

## 📁 **Output Structure**

### **Generated Files**
```
reports/express-entry/
├── ee-august-2025/
│   └── index.html          # Generated report
├── ee-september-2025/
│   └── index.html          # Future report
└── ee-october-2025/
    └── index.html          # Future report
```

### **URL Structure**
- **Generated URL**: `https://immiwatch.ca/reports/express-entry/ee-august-2025/`
- **Navigation**: Automatic breadcrumb and menu integration
- **SEO**: Optimized meta tags and descriptions

## 🔄 **Workflow**

### **1. Data Collection**
```bash
# Gather monthly data from government sources
# Update data template with actual numbers
```

### **2. Report Generation**
```bash
# Generate the report
python3 scripts/generate_monthly_report.py 2025-08 --data-file august_data.json
```

### **3. Review & Testing**
```bash
# Test locally
python3 -m http.server 8000
# Visit: http://localhost:8000/reports/express-entry/ee-august-2025/
```

### **4. Deployment**
```bash
# Commit and push
git add .
git commit -m "📊 Add August 2025 Express Entry report"
git push origin main
```

## 🛡️ **Best Practices**

### **Data Accuracy**
- ✅ **Verify Numbers**: Double-check all ITA numbers
- ✅ **Source Data**: Use official government sources
- ✅ **Consistency**: Ensure totals match breakdowns
- ✅ **Validation**: Test generated report thoroughly

### **Content Quality**
- ✅ **Executive Summary**: Write compelling analysis
- ✅ **Strategic Insights**: Provide valuable recommendations
- ✅ **Key Highlights**: Focus on important trends
- ✅ **Professional Tone**: Maintain consistent voice

### **Technical Quality**
- ✅ **Test Locally**: Always test before deployment
- ✅ **Check Links**: Verify navigation works correctly
- ✅ **Mobile Responsive**: Test on mobile devices
- ✅ **SEO Optimization**: Verify meta tags

## 🚨 **Troubleshooting**

### **Common Issues**

**Problem**: Template file not found
```bash
# Solution: Check template path
ls reports/express-entry/ee-april-2025/index.html
```

**Problem**: Invalid month format
```bash
# Solution: Use YYYY-MM format
python3 scripts/generate_monthly_report.py 2025-08  # ✅ Correct
python3 scripts/generate_monthly_report.py 08-2025  # ❌ Wrong
```

**Problem**: Data file not found
```bash
# Solution: Create data file first
cp scripts/monthly_report_data_template.json my_data.json
# Edit my_data.json, then run generator
```

### **Error Messages**
- **"Template file not found"**: Check template path
- **"Invalid month format"**: Use YYYY-MM format
- **"Data file not found"**: Create data file first
- **"Permission denied"**: Check file permissions

## 📈 **Future Enhancements**

### **Planned Features**
- 🔄 **Newsletter Integration**: Auto-generate newsletter content
- 🔄 **News Article Generation**: Create news articles from reports
- 🔄 **Data Validation**: Enhanced data validation
- 🔄 **Template Customization**: More template options
- 🔄 **Batch Generation**: Generate multiple months at once

### **Integration Opportunities**
- 🔄 **API Integration**: Pull data from government APIs
- 🔄 **Automated Scheduling**: Monthly report generation
- 🔄 **Analytics Integration**: Track report performance
- 🔄 **Social Media**: Auto-post to social platforms

## 🤝 **Team Collaboration**

### **For AI Agents**
- **Always use the generator** for new monthly reports
- **Follow the data template** structure
- **Test thoroughly** before deployment
- **Update documentation** if needed

### **For Human Developers**
- **Review generated reports** for accuracy
- **Maintain template quality** in base template
- **Update data sources** as needed
- **Monitor system performance**

## 📞 **Support Resources**

- **Template**: `reports/express-entry/ee-april-2025/index.html`
- **Data Template**: `scripts/monthly_report_data_template.json`
- **Generator Script**: `scripts/generate_monthly_report.py`
- **Documentation**: This guide and related docs
- **Examples**: Existing monthly reports for reference

---

**Last Updated**: July 2025  
**Maintained By**: ImmiWatch Development Team  
**Version**: 1.0 