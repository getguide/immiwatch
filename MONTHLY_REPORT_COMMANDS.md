# 📊 Monthly Report Generation Commands

## ⚡ **For AI Agents: Use These Commands for Monthly Reports**

### **Generate New Monthly Report**
```bash
# Basic generation (uses default data)
python3 scripts/generate_monthly_report.py 2025-08

# With custom data file
python3 scripts/generate_monthly_report.py 2025-08 --data-file august_data.json

# With custom template
python3 scripts/generate_monthly_report.py 2025-08 --template reports/express-entry/ee-july-2025/index.html
```

### **Update Existing Monthly Report**
```bash
# Update with new draw data
python3 scripts/update_monthly_report.py 2025-08 --draw-data august_draw_1.json

# Update with second draw
python3 scripts/update_monthly_report.py 2025-08 --draw-data august_draw_2.json
```

### **Complete Workflow Example**
```bash
# 1. Create data file from template
cp scripts/monthly_report_data_template.json august_2025_data.json

# 2. Edit august_2025_data.json with actual data
# 3. Generate the report
python3 scripts/generate_monthly_report.py 2025-08 --data-file august_2025_data.json

# 4. Test locally
python3 -m http.server 8000
# Visit: http://localhost:8000/reports/express-entry/ee-august-2025/

# 5. Commit and push
git add .
git commit -m "📊 Add August 2025 Express Entry report"
git push origin main
```

## 📋 **Data Template Structure**
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

## 📚 **Full Documentation**
- **Complete Guide**: [docs/MONTHLY_REPORT_COMPLETE_GUIDE.md](docs/MONTHLY_REPORT_COMPLETE_GUIDE.md)
- **Data Template**: [scripts/monthly_report_data_template.json](scripts/monthly_report_data_template.json)
- **Draw Template**: [scripts/draw_data_template.json](scripts/draw_data_template.json)
- **Generator Script**: [scripts/generate_monthly_report.py](scripts/generate_monthly_report.py)
- **Updater Script**: [scripts/update_monthly_report.py](scripts/update_monthly_report.py)

## ⚠️ **IMPORTANT**
- **Always use the generator** for new monthly reports
- **Use the updater** for draw-by-draw updates
- **Never manually copy** existing reports
- **Test thoroughly** before deployment
- **Use official data sources** for accuracy

---
**Last Updated**: July 2025  
**For AI Agents**: Check this file first before creating monthly reports. 