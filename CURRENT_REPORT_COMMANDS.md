# 📋 Current Monthly Report Commands

## 🎯 **Quick Reference**

### **Current Report Management**
```bash
# Create current month's report
python3 scripts/current_monthly_report_manager.py --create-current

# Get current report information
python3 scripts/current_monthly_report_manager.py --get-current

# Update current report designation
python3 scripts/current_monthly_report_manager.py --update-current

# Check for month transition
python3 scripts/current_monthly_report_manager.py --check-transition

# Get status summary of all reports
python3 scripts/current_monthly_report_manager.py --status

# Test the system
python3 scripts/current_monthly_report_manager.py --test
```

## 🔄 **How It Works**

### **Current Report System**
1. **Designates one report as "current"** for the active month
2. **Automatically creates new reports** on the 1st of each month
3. **Updates only the current report** when new draws arrive
4. **Maintains designation file** for tracking current report

### **Current Report File**
- **Location**: `scripts/current_monthly_report.json`
- **Purpose**: Tracks which report is currently active
- **Auto-updated**: When month transitions occur

### **Current Report Link**
- **Location**: `scripts/current_monthly_report_link.txt`
- **Purpose**: Human-readable reference for current report
- **Contains**: URL, local path, designation date

## 📅 **Monthly Schedule**

### **August 1, 2025 (00:00)**
- ✅ **Current Report**: July 2025
- 🔄 **Creates**: August 2025 report
- 🎯 **Designates**: August 2025 as current

### **September 1, 2025 (00:00)**
- ✅ **Current Report**: August 2025
- 🔄 **Creates**: September 2025 report
- 🎯 **Designates**: September 2025 as current

### **October 1, 2025 (00:00)**
- ✅ **Current Report**: September 2025
- 🔄 **Creates**: October 2025 report
- 🎯 **Designates**: October 2025 as current

## 🤖 **Automation Features**

### **GitHub Actions Scheduler**
- **Frequency**: Daily at 2 AM UTC
- **Purpose**: Check for month transitions
- **Action**: Create new monthly reports automatically
- **File**: `.github/workflows/monthly_report_scheduler.yml`

### **Webhook Integration**
- **Trigger**: When Lambda detects new draw
- **Action**: Update current monthly report
- **Integration**: Uses current report manager
- **Result**: Automatic report updates

## 📊 **Status Commands**

### **Check Current Report**
```bash
python3 scripts/current_monthly_report_manager.py --get-current
```
**Output**:
```
📋 Current report: 2025-07
📁 Path: reports/express-entry/ee-july-2025/index.html
🌐 URL: https://immiwatch.ca/reports/express-entry/ee-july-2025/
```

### **Get All Reports Status**
```bash
python3 scripts/current_monthly_report_manager.py --status
```
**Output**:
```
📊 Report Status Summary
Current: 2025-07
Total Reports: 7

All Reports:
  ⚪ January 2025 - https://immiwatch.ca/reports/express-entry/ee-january-2025/
  ⚪ February 2025 - https://immiwatch.ca/reports/express-entry/ee-february-2025/
  ⚪ March 2025 - https://immiwatch.ca/reports/express-entry/ee-march-2025/
  ⚪ April 2025 - https://immiwatch.ca/reports/express-entry/ee-april-2025/
  ⚪ May 2025 - https://immiwatch.ca/reports/express-entry/ee-may-2025/
  ⚪ June 2025 - https://immiwatch.ca/reports/express-entry/ee-june-2025/
  🟢 CURRENT July 2025 - https://immiwatch.ca/reports/express-entry/ee-july-2025/
```

## 🚀 **Quick Setup**

### **Initialize Current Report System**
```bash
# Create current month's report (if doesn't exist)
python3 scripts/current_monthly_report_manager.py --create-current

# Verify current designation
python3 scripts/current_monthly_report_manager.py --get-current
```

### **Test the System**
```bash
# Run comprehensive test
python3 scripts/current_monthly_report_manager.py --test
```

## 🔧 **Manual Override**

### **Force Create Current Report**
```bash
python3 scripts/current_monthly_report_manager.py --create-current
```

### **Force Update Designation**
```bash
python3 scripts/current_monthly_report_manager.py --update-current
```

### **Force Month Transition**
```bash
python3 scripts/current_monthly_report_manager.py --check-transition
```

## 📈 **Monitoring**

### **Check Logs**
```bash
# View current report management logs
tail -f current_report_management.log

# View webhook processing logs
tail -f webhook_processing.log
```

### **Check GitHub Actions**
- **Scheduler**: `.github/workflows/monthly_report_scheduler.yml`
- **Webhook Handler**: `.github/workflows/webhook_handler.yml`
- **Status**: GitHub Actions tab

## 🎯 **Key Benefits**

### **For You**
- ✅ **Zero Manual Work**: Reports created automatically
- ✅ **Always Current**: One designated report for updates
- ✅ **Seamless Transitions**: Automatic month-to-month handoff
- ✅ **Professional Quality**: Consistent report structure

### **For AI Agents**
- ✅ **Clear Commands**: Simple, predictable commands
- ✅ **Status Tracking**: Easy to check current state
- ✅ **Error Handling**: Comprehensive logging and recovery
- ✅ **Documentation**: Complete setup and usage guides

### **For Automation**
- ✅ **Scheduled Creation**: Daily checks for month transitions
- ✅ **Webhook Integration**: Automatic updates to current report
- ✅ **Git Integration**: Automatic commits and pushes
- ✅ **Status Monitoring**: Real-time tracking of system state

---

**Last Updated**: July 2025  
**Maintained By**: ImmiWatch Development Team  
**Version**: 1.0 