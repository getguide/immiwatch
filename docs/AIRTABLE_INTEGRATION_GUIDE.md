# 🔗 Airtable Integration Guide

## Overview
This guide explains how to set up Airtable automation to send Express Entry draw data to the ImmiWatch GitHub repository via webhooks.

## Prerequisites

### 1. GitHub Token Setup
1. Go to **GitHub.com** → Click your **profile picture** (top right)
2. Click **Settings**
3. Scroll down to **Developer settings** (bottom left)
4. Click **Personal access tokens**
5. Click **Tokens (classic)**
6. Click **Generate new token (classic)**
7. Give it a name: `"Airtable Webhook Token"`
8. Set **Expiration**: Choose `No expiration` or `90 days`
9. **Set EXACT Permissions:**
   - ✅ **repo** (Full control of private repositories)
   - ✅ **workflow** (Update GitHub Action workflows)
10. Click **Generate token**
11. **Copy the token immediately** (you won't see it again!)

### 2. Airtable Setup
1. Create a table with these fields:
   - `Program` (Single select: EE-PNP, EE-CEC, EE-FSW, EE-FST, EE-Health, EE-French, EE-Trade, EE-Education, EE-Agriculture, EE-STEM)
   - `Draw Date` (Date)
   - `CRS Score` (Number)
   - `ITAs Issued` (Number)
   - `Draw Number` (Number)
   - `Category` (Single select: General, Healthcare, STEM, Trade, etc.)
   - `Region` (Single select: All, Ontario, BC, etc.)

## Working Script

**Copy and paste this script into your Airtable automation:**

```javascript
// Final Working Airtable Automation Script for Express Entry Draws
// ======================================================

// Configuration - UPDATE THIS TOKEN
const GITHUB_TOKEN = "YOUR_NEW_TOKEN_HERE"; // Replace with your new token
const GITHUB_REPO = "getguide/immiwatch";
const WEBHOOK_URL = `https://api.github.com/repos/${GITHUB_REPO}/dispatches`;

// Main function for Airtable automation
async function sendDrawWebhook() {
    try {
        console.log("🔄 Processing Express Entry draw from Airtable...");
        
        // Get the config object which contains the record data
        const config = input.config();
        console.log("📊 Config object:", config);
        
        // Extract data directly from the config object
        const drawData = {
            Program: config.Program,
            draw_date: config['Draw Date'],
            Score: config['CRS Score'],
            Invitation: config['ITAs Issued'],
            Draw_Number: config['Draw Number'],
            Category: config.Category || "General",
            Region: config.Region || "All"
        };
        
        console.log("📊 Extracted draw data:", drawData);
        
        return await processDrawData(drawData);
        
    } catch (error) {
        console.error("❌ Error sending webhook:", error.message);
        return { 
            success: false, 
            error: error.message 
        };
    }
}

// Process draw data and send webhook
async function processDrawData(drawData) {
    try {
        // Validate required fields
        const requiredFields = ['Program', 'draw_date', 'Score', 'Invitation', 'Draw_Number'];
        for (const field of requiredFields) {
            if (!drawData[field]) {
                throw new Error(`Missing required field: ${field}`);
            }
        }
        
        // Format webhook payload for our system
        const webhookPayload = {
            body: {
                Program: drawData.Program,
                Category: drawData.Category,
                Region: drawData.Region,
                "draw.date.most.recent": drawData.draw_date,
                Score: parseInt(drawData.Score),
                "Scoring System": "CRS",
                "Filter by program": "Express Entry",
                Invitation: parseInt(drawData.Invitation),
                "Last Checked": new Date().toISOString(),
                "Draw Number": parseInt(drawData.Draw_Number)
            }
        };
        
        console.log("📄 Formatted webhook payload:", JSON.stringify(webhookPayload, null, 2));
        
        // Send webhook to GitHub
        const payload = {
            event_type: "express_entry_draw",
            client_payload: webhookPayload.body
        };
        
        const response = await fetch(WEBHOOK_URL, {
            method: 'POST',
            headers: {
                'Authorization': `token ${GITHUB_TOKEN}`,
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`GitHub API error: ${response.status} - ${errorText}`);
        }
        
        console.log(`✅ Webhook sent successfully for Draw #${drawData.Draw_Number}`);
        console.log(`🎯 Program: ${drawData.Program}`);
        console.log(`📅 Date: ${drawData.draw_date}`);
        console.log(`📈 ITAs: ${drawData.Invitation}`);
        console.log(`🎯 CRS: ${drawData.Score}`);
        
        return { 
            success: true, 
            draw_number: drawData.Draw_Number,
            program: drawData.Program,
            message: "Webhook sent successfully"
        };
        
    } catch (error) {
        console.error("❌ Error processing draw data:", error.message);
        return { 
            success: false, 
            error: error.message 
        };
    }
}

// Execute the function
return await sendDrawWebhook();
```

## Airtable Automation Setup

### 1. Create Automation
1. In your Airtable base, click **Automations** (top right)
2. Click **Create a custom automation**
3. Choose **When a record is created** or **When a record is updated**
4. Select your table
5. Add **Run a script** action
6. Paste the script above

### 2. Configure the Script
1. Replace `YOUR_NEW_TOKEN_HERE` with your GitHub token
2. Update field names if they don't match your Airtable fields
3. Test with a sample record

## Supported Program Values

| Program | Type | Description |
|---------|------|-------------|
| EE-PNP | Program-based | Provincial Nominee Program |
| EE-CEC | Program-based | Canadian Experience Class |
| EE-FSW | Program-based | Federal Skilled Worker |
| EE-FST | Program-based | Federal Skilled Trades |
| EE-Health | Category-based | Healthcare workers |
| EE-French | Category-based | French-speaking candidates |
| EE-Trade | Category-based | Skilled trades |
| EE-Education | Category-based | Education workers |
| EE-Agriculture | Category-based | Agriculture workers |
| EE-STEM | Category-based | STEM professionals |

## Expected Output

When successful, you should see:
```
🔄 Processing Express Entry draw from Airtable...
📊 Config object: {Program: "EE-PNP", Draw Date: "2025-06-02", ...}
📊 Extracted draw data: {Program: "EE-PNP", draw_date: "2025-06-02", ...}
📄 Formatted webhook payload: {...}
✅ Webhook sent successfully for Draw #348
🎯 Program: EE-PNP
📅 Date: 2025-06-02
📈 ITAs: 277
🎯 CRS: 726
```

## Troubleshooting

### Common Issues

1. **"Resource not accessible by personal access token"**
   - Ensure your GitHub token has `repo` and `workflow` permissions
   - Create a new token with the correct permissions

2. **"Missing required field"**
   - Check that all required fields are filled in your Airtable record
   - Verify field names match exactly

3. **"Config object is empty"**
   - Ensure your automation is triggered by the correct table
   - Check that the record has data in all required fields

### Debug Steps

1. Check the console output in Airtable
2. Verify GitHub token permissions
3. Test with a simple record first
4. Check GitHub Actions logs for webhook processing

## Security Best Practices

1. **Token Security**
   - Use environment variables when possible
   - Rotate tokens regularly
   - Never share tokens publicly

2. **Data Validation**
   - Always validate input data
   - Sanitize user inputs
   - Handle errors gracefully

3. **Monitoring**
   - Monitor webhook delivery status
   - Set up alerts for failures
   - Log all automation runs

## Integration with GitHub Actions

The webhook triggers the GitHub Actions workflow in `.github/workflows/webhook_handler.yml`, which:

1. Receives the webhook data
2. Validates the draw information
3. Updates the current monthly Express Entry report
4. Commits and pushes changes to the repository

## Support

For issues or questions:
1. Check the console output in Airtable
2. Review GitHub Actions logs
3. Verify token permissions
4. Test with sample data first 