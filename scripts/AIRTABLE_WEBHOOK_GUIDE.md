# 🔗 Airtable Webhook Script Guide

## The Bridge Between Airtable and News Automation

This guide explains how to set up the Airtable webhook script to send news data to our automation system with comprehensive logging and error handling.

## 📋 **OVERVIEW**

### **What This Script Does**
1. **Receives Airtable Records**: Processes triggered records from your Airtable base
2. **Validates Data**: Checks all required fields and data quality
3. **Transforms Data**: Maps Airtable fields to our automation format
4. **Sends to Automation**: Forwards validated data to our news automation system
5. **Logs Everything**: Comprehensive logging for debugging and monitoring
6. **Notifies Team**: Sends Slack notifications for success/failure

### **Key Features**
- ✅ **Comprehensive Validation**: Checks all required fields and data quality
- ✅ **Detailed Logging**: Every step is logged with timestamps
- ✅ **Error Handling**: Graceful handling of all error scenarios
- ✅ **Retry Logic**: Automatic retries for failed requests
- ✅ **Slack Integration**: Real-time notifications to your team
- ✅ **Data Cleaning**: Normalizes and validates all input data

## 🔧 **SETUP INSTRUCTIONS**

### **Step 1: Configure the Script**

Edit the configuration section in `airtable_webhook_script.js`:

```javascript
const CONFIG = {
    // Update these URLs to your actual endpoints
    AUTOMATION_WEBHOOK_URL: 'https://your-server.com/webhook/news',
    SLACK_WEBHOOK_URL: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK',
    
    // Logging level (DEBUG, INFO, WARN, ERROR)
    LOG_LEVEL: 'INFO',
    
    // Retry configuration
    MAX_RETRIES: 3,
    RETRY_DELAY: 2000
};
```

### **Step 2: Deploy the Script**

#### **Option A: Airtable Scripting App**
1. Open your Airtable base
2. Go to **Apps** → **Scripting**
3. Create a new script
4. Copy and paste the entire `airtable_webhook_script.js` content
5. Save and run the script

#### **Option B: External Webhook Service**
1. Deploy the script to a webhook service (Zapier, Make, etc.)
2. Configure the webhook to call our automation system
3. Set up the Airtable automation to trigger the webhook

### **Step 3: Set Up Airtable Automation**

1. **Create Automation**: In your Airtable base, go to **Automations**
2. **Choose Trigger**: "When a record is created" or "When a record is updated"
3. **Add Action**: "Run a script"
4. **Configure Script**: Use the webhook script with your data

## 📊 **FIELD MAPPING**

### **Airtable Fields → Automation Fields**

| Airtable Field Name | Automation Field | Required | Type | Description |
|-------------------|------------------|----------|------|-------------|
| `Headline` | `headline` | ✅ | Text | Article headline |
| `Summary` | `summary` | ✅ | Text | Brief summary |
| `Program Affected` | `program_affected` | ❌ | Multi-select | Affected programs |
| `Impact` | `impact` | ✅ | Single select | Impact level |
| `Urgency Level` | `urgency_level` | ❌ | Single select | Urgency level |
| `Week of Year` | `week_of_year` | ❌ | Number | Week number |
| `Date of Update` | `date_of_update` | ✅ | Date | Publication date |
| `Source URL` | `source_url` | ❌ | URL | Official source |
| `Source` | `source` | ❌ | Single select | Source organization |
| `Category` | `category` | ✅ | Single select | News category |
| `Cutoff` | `cutoff` | ❌ | Number | CRS cutoff (draws only) |
| `Invitation` | `invitation` | ❌ | Number | ITAs issued (draws only) |

### **Valid Values**

#### **Category Options**
- `policy` - Policy Announcements
- `draws` - Invitation Rounds
- `legal` - Legal Decisions
- `systems` - System Updates
- `programs` - Program Updates
- `documents` - Forms & Documents
- `analysis` - Analysis & Insights
- `other` - Other Updates

#### **Impact Levels**
- `critical` - Critical Impact
- `high` - High Impact
- `moderate` - Important Impact
- `low` - Medium Impact
- `informational` - Low Impact

#### **Program Affected Options**
- Express Entry
- Work Permit
- Study Permit
- Provincial Nominee Program
- Family Sponsorship
- Refugee Programs
- Citizenship
- Healthcare Occupations
- Tech Occupations
- Trade Occupations

## 🔍 **VALIDATION RULES**

### **Required Fields**
- `headline` - Must not be empty
- `summary` - Must not be empty
- `date_of_update` - Must be YYYY-MM-DD format
- `category` - Must be one of valid categories
- `impact` - Must be one of valid impact levels

### **Data Quality Checks**
- **Headline Length**: Warning if > 200 characters
- **Summary Length**: Warning if > 500 characters
- **URL Format**: Validates source URLs
- **Date Format**: Ensures YYYY-MM-DD format
- **Numeric Fields**: Validates cutoff and invitation numbers

### **Category-Specific Validation**
- **Draws Category**: Requires numeric cutoff and invitation values
- **All Categories**: Validates category-specific requirements

## 📝 **USAGE EXAMPLES**

### **Example 1: Express Entry Draw**

```javascript
// Airtable record data
const drawData = {
    record: {
        fields: {
            'Headline': 'Express Entry Draw #348: 2,500 ITAs with 485 CRS',
            'Summary': 'IRCC conducted Express Entry draw #348, issuing 2,500 ITAs with a CRS cutoff of 485 points.',
            'Program Affected': ['Express Entry', 'Work Permit'],
            'Impact': 'high',
            'Urgency Level': 'informational',
            'Week of Year': 31,
            'Date of Update': '2025-07-29',
            'Source URL': 'https://ircc.gc.ca/english/immigrate/express-entry/draws.asp',
            'Source': 'IRCC',
            'Category': 'draws',
            'Cutoff': 485,
            'Invitation': 2500
        }
    }
};

// Process the webhook
const result = await handleAirtableWebhook(drawData);
```

### **Example 2: Policy Announcement**

```javascript
// Airtable record data
const policyData = {
    record: {
        fields: {
            'Headline': 'New Express Entry Policy Changes Effective September 1',
            'Summary': 'IRCC announces significant changes to Express Entry system including new scoring criteria and processing improvements.',
            'Program Affected': ['Express Entry'],
            'Impact': 'critical',
            'Urgency Level': 'informational',
            'Week of Year': 31,
            'Date of Update': '2025-07-29',
            'Source URL': 'https://ircc.gc.ca/english/immigrate/express-entry/changes.asp',
            'Source': 'IRCC',
            'Category': 'policy'
        }
    }
};

// Process the webhook
const result = await handleAirtableWebhook(policyData);
```

## 🔔 **SLACK NOTIFICATIONS**

### **Success Notification**
```
✅ News article processed successfully!

**Article:** Express Entry Draw #348: 2,500 ITAs with 485 CRS
**Category:** draws
**Processing Time:** 1250ms
```

### **Error Notification**
```
❌ News article validation failed:
Missing required field: headline
Invalid category: invalid_category
```

### **Warning Notification**
```
⚠️ News article warnings:
Headline is very long (250 characters). Consider shortening.
Invalid source URL format: not-a-url
```

## 📊 **LOGGING**

### **Log Levels**
- **DEBUG**: Detailed information for debugging
- **INFO**: General information about processing
- **WARN**: Warning messages for data quality issues
- **ERROR**: Error messages for failures

### **Log Format**
```
[2025-07-29T15:30:45.123Z] INFO: Starting webhook processing
[2025-07-29T15:30:45.125Z] DEBUG: Extracted record data
[2025-07-29T15:30:45.130Z] INFO: Data validation completed
[2025-07-29T15:30:45.500Z] INFO: Request completed successfully
```

## 🛠️ **TROUBLESHOOTING**

### **Common Issues**

#### **1. Missing Required Fields**
```
Error: Missing required field: headline
Solution: Ensure all required fields are filled in Airtable
```

#### **2. Invalid Category**
```
Error: Invalid category: invalid_category
Solution: Use one of the valid categories: policy, draws, legal, systems, programs, documents, analysis, other
```

#### **3. Invalid Date Format**
```
Error: Invalid date format: 29-07-2025
Solution: Use YYYY-MM-DD format: 2025-07-29
```

#### **4. Network Errors**
```
Error: Request failed: Network timeout
Solution: Check webhook URL and network connectivity
```

### **Debug Mode**
Enable debug logging to see detailed information:

```javascript
const CONFIG = {
    LOG_LEVEL: 'DEBUG', // Change from 'INFO' to 'DEBUG'
    // ... other config
};
```

## 🔄 **RETRY LOGIC**

### **Automatic Retries**
- **Max Retries**: 3 attempts
- **Delay**: 2 seconds between attempts (increasing)
- **Conditions**: Network errors, timeouts, server errors

### **Retry Example**
```
[2025-07-29T15:30:45.123Z] INFO: Attempt 1/3 to send data to automation system
[2025-07-29T15:30:45.500Z] WARN: Attempt 1 failed: Network timeout
[2025-07-29T15:30:47.123Z] INFO: Attempt 2/3 to send data to automation system
[2025-07-29T15:30:47.500Z] INFO: Request completed successfully
```

## 🚀 **DEPLOYMENT OPTIONS**

### **Option 1: Airtable Scripting App**
1. Copy script to Airtable Scripting app
2. Configure automation trigger
3. Test with sample data

### **Option 2: External Webhook Service**
1. Deploy to Zapier, Make, or similar
2. Configure Airtable automation
3. Set up webhook endpoints

### **Option 3: Custom Server**
1. Deploy script to your server
2. Set up webhook endpoint
3. Configure Airtable automation

## 📈 **MONITORING**

### **Success Metrics**
- ✅ Articles processed successfully
- ✅ Processing time under 5 seconds
- ✅ No validation errors
- ✅ Slack notifications sent

### **Error Tracking**
- ❌ Validation failures
- ❌ Network timeouts
- ❌ Server errors
- ❌ Data quality issues

## 🔐 **SECURITY**

### **Best Practices**
1. **Validate Input**: All data is validated before processing
2. **Error Handling**: No sensitive data in error messages
3. **Rate Limiting**: Built-in retry logic prevents spam
4. **Logging**: Comprehensive audit trail

### **Configuration Security**
- Store webhook URLs securely
- Use environment variables for sensitive data
- Validate all input data
- Monitor for unusual activity

---

**This webhook script is the perfect bridge between Airtable and our news automation system!** 🚀

It provides comprehensive validation, detailed logging, and reliable delivery of news data to our automation system. 