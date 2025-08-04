// Airtable Automation: News Article Webhook Sender
// ================================================
// 
// Copy and paste this entire script into your Airtable automation
// 
// Prerequisites:
// 1. Replace "your_github_token_here" with your actual GitHub token
// 2. Ensure your Airtable fields match the field names below
// 3. Make sure your GitHub token has repo permissions

// Configuration - UPDATE THIS TOKEN
const GITHUB_TOKEN = "your_github_token_here"; // Replace with your actual token
const GITHUB_REPO = "getguide/immiwatch";
const WEBHOOK_URL = "https://api.github.com/repos/" + GITHUB_REPO + "/dispatches";

// Main function for Airtable automation
async function sendNewsWebhook(record) {
    try {
        console.log("🔄 Processing news article from Airtable...");
        
        // Debug: Check if record exists
        if (!record) {
            throw new Error("Record is undefined - check Airtable automation setup");
        }
        
        console.log("📊 Record object:", record);
        console.log("📊 Record keys:", Object.keys(record));
        
        // Extract data from Airtable record
        // UPDATE THESE FIELD NAMES to match your Airtable field names
        const newsData = {
            headline: record.getCellValue('Headline'),
            summary: record.getCellValue('Summary'),
            program_affected: record.getCellValue('Program Affected'),
            impact: record.getCellValue('Impact'),
            urgency_level: record.getCellValue('Urgency Level'),
            week_of_year: record.getCellValue('Week of Year'),
            date_of_update: record.getCellValue('Date of Update'),
            source_url: record.getCellValue('Source URL'),
            source: record.getCellValue('Source'),
            category: record.getCellValue('Category'),
            cutoff: record.getCellValue('Cutoff'),
            invitation: record.getCellValue('Invitation')
        };
        
        console.log("📊 Extracted news data:", newsData);
        
        // Validate required fields
        const requiredFields = ['headline', 'summary', 'date_of_update', 'category', 'impact'];
        for (const field of requiredFields) {
            if (!newsData[field] || newsData[field].toString().trim() === '') {
                throw new Error("Missing required field: " + field);
            }
        }
        
        // Validate category
        const validCategories = ['policy', 'draws', 'legal', 'systems', 'programs', 'documents', 'analysis', 'other'];
        if (newsData.category && !validCategories.includes(newsData.category.toLowerCase())) {
            throw new Error("Invalid category: " + newsData.category + ". Valid categories: " + validCategories.join(', '));
        }
        
        // Validate impact level
        const validImpactLevels = ['critical', 'high', 'moderate', 'low', 'informational'];
        if (newsData.impact && !validImpactLevels.includes(newsData.impact.toLowerCase())) {
            throw new Error("Invalid impact level: " + newsData.impact + ". Valid levels: " + validImpactLevels.join(', '));
        }
        
        // Validate date format
        if (newsData.date_of_update) {
            const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
            if (!dateRegex.test(newsData.date_of_update)) {
                throw new Error("Invalid date format: " + newsData.date_of_update + ". Expected format: YYYY-MM-DD");
            }
        }
        
        // Clean and normalize data
        const cleanedData = {};
        for (const [key, value] of Object.entries(newsData)) {
            if (value !== null && value !== undefined) {
                if (typeof value === 'string') {
                    cleanedData[key] = value.trim();
                } else if (Array.isArray(value)) {
                    cleanedData[key] = value.filter(item => item && item.toString().trim() !== '');
                } else {
                    cleanedData[key] = value;
                }
            }
        }
        
        // Normalize category and impact to lowercase
        if (cleanedData.category) {
            cleanedData.category = cleanedData.category.toLowerCase();
        }
        if (cleanedData.impact) {
            cleanedData.impact = cleanedData.impact.toLowerCase();
        }
        
        // Convert numeric fields
        if (cleanedData.cutoff) {
            cleanedData.cutoff = parseInt(cleanedData.cutoff);
        }
        if (cleanedData.invitation) {
            cleanedData.invitation = parseInt(cleanedData.invitation);
        }
        if (cleanedData.week_of_year) {
            cleanedData.week_of_year = parseInt(cleanedData.week_of_year);
        }
        
        console.log("📄 Formatted news data:", JSON.stringify(cleanedData));
        
        // Send webhook to GitHub Repository Dispatch
        const payload = {
            event_type: "news_article",
            client_payload: cleanedData
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
            throw new Error("GitHub API error: " + response.status + " - " + errorText);
        }
        
        console.log("✅ News webhook sent successfully!");
        console.log("📰 Headline: " + cleanedData.headline);
        console.log("📅 Date: " + cleanedData.date_of_update);
        console.log("🏷️ Category: " + cleanedData.category);
        console.log("⚡ Impact: " + cleanedData.impact);
        
        return { 
            success: true, 
            headline: cleanedData.headline,
            category: cleanedData.category,
            message: "News webhook sent successfully"
        };
        
    } catch (error) {
        console.error("❌ Error sending news webhook:", error.message);
        return {
            success: false,
            error: error.message
        };
    }
}

// Execute the function with the current record
return await sendNewsWebhook(input.config().record); 