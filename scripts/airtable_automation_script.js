// Airtable Automation Script: Express Entry Draw Webhook Sender
// ===========================================================
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
const WEBHOOK_URL = `https://api.github.com/repos/${GITHUB_REPO}/dispatches`;

// Main function for Airtable automation
async function sendDrawWebhook(record) {
    try {
        console.log("🔄 Processing Express Entry draw from Airtable...");
        
        // Debug: Check if record exists
        if (!record) {
            throw new Error("Record is undefined - check Airtable automation setup");
        }
        
        console.log("📊 Record object:", record);
        console.log("📊 Record keys:", Object.keys(record));
        
        // Extract data from Airtable record
        // UPDATE THESE FIELD NAMES to match your Airtable field names
        const drawData = {
            Program: record.getCellValue('Program'),           // Your Airtable field name
            draw_date: record.getCellValue('Draw Date'),       // Your Airtable field name
            Score: record.getCellValue('CRS Score'),           // Your Airtable field name
            Invitation: record.getCellValue('ITAs Issued'),    // Your Airtable field name
            Draw_Number: record.getCellValue('Draw Number'),   // Your Airtable field name
            Category: record.getCellValue('Category') || "General",
            Region: record.getCellValue('Region') || "All"
        };
        
        console.log("📊 Extracted draw data:", drawData);
        
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
        console.error("❌ Error sending webhook:", error.message);
        return { 
            success: false, 
            error: error.message 
        };
    }
}

// Execute the function with the current record
// This is what Airtable will run when the automation triggers
return await sendDrawWebhook(input.config().record); 