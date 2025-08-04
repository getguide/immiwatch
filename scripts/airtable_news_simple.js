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
async function sendNewsWebhook() {
    try {
        console.log("🔄 Processing news article from Airtable...");
        
        // Access mapped values directly from input.config()
        const config = input.config();
        console.log("📊 Config object:", config);
        console.log("📊 Config keys:", Object.keys(config));
        
        // Extract data from mapped input variables
        // These should match your Airtable automation input variable names exactly
        const newsData = {
            headline: config.Headline,
            summary: config.Summary,
            program_affected: config['Program Affected'],
            impact: config.Impact,
            urgency_level: config['Urgency Level'],
            week_of_year: config['Week of Year'],
            date_of_update: config['Date of Update'],
            source_url: config['Source URL'],
            source: config.Source,
            category: config.Category,
            cutoff: config.Cutoff,
            invitation: config.Invitation
        };
        
        console.log("📊 Extracted news data:", newsData);
        
        // Validate required fields
        const requiredFields = ['headline', 'summary', 'date_of_update', 'category', 'impact'];
        for (const field of requiredFields) {
            if (!newsData[field] || newsData[field].toString().trim() === '') {
                throw new Error("Missing required field: " + field);
            }
        }
        
        // Category mapping function
        function mapCategory(airtableCategory) {
            const categoryMap = {
                'Policy Announcement': 'policy-announcements',
                'Program Delivery Update': 'program-delivery',
                'Invitation Round': 'invitation-rounds',
                'ATIP Insight / Internal Docs': 'atip-insights',
                'Legal Decision / Jurisprudence': 'legal-decisions',
                'System / Portal Notice': 'system-notices',
                'Form / Document Change': 'form-changes',
                'Deadline / Expiry Alert': 'deadline-alerts',
                'Statistical / Trend Report': 'statistical-reports',
                'Scam / Fraud Alert': 'scam-alerts',
                'Other': 'other'
            };
            
            return categoryMap[airtableCategory] || 'other';
        }
        
        // Map the category to our system format
        if (newsData.category) {
            newsData.category = mapCategory(newsData.category);
        }
        
        // Validate category (now using our mapped categories)
        const validCategories = ['policy-announcements', 'program-delivery', 'invitation-rounds', 'atip-insights', 'legal-decisions', 'system-notices', 'form-changes', 'deadline-alerts', 'statistical-reports', 'scam-alerts', 'other'];
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
        
                            // Clean and normalize data - only include essential fields for GitHub API limit
                    const cleanedData = {
                        headline: newsData.headline ? newsData.headline.trim() : '',
                        summary: newsData.summary ? newsData.summary.trim() : '',
                        date_of_update: newsData.date_of_update ? newsData.date_of_update.trim() : '',
                        category: newsData.category ? newsData.category.toLowerCase() : '',
                        impact: newsData.impact ? newsData.impact.toLowerCase() : '',
                        source: newsData.source ? newsData.source.trim() : '',
                        source_url: newsData.source_url ? newsData.source_url.trim() : '',
                        program_affected: Array.isArray(newsData.program_affected) ? newsData.program_affected.filter(item => item && item.toString().trim() !== '') : [],
                        urgency_level: newsData.urgency_level ? newsData.urgency_level.trim() : '',
                        week_of_year: newsData.week_of_year ? parseInt(newsData.week_of_year) : null
                    };
        
                            // Add cutoff and invitation if they exist (for invitation rounds)
                    if (newsData.cutoff && newsData.cutoff.toString().trim() !== '') {
                        cleanedData.cutoff = parseInt(newsData.cutoff);
                    }
                    if (newsData.invitation && newsData.invitation.toString().trim() !== '') {
                        cleanedData.invitation = parseInt(newsData.invitation);
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

// Execute the function without parameters
// This is what Airtable will run when the automation triggers
return await sendNewsWebhook(); 