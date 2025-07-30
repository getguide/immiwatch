/**
 * Airtable Script: Express Entry Draw Webhook Sender
 * =================================================
 * 
 * This script processes Express Entry draw data from Airtable and sends it
 * to our webhook system for automatic monthly report updates.
 * 
 * Usage: Copy and paste this script into Airtable's Scripting app
 * 
 * Prerequisites:
 * - Airtable Scripting app enabled
 * - GitHub personal access token with repo permissions
 * - Repository: getguide/immiwatch
 */

// Configuration - Update these values
const GITHUB_TOKEN = "your_github_token_here"; // Replace with your actual token
const GITHUB_REPO = "getguide/immiwatch";
const WEBHOOK_URL = `https://api.github.com/repos/${GITHUB_REPO}/dispatches`;

/**
 * Main function to process draw data and send webhook
 * @param {Object} drawData - The draw data from Airtable
 */
async function processDrawAndSendWebhook(drawData) {
    try {
        console.log("🔄 Processing draw data...");
        
        // Validate required fields
        const requiredFields = ['Program', 'draw_date', 'Score', 'Invitation', 'Draw_Number'];
        for (const field of requiredFields) {
            if (!drawData[field]) {
                throw new Error(`Missing required field: ${field}`);
            }
        }
        
        // Format the webhook payload
        const webhookPayload = formatWebhookPayload(drawData);
        
        // Send webhook to GitHub
        const response = await sendWebhookToGitHub(webhookPayload);
        
        console.log("✅ Webhook sent successfully!");
        console.log(`📊 Draw #${drawData.Draw_Number} processed`);
        console.log(`🎯 Program: ${drawData.Program}`);
        console.log(`📅 Date: ${drawData.draw_date}`);
        console.log(`📈 ITAs: ${drawData.Invitation}`);
        console.log(`🎯 CRS: ${drawData.Score}`);
        
        return {
            success: true,
            message: "Webhook sent successfully",
            draw_number: drawData.Draw_Number,
            program: drawData.Program
        };
        
    } catch (error) {
        console.error("❌ Error processing draw:", error.message);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Format draw data into webhook payload
 * @param {Object} drawData - Raw draw data from Airtable
 * @returns {Object} Formatted webhook payload
 */
function formatWebhookPayload(drawData) {
    // Map Airtable field names to webhook format
    const webhookData = {
        body: {
            Program: drawData.Program,
            Category: drawData.Category || "General",
            Region: drawData.Region || "All",
            "draw.date.most.recent": drawData.draw_date,
            Score: parseInt(drawData.Score),
            "Scoring System": "CRS",
            "Filter by program": "Express Entry",
            Invitation: parseInt(drawData.Invitation),
            "Last Checked": new Date().toISOString(),
            "Draw Number": parseInt(drawData.Draw_Number)
        }
    };
    
    console.log("📄 Formatted webhook data:", JSON.stringify(webhookData, null, 2));
    return webhookData;
}

/**
 * Send webhook to GitHub repository
 * @param {Object} webhookData - The webhook payload
 * @returns {Object} Response from GitHub API
 */
async function sendWebhookToGitHub(webhookData) {
    const payload = {
        event_type: "express_entry_draw",
        client_payload: webhookData.body
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
    
    return await response.json();
}

/**
 * Example usage function - Replace with your actual Airtable data
 * This function shows how to map your Airtable fields to the webhook
 */
function exampleUsage() {
    // Example: Your Airtable data structure
    const airtableDrawData = {
        Program: "EE-PNP",           // From your Airtable field
        draw_date: "2025-08-05",     // From your Airtable field
        Score: 726,                   // From your Airtable field
        Invitation: 277,              // From your Airtable field
        Draw_Number: 348,             // From your Airtable field
        Category: "General",          // Optional
        Region: "All"                 // Optional
    };
    
    // Process the draw data
    return processDrawAndSendWebhook(airtableDrawData);
}

/**
 * Airtable Integration Functions
 * =============================
 * 
 * Use these functions to integrate with your Airtable automation
 */

/**
 * Process draw from Airtable record
 * @param {Object} record - Airtable record object
 */
async function processAirtableRecord(record) {
    // Extract data from Airtable record
    const drawData = {
        Program: record.getCellValue('Program'),
        draw_date: record.getCellValue('Draw Date'),
        Score: record.getCellValue('CRS Score'),
        Invitation: record.getCellValue('ITAs Issued'),
        Draw_Number: record.getCellValue('Draw Number'),
        Category: record.getCellValue('Category') || "General",
        Region: record.getCellValue('Region') || "All"
    };
    
    return await processDrawAndSendWebhook(drawData);
}

/**
 * Process multiple draws from Airtable records
 * @param {Array} records - Array of Airtable record objects
 */
async function processMultipleDraws(records) {
    const results = [];
    
    for (const record of records) {
        try {
            const result = await processAirtableRecord(record);
            results.push(result);
            
            // Add delay between requests to avoid rate limiting
            await new Promise(resolve => setTimeout(resolve, 1000));
            
        } catch (error) {
            console.error(`❌ Error processing record:`, error);
            results.push({
                success: false,
                error: error.message
            });
        }
    }
    
    return results;
}

/**
 * Airtable Automation Integration
 * ===============================
 * 
 * Copy and paste this section into your Airtable automation
 */

// Airtable Automation Script Template
const AIRTABLE_AUTOMATION_SCRIPT = `
// Airtable Automation: Express Entry Draw Webhook Sender
// =====================================================

// Configuration
const GITHUB_TOKEN = "your_github_token_here"; // Replace with your token
const GITHUB_REPO = "getguide/immiwatch";
const WEBHOOK_URL = \`https://api.github.com/repos/\${GITHUB_REPO}/dispatches\`;

// Main function for Airtable automation
async function sendDrawWebhook(record) {
    try {
        // Extract data from Airtable record
        const drawData = {
            Program: record.getCellValue('Program'),
            draw_date: record.getCellValue('Draw Date'),
            Score: record.getCellValue('CRS Score'),
            Invitation: record.getCellValue('ITAs Issued'),
            Draw_Number: record.getCellValue('Draw Number'),
            Category: record.getCellValue('Category') || "General",
            Region: record.getCellValue('Region') || "All"
        };
        
        // Validate required fields
        const requiredFields = ['Program', 'draw_date', 'Score', 'Invitation', 'Draw_Number'];
        for (const field of requiredFields) {
            if (!drawData[field]) {
                throw new Error(\`Missing required field: \${field}\`);
            }
        }
        
        // Format webhook payload
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
        
        // Send webhook to GitHub
        const payload = {
            event_type: "express_entry_draw",
            client_payload: webhookPayload.body
        };
        
        const response = await fetch(WEBHOOK_URL, {
            method: 'POST',
            headers: {
                'Authorization': \`token \${GITHUB_TOKEN}\`,
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(\`GitHub API error: \${response.status} - \${errorText}\`);
        }
        
        console.log(\`✅ Webhook sent successfully for Draw #\${drawData.Draw_Number}\`);
        return { success: true, draw_number: drawData.Draw_Number };
        
    } catch (error) {
        console.error("❌ Error sending webhook:", error.message);
        return { success: false, error: error.message };
    }
}

// Execute the function with the current record
return await sendDrawWebhook(input.config().record);
`;

/**
 * Field Mapping Guide
 * ===================
 * 
 * Map your Airtable fields to the webhook format:
 * 
 * Airtable Field Name → Webhook Field
 * -----------------------------------
 * Program → body.Program
 * Draw Date → body.draw.date.most.recent
 * CRS Score → body.Score
 * ITAs Issued → body.Invitation
 * Draw Number → body.Draw Number
 * Category → body.Category (optional)
 * Region → body.Region (optional)
 * 
 * Supported Program Values:
 * -------------------------
 * Program-Based: EE-PNP, EE-CEC, EE-FSW, EE-FST
 * Category-Based: EE-Health, EE-French, EE-Trade, EE-Education, EE-Agriculture, EE-STEM
 */

// Export functions for use in Airtable
module.exports = {
    processDrawAndSendWebhook,
    processAirtableRecord,
    processMultipleDraws,
    AIRTABLE_AUTOMATION_SCRIPT
}; 