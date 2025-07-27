# 📊 Data Formats & Specifications

> **Comprehensive data structure definitions for ImmiWatch platform**

## 🎯 **Overview**

This document defines all data formats, structures, and validation rules used across the ImmiWatch platform. Maintaining consistency in data formats is crucial for accurate analysis and seamless updates.

## 📋 **Express Entry Draw Data**

### **Draw Record Structure**
```javascript
{
  drawNumber: Number,        // Sequential draw number (e.g., 357)
  date: String,             // "Month DD, YYYY" format
  roundType: String,        // Program/category type
  invitationsIssued: Number, // Number of ITAs issued
  crsScore: Number,         // Minimum CRS score invited
  year: Number,             // Year of the draw
  month: String,            // Month name
  category: String          // "program" or "category"
}
```

### **Example Draw Records**
```javascript
// Program-Based Draw
{
  drawNumber: 356,
  date: "July 21, 2025",
  roundType: "Provincial Nominee Program",
  invitationsIssued: 202,
  crsScore: 788,
  year: 2025,
  month: "July",
  category: "program"
}

// Category-Based Draw
{
  drawNumber: 357,
  date: "July 22, 2025",
  roundType: "Healthcare and social services occupations (Version 2)",
  invitationsIssued: 4000,
  crsScore: 475,
  year: 2025,
  month: "July",
  category: "category"
}
```

### **Program Type Classifications**
```javascript
const PROGRAM_TYPES = {
  "Provincial Nominee Program": "PNP",
  "Canadian Experience Class": "CEC",
  "Federal Skilled Worker": "FSW",
  "Federal Skilled Trades": "FST"
};

const CATEGORY_TYPES = {
  "Healthcare and social services occupations": "Healthcare",
  "French language proficiency": "French",
  "Education occupations": "Education",
  "STEM occupations": "STEM",
  "Transport occupations": "Transport",
  "Agriculture and agri-food occupations": "Agriculture",
  "Trades occupations": "Trades"
};
```

## 🏊‍♂️ **Pool Distribution Data**

### **Pool Data Structure**
```javascript
{
  asOfDate: String,          // "Month DD, YYYY"
  totalCandidates: Number,   // Total pool size
  scoreRanges: [             // Array of score range objects
    {
      range: String,         // e.g., "601-1200"
      candidates: Number,    // Number of candidates in range
      percentage: Number,    // Percentage of total pool
      description: String,   // Competition level description
      color: String         // Display color code
    }
  ]
}
```

### **Example Pool Data**
```javascript
{
  asOfDate: "July 20, 2025",
  totalCandidates: 256914,
  scoreRanges: [
    {
      range: "601-1200",
      candidates: 200,
      percentage: 0.08,
      description: "Elite Tier",
      color: "success"
    },
    {
      range: "501-600",
      candidates: 21348,
      percentage: 8.3,
      description: "Sweet Spot",
      color: "primary"
    },
    {
      range: "451-500",
      candidates: 78339,
      percentage: 30.5,
      description: "High Competition",
      color: "warning"
    }
  ]
}
```

## 📊 **Capacity Tracking Data**

### **Capacity Structure**
```javascript
{
  year: Number,                    // Target year (2025)
  categoryBased: {
    target: Number,                // Annual target (62,000)
    used: Number,                  // PRs used to date
    itasIssued: Number,           // ITAs issued to date
    coefficient: Number,           // Conversion coefficient (1.6)
    percentageUsed: Number,        // Percentage of capacity used
    remaining: Number              // Remaining capacity
  },
  programBased: {
    target: Number,                // Annual target (89,000)
    used: Number,                  // PRs used to date
    itasIssued: Number,           // ITAs issued to date
    coefficient: Number,           // Conversion coefficient (1.6)
    percentageUsed: Number,        // Percentage of capacity used
    remaining: Number              // Remaining capacity
  }
}
```

### **Example Capacity Data**
```javascript
{
  year: 2025,
  categoryBased: {
    target: 62000,
    used: 39200,
    itasIssued: 24500,
    coefficient: 1.6,
    percentageUsed: 63,
    remaining: 22800
  },
  programBased: {
    target: 89000,
    used: 40000,
    itasIssued: 24903,
    coefficient: 1.6,
    percentageUsed: 45,
    remaining: 49000
  }
}
```

## 🔮 **Prediction Data**

### **Prediction Structure**
```javascript
{
  program: String,              // "PNP", "CEC", "Healthcare", etc.
  nextDrawDate: {
    earliest: String,           // "Aug 4, 2025"
    latest: String,             // "Aug 5, 2025"
    confidence: String          // "High", "Medium", "Low"
  },
  expectedSize: {
    min: Number,                // Minimum expected ITAs
    max: Number,                // Maximum expected ITAs
    average: Number             // Average expected ITAs
  },
  pattern: {
    frequency: String,          // "Bi-weekly", "Monthly", etc.
    timing: String,             // "Early + Mid-month", "After PNP", etc.
    reliability: String         // "Consistent", "Variable", "Unpredictable"
  }
}
```

## 📈 **Historical Analysis Data**

### **Pattern Analysis Structure**
```javascript
{
  program: String,
  period: String,               // "Q1 2025", "2025 YTD", etc.
  patterns: {
    frequency: {
      days: Number,             // Average days between draws
      variance: Number,         // Standard deviation
      trend: String            // "Increasing", "Stable", "Decreasing"
    },
    size: {
      average: Number,          // Average ITAs per draw
      min: Number,              // Minimum ITAs
      max: Number,              // Maximum ITAs
      trend: String            // Size trend
    },
    crsScore: {
      average: Number,          // Average CRS score
      min: Number,              // Lowest score
      max: Number,              // Highest score
      trend: String            // Score trend
    }
  }
}
```

## 🔄 **Data Validation Rules**

### **Draw Data Validation**
```javascript
const validateDraw = (draw) => {
  const rules = {
    drawNumber: (n) => n > 0 && Number.isInteger(n),
    date: (d) => /^[A-Za-z]+ \d{1,2}, \d{4}$/.test(d),
    invitationsIssued: (i) => i > 0 && Number.isInteger(i),
    crsScore: (s) => s >= 300 && s <= 1200,
    roundType: (t) => typeof t === 'string' && t.length > 0
  };
  
  return Object.entries(rules).every(([field, rule]) => 
    rule(draw[field])
  );
};
```

### **Pool Data Validation**
```javascript
const validatePoolData = (pool) => {
  const rules = {
    totalCandidates: (n) => n > 0 && Number.isInteger(n),
    scoreRanges: (ranges) => {
      const total = ranges.reduce((sum, r) => sum + r.candidates, 0);
      return Math.abs(total - pool.totalCandidates) < 100; // Allow small variance
    }
  };
  
  return Object.entries(rules).every(([field, rule]) => 
    rule(pool[field])
  );
};
```

## 📊 **Data Sources & URLs**

### **Primary Sources**
```javascript
const DATA_SOURCES = {
  draws: "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/submit-profile/rounds-invitations.html",
  poolData: "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/submit-profile/rounds-invitations/dynamic-report.html",
  levels: "https://www.canada.ca/en/immigration-refugees-citizenship/news/notices/supplementary-immigration-levels-2024-2026.html",
  ministerialInstructions: "https://www.canada.ca/en/immigration-refugees-citizenship/corporate/mandate/policies-operational-instructions-agreements/ministerial-instructions.html"
};
```

### **Backup Sources**
```javascript
const BACKUP_SOURCES = {
  immigrationNews: "https://www.cicnews.com/category/express-entry",
  lawyerUpdates: "Twitter: @immigration_ca, @CanadaVisa",
  consultantForums: "Canadian Association of Professional Immigration Consultants"
};
```

## 🎨 **Display Format Standards**

### **Number Formatting**
```javascript
const formatNumbers = {
  drawNumber: (n) => `#${n}`,
  invitations: (n) => n.toLocaleString(),
  crsScore: (n) => n.toString(),
  percentage: (n) => `${n}%`,
  candidates: (n) => n.toLocaleString(),
  currency: (n) => `$${n.toLocaleString()}`
};
```

### **Date Formatting**
```javascript
const formatDates = {
  display: "Month DD, YYYY",         // "July 22, 2025"
  short: "MMM DD",                   // "Jul 22"
  iso: "YYYY-MM-DD",                 // "2025-07-22"
  prediction: "MMM DD-DD"            // "Aug 4-5"
};
```

### **Color Coding Standards**
```javascript
const COLORS = {
  success: "#10b981",     // Green - positive indicators
  warning: "#f59e0b",     // Orange - caution indicators
  error: "#ef4444",       // Red - negative indicators
  primary: "#3b82f6",     // Blue - neutral/informational
  accent: "#8b5cf6",      // Purple - special highlights
  gray: "#6b7280"         // Gray - secondary information
};
```

## 📋 **Template Files**

### **Draw Data Template** (`draw-template.json`)
```json
{
  "drawNumber": 0,
  "date": "",
  "roundType": "",
  "invitationsIssued": 0,
  "crsScore": 0,
  "notes": ""
}
```

### **Pool Data Template** (`pool-template.json`)
```json
{
  "asOfDate": "",
  "totalCandidates": 0,
  "scoreRanges": [
    {
      "range": "",
      "candidates": 0,
      "percentage": 0
    }
  ]
}
```

## 🔍 **Data Quality Checks**

### **Automated Validation**
- Draw numbers must be sequential
- Dates must be chronological
- ITA numbers must be reasonable (< 50,000 per draw)
- CRS scores must be within valid range (300-1200)
- Pool totals must match sum of ranges

### **Manual Review Points**
- Unusual draw sizes (< 100 or > 10,000 ITAs)
- CRS score changes > 50 points
- New program types or categories
- Timing anomalies (draws on weekends/holidays)

---

**Last Updated**: July 27, 2025  
**Next Review**: August 30, 2025 