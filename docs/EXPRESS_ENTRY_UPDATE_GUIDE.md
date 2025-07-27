# 📊 Express Entry Dashboard Update Guide

> **Complete step-by-step guide for maintaining the Express Entry Capacity Intelligence Dashboard**

## 🎯 **Overview**

This guide covers all procedures for updating the Express Entry 2025 dashboard located at:
- **File**: `reports/express-entry/ee-2025/index.html`
- **Live URL**: https://immiwatch.ca/reports/express-entry/ee-2025/

## 📅 **Update Schedule**

### **Weekly Updates** (After each draw announcement)
- Update recent draw history table
- Adjust next draw predictions
- Update "days since last" counters

### **Monthly Updates** (30th of each month)
- Comprehensive capacity analysis
- Pool distribution data refresh
- Pattern recognition refinement
- Professional insights review

## 📊 **Data Sources**

### **1. Government of Canada - Express Entry Draws**
- **URL**: https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/submit-profile/rounds-invitations.html
- **Data Needed**: Draw number, date, program type, ITAs issued, CRS cutoff

### **2. Pool Distribution Data**
- **URL**: https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/submit-profile/rounds-invitations/dynamic-report.html
- **Data Needed**: CRS score ranges, candidate counts, total pool size

### **3. Immigration Levels Plan**
- **URL**: https://www.canada.ca/en/immigration-refugees-citizenship/news/notices/supplementary-immigration-levels-2024-2026.html
- **Data Needed**: Annual PR targets by stream

## 🔄 **Weekly Update Procedure**

### **Step 1: Data Collection**
1. Check Government of Canada for new draws
2. Record draw details in the format:
   ```
   Draw #, Date, Program Type, ITAs, CRS Score
   357, July 22 2025, Healthcare, 4000, 475
   ```

### **Step 2: Update Recent Draw History Table**
**Location**: `reports/express-entry/ee-2025/index.html` (lines ~450-550)

**Find the table section:**
```html
<table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
  <thead>
    <tr style="background: var(--gray-50);">
      <th>Date</th><th>Program</th><th>ITAs</th><th>CRS</th>
    </tr>
  </thead>
  <tbody>
    <!-- UPDATE THIS SECTION -->
  </tbody>
</table>
```

**Add new draws to the top**, remove oldest entries to maintain 10 recent draws.

### **Step 3: Update Draw Predictions**
**Location**: Lines ~380-420

**Update the prediction cards:**
- **PNP**: Calculate 13-14 days from last PNP draw
- **CEC**: Check if pattern suggests 1-2 days after next PNP
- **Category-Based**: Update based on monthly patterns

### **Step 4: Update Counters**
**Update "days since last" counters:**
- CEC status alert: Calculate days since last CEC draw
- Category-based draws: Update timing estimates

## 📊 **Monthly Update Procedure**

### **Step 1: Capacity Analysis Update**
**Location**: Lines ~200-350

**Update the capacity tracking dashboard:**

1. **Calculate new ITAs issued**:
   - Sum all ITAs from the last month
   - Add to year-to-date totals

2. **Update capacity percentages**:
   ```
   Category-Based Used = (Category ITAs × 1.6) / 62,000
   Program-Based Used = (Program ITAs × 1.6) / 89,000
   ```

3. **Update progress bars**:
   - Adjust `width: XX%` in progress bar styles
   - Update percentage text inside bars

### **Step 2: Pool Distribution Update**
**Location**: Lines ~180-250

**When new pool data is available:**

1. **Update pool overview cards**:
   ```html
   <div style="font-size: 1.8rem; font-weight: 700; color: var(--primary-600);">256,914</div>
   <div style="font-size: 0.9rem; color: var(--gray-600);">Total Pool Size</div>
   ```

2. **Update competition intensity bars**:
   - Recalculate percentages for each CRS range
   - Adjust progress bar widths accordingly

### **Step 3: Pattern Analysis Review**
**Location**: Lines ~380-450

**Review and update prediction patterns:**

1. **PNP Pattern**: Verify 13-14 day cycle still accurate
2. **CEC Pattern**: Check if 1-2 day delay still holds
3. **Category-Based**: Update frequency assessments

### **Step 4: Professional Insights Update**
**Location**: Lines ~460-550

**Update government priority analysis:**
- Add new draws to category totals
- Update percentage calculations
- Refresh strategic recommendations

## 🎯 **Data Format Examples**

### **Draw History Format**
```javascript
{
  drawNumber: 357,
  date: "July 22, 2025",
  program: "Healthcare and social services occupations (Version 2)",
  invitations: 4000,
  crsScore: 475
}
```

### **Pool Distribution Format**
```javascript
{
  scoreRange: "601-1200",
  candidates: 200,
  description: "Elite Tier"
}
```

## ⚠️ **Critical Update Points**

### **1. Capacity Calculation**
- **Always use 1.6 multiplier** for PR conversion
- Category-Based target: 62,000 PRs
- Program-Based target: 89,000 PRs

### **2. Draw Pattern Recognition**
- **PNP**: Bi-weekly (early month + mid-month)
- **CEC**: Follows PNP by 1-2 days (selective)
- **Category-Based**: Variable timing

### **3. Professional Insights**
- Keep government priority critique updated
- Maintain strategic client recommendations
- Update critical timing windows

## 🔍 **Quality Checklist**

### **Before Publishing**
- [ ] All numbers are accurate and verified
- [ ] Draw history table shows latest 10 draws
- [ ] Predictions reflect actual patterns
- [ ] Pool data is current (if available)
- [ ] Professional insights are relevant
- [ ] No broken links or formatting issues

### **After Publishing**
- [ ] Test live site functionality
- [ ] Verify all numbers display correctly
- [ ] Check mobile responsiveness
- [ ] Confirm navigation works properly

## 🚨 **Emergency Updates**

### **Breaking News Scenarios**
1. **Unexpected Large Draw**: Update within 4 hours
2. **New Program Launch**: Comprehensive analysis within 24 hours
3. **Policy Changes**: Full dashboard review within 48 hours

### **Data Correction Procedures**
1. **Verify source data accuracy**
2. **Update affected calculations**
3. **Push corrected version immediately**
4. **Document correction in commit message**

## 📞 **Support & Questions**

### **Data Verification**
- Cross-reference with multiple government sources
- Check immigration lawyer social media for confirmations
- Verify unusual patterns before publishing

### **Technical Issues**
- Test locally before pushing to production
- Use browser dev tools to check console errors
- Verify CSS variables are working correctly

## 📝 **Update Log Template**

```markdown
## Update: [Date]

### Changes Made:
- [ ] Draw history updated (Draws #XXX-XXX)
- [ ] Capacity analysis refreshed
- [ ] Pool data updated
- [ ] Predictions adjusted
- [ ] Professional insights reviewed

### New Data:
- Total ITAs YTD: XX,XXX
- Capacity Used: XX%
- Pool Size: XXX,XXX candidates

### Next Update Due: [Date]
```

---

**Last Updated**: July 27, 2025  
**Next Review**: August 30, 2025 