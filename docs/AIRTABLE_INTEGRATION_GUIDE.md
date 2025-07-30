# 🔗 Airtable Integration Guide

## 🎯 **Overview**

This guide shows you how to set up Airtable automation to send Express Entry draw data to our webhook system for automatic monthly report updates.

## 📋 **Prerequisites**

### **1. GitHub Token Setup**
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Create a new token with `repo` permissions
3. Copy the token (you'll need it for the script)

### **2. Airtable Setup**
1. Enable Airtable Scripting app in your workspace
2. Create a table with the required fields (see field mapping below)
3. Set up automation trigger (when new record is created)

## 🔧 **Step-by-Step Setup**

### **Step 1: Create Airtable Table**

Create a table with these fields:

| Field Name | Type | Required | Example |
|------------|------|----------|---------|
| Program | Single select | ✅ | EE-PNP, EE-CEC, EE-Health |
| Draw Date | Date | ✅ | 2025-08-05 |
| CRS Score | Number | ✅ | 726 |
| ITAs Issued | Number | ✅ | 277 |
| Draw Number | Number | ✅ | 348 |
| Category | Single select | ❌ | General |
| Region | Single select | ❌ | All |

### **Step 2: Set Up Automation**

1. **Go to Automations** in your Airtable workspace
2. **Create new automation**
3. **Trigger**: "When a record is created" (or your preferred trigger)
4. **Action**: "Run a script"
5. **Copy the script** from `scripts/airtable_automation_script.js`

### **Step 3: Configure the Script**

1. **Replace the GitHub token**:
   ```javascript
   const GITHUB_TOKEN = "your_actual_github_token_here";
   ```

2. **Update field names** to match your Airtable fields:
   ```javascript
   const drawData = {
       Program: record.getCellValue('Your Program Field Name'),
       draw_date: record.getCellValue('Your Draw Date Field Name'),
       Score: record.getCellValue('Your CRS Score Field Name'),
       Invitation: record.getCellValue('Your ITAs Issued Field Name'),
       Draw_Number: record.getCellValue('Your Draw Number Field Name'),
       // ... etc
   };
   ```

### **Step 4: Test the Integration**

1. **Create a test record** in your Airtable table
2. **Check the automation logs** for success/error messages
3. **Verify the webhook** was sent to GitHub
4. **Check the monthly report** was updated

## 📊 **Field Mapping**

### **Required Fields**
Your Airtable field names must map to these webhook fields:

| Airtable Field | Webhook Field | Description |
|----------------|---------------|-------------|
| Program | body.Program | Draw type (EE-PNP, EE-CEC, etc.) |
| Draw Date | body.draw.date.most.recent | Date of the draw (YYYY-MM-DD) |
| CRS Score | body.Score | CRS cutoff score |
| ITAs Issued | body.Invitation | Number of ITAs issued |
| Draw Number | body.Draw Number | Express Entry draw number |

### **Optional Fields**
| Airtable Field | Webhook Field | Description |
|----------------|---------------|-------------|
| Category | body.Category | Internal category (default: "General") |
| Region | body.Region | Internal region (default: "All") |

## 🎯 **Supported Program Values**

### **Program-Based Draws**
- `EE-PNP` → Updates PNP ITAs
- `EE-CEC` → Updates CEC ITAs
- `EE-FSW` → Updates FSW ITAs
- `EE-FST` → Updates FST ITAs

### **Category-Based Draws**
- `EE-Health` → Updates Healthcare ITAs
- `EE-French` → Updates French-Speaking ITAs
- `EE-Trade` → Updates Trade ITAs
- `EE-Education` → Updates Education ITAs
- `EE-Agriculture` → Updates Agriculture ITAs
- `EE-STEM` → Updates STEM ITAs

## 🔄 **Workflow Example**

### **When IRCC Announces a Draw**

1. **IRCC announces** new Express Entry draw
2. **Your Lambda function** detects the draw
3. **Lambda sends webhook** to Airtable (or you manually add)
4. **Airtable automation triggers** when new record is created
5. **Script processes** the Airtable data
6. **Script sends webhook** to our GitHub repository
7. **GitHub Actions processes** the webhook
8. **Monthly report updates** automatically
9. **Changes are committed** and pushed to live site

### **Example Airtable Record**
```
Program: EE-PNP
Draw Date: 2025-08-05
CRS Score: 726
ITAs Issued: 277
Draw Number: 348
Category: General
Region: All
```

### **Result**
- **Webhook sent** to GitHub
- **August 2025 report** updated with +277 PNP ITAs
- **Total August PNP** now shows accumulated total
- **Report live** within minutes

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **1. GitHub Token Error**
```
❌ Error: GitHub API error: 401 - Bad credentials
```
**Solution**: Check your GitHub token has `repo` permissions

#### **2. Missing Field Error**
```
❌ Error: Missing required field: Program
```
**Solution**: Check your Airtable field names match the script

#### **3. Invalid Program Value**
```
❌ Error: Invalid program value: EE-PNP-INVALID
```
**Solution**: Use only supported program values (EE-PNP, EE-CEC, etc.)

#### **4. Date Format Error**
```
❌ Error: Invalid date format: 05/08/2025
```
**Solution**: Use YYYY-MM-DD format in Airtable

### **Testing Steps**

1. **Test with sample data**:
   ```javascript
   // Add this to your script for testing
   const testData = {
       Program: "EE-PNP",
       draw_date: "2025-08-05",
       Score: 726,
       Invitation: 277,
       Draw_Number: 348
   };
   ```

2. **Check automation logs** in Airtable
3. **Verify GitHub Actions** ran successfully
4. **Check monthly report** was updated

## 📈 **Monitoring**

### **Success Indicators**
- ✅ **Airtable automation** runs without errors
- ✅ **GitHub Actions** workflow completes successfully
- ✅ **Monthly report** shows updated totals
- ✅ **Git commit** created with draw information

### **Log Messages to Look For**
```
🔄 Processing Express Entry draw from Airtable...
📊 Extracted draw data: {Program: "EE-PNP", ...}
📄 Formatted webhook payload: {...}
✅ Webhook sent successfully for Draw #348
🎯 Program: EE-PNP
📅 Date: 2025-08-05
📈 ITAs: 277
🎯 CRS: 726
```

## 🔒 **Security**

### **Token Security**
- ✅ **Store token securely** in Airtable environment variables
- ✅ **Use minimal permissions** (repo scope only)
- ✅ **Rotate tokens** regularly
- ✅ **Monitor token usage** in GitHub

### **Data Validation**
- ✅ **Validate all fields** before sending
- ✅ **Check data types** (numbers, dates)
- ✅ **Sanitize input** to prevent injection
- ✅ **Log all activities** for audit trail

## 🚀 **Advanced Features**

### **Batch Processing**
If you need to process multiple draws at once:

```javascript
// Process multiple records
async function processMultipleDraws(records) {
    const results = [];
    for (const record of records) {
        const result = await sendDrawWebhook(record);
        results.push(result);
        // Add delay to avoid rate limiting
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    return results;
}
```

### **Error Handling**
```javascript
// Enhanced error handling
try {
    const result = await sendDrawWebhook(record);
    if (result.success) {
        console.log("✅ Success:", result.message);
    } else {
        console.error("❌ Failed:", result.error);
        // Send notification or retry
    }
} catch (error) {
    console.error("💥 Critical error:", error);
    // Handle critical failures
}
```

## 📞 **Support**

### **Getting Help**
1. **Check automation logs** in Airtable
2. **Verify GitHub Actions** workflow status
3. **Test with sample data** using the test script
4. **Check field mapping** matches your Airtable setup

### **Common Questions**
- **Q**: "Why isn't my automation triggering?"
- **A**: Check trigger conditions and field values

- **Q**: "Why is the webhook failing?"
- **A**: Verify GitHub token and field names

- **Q**: "Why isn't the report updating?"
- **A**: Check GitHub Actions workflow and logs

---

**Last Updated**: July 2025  
**Maintained By**: ImmiWatch Development Team  
**Version**: 1.0 