# 🤖 Express Entry Automation Guide

## 🎯 **Overview**

This guide covers the **complete automated system** for detecting Express Entry draws and automatically updating monthly reports. The system includes Lambda monitoring, GitHub webhooks, and automated report updates.

## 🔄 **Complete Automation Flow**

```
IRCC Website → Lambda Function → GitHub Webhook → GitHub Actions → Report Update
```

### **1. IRCC Monitoring (Lambda)**
- **Frequency**: Every hour
- **Function**: `lambda/ircc_monitor.py`
- **Purpose**: Detect new draws on IRCC website

### **2. Webhook Processing (GitHub Actions)**
- **Trigger**: Repository dispatch event
- **Workflow**: `.github/workflows/webhook_handler.yml`
- **Purpose**: Process draw data and update reports

### **3. Report Updates (Scripts)**
- **Script**: `scripts/webhook_handler.py`
- **Purpose**: Update monthly reports with new data
- **Output**: Updated HTML reports with intelligent analysis

## 🚀 **Quick Setup**

### **1. Lambda Function Setup**

#### **Deploy Lambda Function**
```bash
# Create deployment package
cd lambda
zip -r ircc_monitor.zip ircc_monitor.py

# Deploy to AWS Lambda
aws lambda create-function \
  --function-name ircc-monitor \
  --runtime python3.11 \
  --handler ircc_monitor.lambda_handler \
  --zip-file fileb://ircc_monitor.zip \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role
```

#### **Set Environment Variables**
```bash
aws lambda update-function-configuration \
  --function-name ircc-monitor \
  --environment Variables='{
    "GITHUB_TOKEN": "your_github_token",
    "GITHUB_REPO": "getguide/immiwatch",
    "S3_BUCKET": "immiwatch-draw-data"
  }'
```

#### **Create CloudWatch Rule**
```bash
# Create rule to trigger every hour
aws events put-rule \
  --name "ircc-monitor-hourly" \
  --schedule-expression "rate(1 hour)" \
  --state ENABLED

# Add Lambda as target
aws events put-targets \
  --rule "ircc-monitor-hourly" \
  --targets "Id"="1","Arn"="arn:aws:lambda:region:account:function:ircc-monitor"
```

### **2. GitHub Repository Setup**

#### **Add Repository Secrets**
1. Go to repository Settings → Secrets and variables → Actions
2. Add `GITHUB_TOKEN` with appropriate permissions
3. Ensure the token has `repo` scope for repository dispatch

#### **Test Webhook Handler**
```bash
# Test with sample data
python3 scripts/webhook_handler.py --test-webhook
```

## 📊 **Webhook Data Format**

### **Expected Webhook Payload (Lambda Format)**
```json
{
  "body": {
    "Program": "EE-PNP",
    "Category": "General",
    "Region": "All",
    "draw.date.most.recent": "2025-08-05",
    "Score": 726,
    "Scoring System": "CRS",
    "Filter by program": "Express Entry",
    "Invitation": 277,
    "Last Checked": "2025-08-05T13:25:51.846699",
    "Draw Number": 348
  }
}
```

### **Required Fields**
- `body.Program`: Program/Category type (EE-PNP, EE-CEC, EE-Health, etc.)
- `body.draw.date.most.recent`: Date of the draw (YYYY-MM-DD)
- `body.Score`: CRS score cutoff
- `body.Invitation`: Total ITAs issued
- `body.Draw Number`: Express Entry draw number

### **Program/Category Mapping**
**Program-Based Draws:**
- `EE-PNP` → PNP ITAs
- `EE-CEC` → CEC ITAs  
- `EE-FSW` → FSW ITAs
- `EE-FST` → FST ITAs

**Category-Based Draws:**
- `EE-Health` → Healthcare ITAs
- `EE-French` → French-Speaking ITAs
- `EE-Trade` → Trade ITAs
- `EE-Education` → Education ITAs
- `EE-Agriculture` → Agriculture ITAs
- `EE-STEM` → STEM ITAs

### **Ignored Fields**
- `body.Category`, `body.Region`: Internal fields
- `body.Scoring System`, `body.Filter by program`: Internal fields
- `body.Last Checked`: Function timestamp

## 🔧 **System Components**

### **1. Lambda Function (`lambda/ircc_monitor.py`)**

#### **Features**
- ✅ **Hourly Monitoring**: Checks IRCC website every hour
- ✅ **Pattern Recognition**: Detects new draws using regex patterns
- ✅ **Duplicate Prevention**: Compares with last known draw
- ✅ **Webhook Dispatch**: Sends data to GitHub via repository dispatch
- ✅ **S3 Storage**: Stores last known draw for comparison

#### **Configuration**
```python
# Environment variables
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'getguide/immiwatch')
S3_BUCKET = os.environ.get('S3_BUCKET', 'immiwatch-draw-data')
```

### **2. GitHub Actions Workflow (`.github/workflows/webhook_handler.yml`)**

#### **Features**
- ✅ **Webhook Processing**: Handles repository dispatch events
- ✅ **Python Environment**: Sets up Python 3.11
- ✅ **Script Execution**: Runs webhook handler
- ✅ **Status Reporting**: Creates detailed summaries

#### **Trigger**
```yaml
on:
  repository_dispatch:
    types: [express_entry_draw]
```

### **3. Webhook Handler (`scripts/webhook_handler.py`)**

#### **Features**
- ✅ **Data Validation**: Validates webhook payload
- ✅ **Report Creation**: Creates initial reports if needed
- ✅ **Report Updates**: Updates existing monthly reports
- ✅ **Git Integration**: Automatic commits and pushes
- ✅ **Logging**: Comprehensive logging for debugging

#### **Usage**
```bash
# Process webhook data
python3 scripts/webhook_handler.py --webhook-data webhook_data.json

# Test with sample data
python3 scripts/webhook_handler.py --test-webhook

# Process JSON string
python3 scripts/webhook_handler.py --webhook-json '{"draw_date":"2025-08-05",...}'
```

## 🛡️ **Security & Best Practices**

### **Lambda Security**
- ✅ **IAM Roles**: Minimal required permissions
- ✅ **Environment Variables**: Secure token storage
- ✅ **Error Handling**: Graceful failure handling
- ✅ **Rate Limiting**: Respect IRCC website limits

### **GitHub Security**
- ✅ **Repository Secrets**: Secure token storage
- ✅ **Webhook Validation**: Validate incoming data
- ✅ **Access Control**: Limited token permissions
- ✅ **Audit Logging**: Track all webhook activities

### **Data Security**
- ✅ **S3 Encryption**: Encrypt stored draw data
- ✅ **Input Validation**: Validate all webhook data
- ✅ **Error Logging**: Log errors without exposing sensitive data
- ✅ **Backup Strategy**: Regular backups of draw data

## 📈 **Monitoring & Debugging**

### **Lambda Monitoring**
```bash
# Check Lambda logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/ircc-monitor"

# View recent logs
aws logs tail /aws/lambda/ircc-monitor --follow
```

### **GitHub Actions Monitoring**
- **Actions Tab**: View workflow runs
- **Repository Dispatch**: Monitor webhook events
- **Workflow Logs**: Detailed execution logs

### **Webhook Handler Logging**
```bash
# View webhook processing logs
tail -f webhook_processing.log

# Test webhook processing
python3 scripts/webhook_handler.py --test-webhook
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Lambda Function Issues**
**Problem**: Function not detecting draws
```bash
# Check Lambda logs
aws logs tail /aws/lambda/ircc-monitor

# Test function locally
python3 lambda/ircc_monitor.py
```

**Problem**: Webhook not sending
```bash
# Verify GitHub token
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# Check repository permissions
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/repos/getguide/immiwatch
```

#### **GitHub Actions Issues**
**Problem**: Workflow not triggering
```bash
# Check repository dispatch
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/getguide/immiwatch/dispatches \
  -d '{"event_type":"express_entry_draw","client_payload":{"test":true}}'
```

**Problem**: Script execution fails
```bash
# Test webhook handler locally
python3 scripts/webhook_handler.py --test-webhook

# Check Python dependencies
pip install requests boto3
```

### **Error Messages**
- **"Missing required field"**: Check webhook data format
- **"Invalid date format"**: Use YYYY-MM-DD format
- **"GitHub token invalid"**: Verify token permissions
- **"S3 access denied"**: Check IAM permissions
- **"Report file not found"**: Generate initial report first

## 🔄 **Manual Testing**

### **Test Lambda Function**
```bash
# Test locally
cd lambda
python3 ircc_monitor.py
```

### **Test Webhook Handler**
```bash
# Test with sample data
python3 scripts/webhook_handler.py --test-webhook

# Test with custom data
echo '{"draw_date":"2025-08-05","draw_number":1,"itas":3000,"crs":475}' > test_webhook.json
python3 scripts/webhook_handler.py --webhook-data test_webhook.json
```

### **Test GitHub Actions**
```bash
# Trigger repository dispatch
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/getguide/immiwatch/dispatches \
  -d '{
    "event_type": "express_entry_draw",
    "client_payload": {
      "draw_date": "2025-08-05",
      "draw_number": 1,
      "itas": 3000,
      "crs": 475,
      "cec_itas": 2000,
      "pnp_itas": 800
    }
  }'
```

## 📈 **Future Enhancements**

### **Planned Features**
- 🔄 **Advanced IRCC Parsing**: More sophisticated page parsing
- 🔄 **Multiple Data Sources**: Monitor additional IRCC pages
- 🔄 **Real-time Notifications**: Slack/Discord notifications
- 🔄 **Analytics Dashboard**: Monitor system performance
- 🔄 **Predictive Analysis**: Forecast future draws

### **Integration Opportunities**
- 🔄 **Newsletter Automation**: Auto-generate newsletter content
- 🔄 **Social Media**: Auto-post to social platforms
- 🔄 **Email Alerts**: Notify subscribers of new draws
- 🔄 **Analytics Integration**: Track draw patterns and trends

## 🤝 **Team Collaboration**

### **For AI Agents**
- **Monitor system logs** for any issues
- **Test webhook processing** regularly
- **Update IRCC parsing patterns** as needed
- **Maintain documentation** for system changes

### **For Human Developers**
- **Review Lambda logs** for monitoring issues
- **Update IRCC URLs** if website structure changes
- **Monitor GitHub Actions** for webhook processing
- **Maintain security** of tokens and permissions

## 📞 **Support Resources**

- **Lambda Function**: `lambda/ircc_monitor.py`
- **Webhook Handler**: `scripts/webhook_handler.py`
- **GitHub Actions**: `.github/workflows/webhook_handler.yml`
- **Documentation**: This guide and related docs
- **Testing**: Manual testing procedures above

---

**Last Updated**: July 2025  
**Maintained By**: ImmiWatch Development Team  
**Version**: 1.0 