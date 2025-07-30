# 🤖 AI Agent Guidelines for ImmiWatch

## 🎯 **IMPORTANT: Before Making Any Changes**

**This document contains critical information for AI agents working on this project. Please read thoroughly before making any modifications.**

## 📋 **Quick Reference for Common Tasks**

### **Navigation Updates**
**⚠️ CRITICAL**: Never manually edit navigation menus across multiple files. Use our automated scripts:

```bash
# For simple text changes
./scripts/quick_update.sh "old_text" "new_text"

# For complex updates
python3 scripts/update_navigation.py

# For major restructures
python3 scripts/template_generator.py
```

**Full Guide**: [Navigation Management Guide](docs/NAVIGATION_MANAGEMENT_GUIDE.md)

### **Data Updates**
- **Express Entry Reports**: Use automated generator for new monthly reports
  ```bash
  python3 scripts/generate_monthly_report.py 2025-08 --data-file august_data.json
  ```
- **News Articles**: Add to `news/daily/` with proper categorization
- **Newsletters**: Create in `news/digest/week-XX-YYYY/`

### **Content Changes**
- **Home Page**: `index.html` (hero section, features, stats)
- **Reports**: Monthly Express Entry analysis pages
- **Tools**: Immigration calculators and navigators
- **About**: Company information and mission

## 🛡️ **Security & Safety Protocols**

### **Before Any Update**
1. **Commit Current State**: `git add . && git commit -m "Backup before changes"`
2. **Check Documentation**: Review relevant guides in `docs/`
3. **Test Locally**: Verify changes work before pushing
4. **Follow Scripts**: Use provided automation tools when available

### **Navigation Safety**
- **Never manually edit** navigation across multiple files
- **Always use scripts** for navigation changes
- **Test thoroughly** after any navigation updates
- **Check relative paths** for different file depths

### **Content Safety**
- **Backup before changes** to prevent data loss
- **Validate HTML structure** after modifications
- **Test responsive design** on mobile devices
- **Verify all links** work correctly

## 🔧 **Available Automation Tools**

### **Navigation Management**
- `scripts/quick_update.sh` - Quick text replacement
- `scripts/update_navigation.py` - Batch updates
- `scripts/template_generator.py` - Template-based generation

### **Content Management**
- **Monthly Report Generator**: `scripts/generate_monthly_report.py`
- **Data Templates**: `scripts/monthly_report_data_template.json`
- **Template-based page generation**
- **Error handling and rollback procedures**

### **Quality Assurance**
- HTML validation tools
- Link checking automation
- Cross-browser testing procedures

## 📚 **Documentation Structure**

```
docs/
├── NAVIGATION_MANAGEMENT_GUIDE.md    # Navigation automation
├── MONTHLY_REPORT_GENERATOR_GUIDE.md # Monthly report generation
├── EXPRESS_ENTRY_UPDATE_GUIDE.md     # Data update procedures
├── DATA_FORMATS.md                   # Data structure standards
├── ANALYSIS_METHODOLOGY.md           # Analysis procedures
└── NEWS_SYSTEM_GUIDE.md             # News content management
```

## 🎯 **Common Tasks & Solutions**

### **Adding New Menu Item**
1. **Use Script**: `./scripts/quick_update.sh "About</a></li>" "About</a></li><li><a href=\"/new-page/\" class=\"nav-link\">New Item</a></li>"`
2. **Create Page**: Add new HTML file
3. **Update Templates**: If using template generator
4. **Test Navigation**: Verify all links work

### **Updating Brand Name**
1. **Use Script**: `./scripts/quick_update.sh "ImmiWatch" "New Brand Name"`
2. **Update Meta Tags**: Check all page titles and descriptions
3. **Test Branding**: Verify consistent appearance

### **Adding New Report**
1. **Use Generator**: `python3 scripts/generate_monthly_report.py 2025-08 --data-file august_data.json`
2. **Create Data File**: Copy template and edit with actual data
3. **Generate Report**: Run the generator script
4. **Test & Deploy**: Review and commit changes

### **Content Updates**
1. **Backup First**: Always commit current state
2. **Make Changes**: Edit specific files
3. **Test Locally**: Verify functionality
4. **Commit Changes**: With descriptive message

## 🚨 **Emergency Procedures**

### **If Scripts Fail**
1. **Check Permissions**: Ensure scripts are executable
2. **Verify Paths**: Check file paths and relative links
3. **Manual Backup**: Create git commit before manual changes
4. **Test Incrementally**: Make small changes and test

### **If Navigation Breaks**
1. **Revert Changes**: `git reset --hard HEAD~1`
2. **Use Template Generator**: `python3 scripts/template_generator.py`
3. **Check File Structure**: Verify all files exist
4. **Test All Pages**: Ensure navigation works everywhere

### **If Content is Lost**
1. **Check Git History**: `git log --oneline`
2. **Restore from Commit**: `git checkout <commit-hash> -- <file>`
3. **Recreate if Needed**: Use templates and documentation
4. **Test Thoroughly**: Verify all functionality

## 📊 **Quality Standards**

### **Before Committing**
- [ ] All navigation links work correctly
- [ ] Mobile responsive design maintained
- [ ] No broken HTML tags
- [ ] All images and assets load properly
- [ ] Cross-browser compatibility verified
- [ ] Accessibility standards met

### **After Deployment**
- [ ] Live site functions correctly
- [ ] All pages accessible
- [ ] Navigation consistent across site
- [ ] Performance acceptable
- [ ] No console errors

## 🤝 **Team Collaboration**

### **For AI Agents**
- **Always check documentation first**
- **Use provided automation tools**
- **Follow security protocols**
- **Test changes thoroughly**
- **Document custom modifications**

### **For Human Developers**
- **Review AI agent changes**
- **Verify automation scripts**
- **Update documentation as needed**
- **Monitor system performance**
- **Maintain code quality standards**

## 📞 **Support Resources**

- **Documentation**: `docs/` directory
- **Scripts**: `scripts/` directory with README
- **Templates**: `_includes/` directory
- **Git History**: Previous changes and patterns
- **Testing**: Browser testing procedures

---

**Last Updated**: July 2025  
**Maintained By**: ImmiWatch Development Team  
**For AI Agents**: Please follow these guidelines to ensure project stability and consistency. 