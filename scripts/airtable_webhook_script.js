/**
 * ImmiWatch Airtable Webhook Script
 * The Bridge Between Airtable and News Automation System
 * 
 * This script processes Airtable records and sends them to our news automation system
 * with comprehensive logging, error handling, and data validation.
 */

// Configuration
const CONFIG = {
    // Webhook endpoint for our automation system
    // UPDATE THIS URL to your actual webhook handler URL
    AUTOMATION_WEBHOOK_URL: 'https://your-webhook-server.com/webhook/news',
    
    // Webhook secret for security (generate a secure random key)
    // UPDATE THIS SECRET to a secure random string
    WEBHOOK_SECRET: 'your-secure-webhook-secret-here',
    
    // Slack webhook for notifications (optional)
    SLACK_WEBHOOK_URL: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK',
    
    // Logging configuration
    LOG_LEVEL: 'INFO', // DEBUG, INFO, WARN, ERROR
    
    // Retry configuration
    MAX_RETRIES: 3,
    RETRY_DELAY: 2000, // milliseconds
    
    // Validation rules
    REQUIRED_FIELDS: ['headline', 'summary', 'date_of_update', 'category', 'impact'],
    VALID_CATEGORIES: ['policy', 'draws', 'legal', 'systems', 'programs', 'documents', 'analysis', 'other'],
    VALID_IMPACT_LEVELS: ['critical', 'high', 'moderate', 'low', 'informational']
};

/**
 * Logger class for comprehensive logging
 */
class Logger {
    constructor(level = 'INFO') {
        this.level = level;
        this.levels = { DEBUG: 0, INFO: 1, WARN: 2, ERROR: 3 };
    }
    
    log(level, message, data = null) {
        if (this.levels[level] >= this.levels[this.level]) {
            const timestamp = new Date().toISOString();
            const logEntry = {
                timestamp,
                level,
                message,
                data: data ? JSON.stringify(data, null, 2) : null
            };
            
            console.log(`[${timestamp}] ${level}: ${message}`);
            if (data) {
                console.log(`Data: ${JSON.stringify(data, null, 2)}`);
            }
        }
    }
    
    debug(message, data = null) { this.log('DEBUG', message, data); }
    info(message, data = null) { this.log('INFO', message, data); }
    warn(message, data = null) { this.log('WARN', message, data); }
    error(message, data = null) { this.log('ERROR', message, data); }
}

/**
 * Data validator for Airtable records
 */
class DataValidator {
    constructor(logger) {
        this.logger = logger;
    }
    
    validateRecord(record) {
        this.logger.debug('Starting record validation', record);
        
        const errors = [];
        const warnings = [];
        
        // Check required fields
        for (const field of CONFIG.REQUIRED_FIELDS) {
            if (!record[field] || record[field].toString().trim() === '') {
                errors.push(`Missing required field: ${field}`);
            }
        }
        
        // Validate category
        if (record.category && !CONFIG.VALID_CATEGORIES.includes(record.category.toLowerCase())) {
            errors.push(`Invalid category: ${record.category}. Valid categories: ${CONFIG.VALID_CATEGORIES.join(', ')}`);
        }
        
        // Validate impact level
        if (record.impact && !CONFIG.VALID_IMPACT_LEVELS.includes(record.impact.toLowerCase())) {
            errors.push(`Invalid impact level: ${record.impact}. Valid levels: ${CONFIG.VALID_IMPACT_LEVELS.join(', ')}`);
        }
        
        // Validate date format
        if (record.date_of_update) {
            const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
            if (!dateRegex.test(record.date_of_update)) {
                errors.push(`Invalid date format: ${record.date_of_update}. Expected format: YYYY-MM-DD`);
            }
        }
        
        // Validate numeric fields for draws
        if (record.category === 'draws') {
            if (record.cutoff && isNaN(parseInt(record.cutoff))) {
                errors.push(`Invalid cutoff value: ${record.cutoff}. Must be a number.`);
            }
            if (record.invitation && isNaN(parseInt(record.invitation))) {
                errors.push(`Invalid invitation value: ${record.invitation}. Must be a number.`);
            }
        }
        
        // Validate URL format
        if (record.source_url && !this.isValidUrl(record.source_url)) {
            warnings.push(`Invalid source URL format: ${record.source_url}`);
        }
        
        // Check for common data quality issues
        if (record.headline && record.headline.length > 200) {
            warnings.push(`Headline is very long (${record.headline.length} characters). Consider shortening.`);
        }
        
        if (record.summary && record.summary.length > 500) {
            warnings.push(`Summary is very long (${record.summary.length} characters). Consider shortening.`);
        }
        
        const result = {
            isValid: errors.length === 0,
            errors,
            warnings,
            record: this.cleanRecord(record)
        };
        
        this.logger.debug('Validation completed', result);
        return result;
    }
    
    isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }
    
    cleanRecord(record) {
        const cleaned = {};
        
        // Clean and normalize all fields
        for (const [key, value] of Object.entries(record)) {
            if (value !== null && value !== undefined) {
                if (typeof value === 'string') {
                    cleaned[key] = value.trim();
                } else if (Array.isArray(value)) {
                    cleaned[key] = value.filter(item => item && item.toString().trim() !== '');
                } else {
                    cleaned[key] = value;
                }
            }
        }
        
        // Normalize category and impact to lowercase
        if (cleaned.category) {
            cleaned.category = cleaned.category.toLowerCase();
        }
        if (cleaned.impact) {
            cleaned.impact = cleaned.impact.toLowerCase();
        }
        
        // Convert numeric fields
        if (cleaned.cutoff) {
            cleaned.cutoff = parseInt(cleaned.cutoff);
        }
        if (cleaned.invitation) {
            cleaned.invitation = parseInt(cleaned.invitation);
        }
        if (cleaned.week_of_year) {
            cleaned.week_of_year = parseInt(cleaned.week_of_year);
        }
        
        return cleaned;
    }
}

/**
 * HTTP client for making requests to our automation system
 */
class HttpClient {
    constructor(logger) {
        this.logger = logger;
    }
    
    async makeRequest(url, data, options = {}) {
        const defaultOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'User-Agent': 'ImmiWatch-Airtable-Webhook/1.0',
                'X-Webhook-Secret': CONFIG.WEBHOOK_SECRET
            },
            timeout: 30000 // 30 seconds
        };
        
        const requestOptions = { ...defaultOptions, ...options };
        
        this.logger.debug(`Making request to: ${url}`, { data, options: requestOptions });
        
        try {
            const response = await fetch(url, {
                method: requestOptions.method,
                headers: requestOptions.headers,
                body: JSON.stringify(data),
                timeout: requestOptions.timeout
            });
            
            const responseText = await response.text();
            let responseData;
            
            try {
                responseData = JSON.parse(responseText);
            } catch (e) {
                responseData = { raw: responseText };
            }
            
            const result = {
                success: response.ok,
                status: response.status,
                statusText: response.statusText,
                data: responseData,
                headers: Object.fromEntries(response.headers.entries())
            };
            
            this.logger.info(`Request completed`, result);
            return result;
            
        } catch (error) {
            this.logger.error(`Request failed: ${error.message}`, error);
            throw error;
        }
    }
    
    async retryRequest(url, data, maxRetries = CONFIG.MAX_RETRIES) {
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                this.logger.info(`Attempt ${attempt}/${maxRetries} to send data to automation system`);
                return await this.makeRequest(url, data);
            } catch (error) {
                this.logger.warn(`Attempt ${attempt} failed: ${error.message}`);
                
                if (attempt === maxRetries) {
                    throw error;
                }
                
                // Wait before retry
                await new Promise(resolve => setTimeout(resolve, CONFIG.RETRY_DELAY * attempt));
            }
        }
    }
}

/**
 * Slack notification handler
 */
class SlackNotifier {
    constructor(webhookUrl, logger) {
        this.webhookUrl = webhookUrl;
        this.logger = logger;
    }
    
    async sendNotification(message, data = null) {
        if (!this.webhookUrl) {
            this.logger.warn('No Slack webhook configured, skipping notification');
            return;
        }
        
        try {
            const payload = this.formatMessage(message, data);
            const response = await fetch(this.webhookUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            if (response.ok) {
                this.logger.info('Slack notification sent successfully');
            } else {
                this.logger.warn(`Slack notification failed: ${response.status} ${response.statusText}`);
            }
        } catch (error) {
            this.logger.error(`Slack notification error: ${error.message}`);
        }
    }
    
    formatMessage(message, data) {
        const timestamp = new Date().toISOString();
        
        return {
            text: message,
            blocks: [
                {
                    type: "header",
                    text: {
                        type: "plain_text",
                        text: "📰 ImmiWatch News Automation"
                    }
                },
                {
                    type: "section",
                    text: {
                        type: "mrkdwn",
                        text: message
                    }
                },
                {
                    type: "context",
                    elements: [
                        {
                            type: "mrkdwn",
                            text: `Sent at ${timestamp}`
                        }
                    ]
                }
            ]
        };
    }
}

/**
 * Main webhook processor
 */
class AirtableWebhookProcessor {
    constructor() {
        this.logger = new Logger(CONFIG.LOG_LEVEL);
        this.validator = new DataValidator(this.logger);
        this.httpClient = new HttpClient(this.logger);
        this.slackNotifier = new SlackNotifier(CONFIG.SLACK_WEBHOOK_URL, this.logger);
    }
    
    async processWebhook(airtableData) {
        const startTime = Date.now();
        this.logger.info('Starting webhook processing', airtableData);
        
        try {
            // Step 1: Extract and validate record data
            const record = this.extractRecordData(airtableData);
            this.logger.info('Extracted record data', record);
            
            // Step 2: Validate the data
            const validation = this.validator.validateRecord(record);
            
            if (!validation.isValid) {
                const errorMessage = `Data validation failed:\n${validation.errors.join('\n')}`;
                this.logger.error(errorMessage, validation);
                await this.slackNotifier.sendNotification(`❌ News article validation failed:\n${validation.errors.join('\n')}`, validation);
                return { success: false, errors: validation.errors, warnings: validation.warnings };
            }
            
            // Step 3: Log warnings if any
            if (validation.warnings.length > 0) {
                this.logger.warn('Data validation warnings', validation.warnings);
                await this.slackNotifier.sendNotification(`⚠️ News article warnings:\n${validation.warnings.join('\n')}`, validation);
            }
            
            // Step 4: Send to automation system
            this.logger.info('Sending data to automation system', validation.record);
            const result = await this.httpClient.retryRequest(
                CONFIG.AUTOMATION_WEBHOOK_URL,
                validation.record
            );
            
            // Step 5: Handle response
            if (result.success) {
                const processingTime = Date.now() - startTime;
                const successMessage = `✅ News article processed successfully!\n\n**Article:** ${validation.record.headline}\n**Category:** ${validation.record.category}\n**Processing Time:** ${processingTime}ms`;
                
                this.logger.info('Webhook processing completed successfully', {
                    processingTime,
                    articleUrl: result.data?.article_url || 'N/A'
                });
                
                await this.slackNotifier.sendNotification(successMessage, {
                    article: validation.record,
                    result: result.data
                });
                
                return {
                    success: true,
                    processingTime,
                    articleUrl: result.data?.article_url,
                    warnings: validation.warnings
                };
            } else {
                const errorMessage = `❌ Automation system returned error:\nStatus: ${result.status}\nResponse: ${JSON.stringify(result.data)}`;
                
                this.logger.error(errorMessage, result);
                await this.slackNotifier.sendNotification(errorMessage, result);
                
                return {
                    success: false,
                    error: errorMessage,
                    status: result.status,
                    response: result.data
                };
            }
            
        } catch (error) {
            const errorMessage = `❌ Webhook processing failed: ${error.message}`;
            this.logger.error(errorMessage, error);
            await this.slackNotifier.sendNotification(errorMessage, { error: error.message });
            
            return {
                success: false,
                error: errorMessage,
                stack: error.stack
            };
        }
    }
    
    extractRecordData(airtableData) {
        this.logger.debug('Extracting record data from Airtable payload', airtableData);
        
        // Handle different Airtable webhook formats
        let record;
        
        if (airtableData.record) {
            // Single record format
            record = airtableData.record;
        } else if (airtableData.records && airtableData.records.length > 0) {
            // Multiple records format - take the first one
            record = airtableData.records[0];
        } else if (airtableData.fields) {
            // Direct fields format
            record = airtableData;
        } else {
            throw new Error('Unsupported Airtable webhook format');
        }
        
        // Extract fields from Airtable record
        const extractedData = {};
        
        // Map Airtable field names to our expected format
        const fieldMapping = {
            'Headline': 'headline',
            'Summary': 'summary',
            'Program Affected': 'program_affected',
            'Impact': 'impact',
            'Urgency Level': 'urgency_level',
            'Week of Year': 'week_of_year',
            'Date of Update': 'date_of_update',
            'Source URL': 'source_url',
            'Source': 'source',
            'Category': 'category',
            'Cutoff': 'cutoff',
            'Invitation': 'invitation'
        };
        
        // Extract fields from Airtable record
        if (record.fields) {
            for (const [airtableField, ourField] of Object.entries(fieldMapping)) {
                if (record.fields[airtableField] !== undefined) {
                    extractedData[ourField] = record.fields[airtableField];
                }
            }
        } else {
            // Direct field access
            for (const [airtableField, ourField] of Object.entries(fieldMapping)) {
                if (record[airtableField] !== undefined) {
                    extractedData[ourField] = record[airtableField];
                }
            }
        }
        
        this.logger.debug('Extracted data', extractedData);
        return extractedData;
    }
}

/**
 * Main execution function for Airtable webhook
 */
async function handleAirtableWebhook(airtableData) {
    const processor = new AirtableWebhookProcessor();
    return await processor.processWebhook(airtableData);
}

// Export for use in different environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        handleAirtableWebhook,
        AirtableWebhookProcessor,
        Logger,
        DataValidator,
        HttpClient,
        SlackNotifier,
        CONFIG
    };
}

// For browser/node.js compatibility
if (typeof window !== 'undefined') {
    window.ImmiWatchWebhook = {
        handleAirtableWebhook,
        AirtableWebhookProcessor,
        Logger,
        DataValidator,
        HttpClient,
        SlackNotifier,
        CONFIG
    };
}

// Example usage for testing
if (typeof process !== 'undefined' && process.argv[2] === 'test') {
    const testData = {
        record: {
            fields: {
                'Headline': 'Test Express Entry Draw',
                'Summary': 'This is a test summary for the automation system.',
                'Program Affected': ['Express Entry', 'Work Permit'],
                'Impact': 'high',
                'Urgency Level': 'informational',
                'Week of Year': 31,
                'Date of Update': '2025-07-29',
                'Source URL': 'https://ircc.gc.ca/test',
                'Source': 'IRCC',
                'Category': 'draws',
                'Cutoff': 485,
                'Invitation': 3500
            }
        }
    };
    
    handleAirtableWebhook(testData)
        .then(result => {
            console.log('Test completed:', result);
        })
        .catch(error => {
            console.error('Test failed:', error);
        });
} 