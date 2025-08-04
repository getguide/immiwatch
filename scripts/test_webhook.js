/**
 * Test Script for Airtable Webhook
 * Demonstrates the webhook functionality with sample data
 */

// Import the webhook processor
const { handleAirtableWebhook, CONFIG } = require('./airtable_webhook_script.js');

// Test data samples
const testCases = [
    {
        name: "Express Entry Draw",
        data: {
            record: {
                fields: {
                    'Headline': 'Express Entry Draw #348: 2,500 ITAs with 485 CRS',
                    'Summary': 'IRCC conducted Express Entry draw #348, issuing 2,500 ITAs with a CRS cutoff of 485 points. This draw targeted all Express Entry candidates.',
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
        }
    },
    {
        name: "Policy Announcement",
        data: {
            record: {
                fields: {
                    'Headline': 'New Express Entry Policy Changes Effective September 1',
                    'Summary': 'IRCC announces significant changes to Express Entry system including new scoring criteria and processing improvements for all applicants.',
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
        }
    },
    {
        name: "Legal Decision",
        data: {
            record: {
                fields: {
                    'Headline': 'Federal Court Rules on Study Permit Renewal Process',
                    'Summary': 'Federal Court issues important decision affecting study permit renewal procedures and eligibility criteria for international students.',
                    'Program Affected': ['Study Permit'],
                    'Impact': 'moderate',
                    'Urgency Level': 'informational',
                    'Week of Year': 31,
                    'Date of Update': '2025-07-29',
                    'Source URL': 'https://decisions.fct-cf.gc.ca/fc-cf/decisions/en/item/123456/index.do',
                    'Source': 'Federal Court',
                    'Category': 'legal'
                }
            }
        }
    },
    {
        name: "System Update",
        data: {
            record: {
                fields: {
                    'Headline': 'IRCC Portal Maintenance Scheduled for August 15',
                    'Summary': 'IRCC announces scheduled maintenance for the online portal affecting all immigration applications and document uploads.',
                    'Program Affected': ['Express Entry', 'Work Permit', 'Study Permit'],
                    'Impact': 'low',
                    'Urgency Level': 'informational',
                    'Week of Year': 31,
                    'Date of Update': '2025-07-29',
                    'Source URL': 'https://ircc.gc.ca/english/helpcentre/notices.asp',
                    'Source': 'IRCC',
                    'Category': 'systems'
                }
            }
        }
    },
    {
        name: "Invalid Data Test",
        data: {
            record: {
                fields: {
                    'Headline': '', // Missing required field
                    'Summary': 'This should fail validation',
                    'Category': 'invalid_category', // Invalid category
                    'Impact': 'invalid_impact', // Invalid impact
                    'Date of Update': 'invalid-date' // Invalid date format
                }
            }
        }
    }
];

/**
 * Run all test cases
 */
async function runTests() {
    console.log('🧪 Starting Airtable Webhook Tests\n');
    
    for (const testCase of testCases) {
        console.log(`\n📋 Testing: ${testCase.name}`);
        console.log('─'.repeat(50));
        
        try {
            const startTime = Date.now();
            const result = await handleAirtableWebhook(testCase.data);
            const processingTime = Date.now() - startTime;
            
            console.log(`⏱️  Processing Time: ${processingTime}ms`);
            console.log(`✅ Success: ${result.success}`);
            
            if (result.success) {
                console.log(`📰 Article: ${result.articleUrl || 'N/A'}`);
                if (result.warnings && result.warnings.length > 0) {
                    console.log(`⚠️  Warnings: ${result.warnings.join(', ')}`);
                }
            } else {
                console.log(`❌ Errors: ${result.errors ? result.errors.join(', ') : result.error}`);
            }
            
        } catch (error) {
            console.log(`💥 Test failed: ${error.message}`);
        }
        
        console.log('─'.repeat(50));
    }
    
    console.log('\n🎉 All tests completed!');
}

/**
 * Test specific functionality
 */
async function testValidation() {
    console.log('🔍 Testing Data Validation\n');
    
    const validator = new (require('./airtable_webhook_script.js').DataValidator)(
        new (require('./airtable_webhook_script.js').Logger)('DEBUG')
    );
    
    const testData = {
        headline: 'Test Article',
        summary: 'Test summary',
        category: 'draws',
        impact: 'high',
        date_of_update: '2025-07-29',
        cutoff: 485,
        invitation: 2500
    };
    
    const validation = validator.validateRecord(testData);
    console.log('Validation Result:', validation);
}

/**
 * Test Slack notifications
 */
async function testSlackNotifications() {
    console.log('🔔 Testing Slack Notifications\n');
    
    const notifier = new (require('./airtable_webhook_script.js').SlackNotifier)(
        CONFIG.SLACK_WEBHOOK_URL,
        new (require('./airtable_webhook_script.js').Logger)('INFO')
    );
    
    await notifier.sendNotification('🧪 Test notification from ImmiWatch webhook script');
    console.log('Slack notification test completed');
}

// Main execution
if (require.main === module) {
    const command = process.argv[2];
    
    switch (command) {
        case 'validation':
            testValidation();
            break;
        case 'slack':
            testSlackNotifications();
            break;
        case 'all':
        default:
            runTests();
            break;
    }
}

module.exports = {
    runTests,
    testValidation,
    testSlackNotifications,
    testCases
}; 