# 🚀 Quick Navigation Update Commands

## ⚡ **For AI Agents: Use These Commands Instead of Manual Updates**

### **Simple Text Changes**
```bash
./scripts/quick_update.sh "old_text" "new_text"
```

**Examples:**
```bash
# Change menu item
./scripts/quick_update.sh "Tools" "Navigators"

# Update brand name
./scripts/quick_update.sh "ImmiWatch" "ImmiWatch Pro"

# Add new menu item
./scripts/quick_update.sh "About</a></li>" "About</a></li><li><a href=\"/new-page/\" class=\"nav-link\">New Item</a></li>"
```

### **Complex Updates**
```bash
# Edit scripts/update_navigation.py and run:
python3 scripts/update_navigation.py
```

### **Major Restructures**
```bash
# Template-based regeneration:
python3 scripts/template_generator.py
```

## 📚 **Full Documentation**
- **Complete Guide**: [docs/NAVIGATION_MANAGEMENT_GUIDE.md](docs/NAVIGATION_MANAGEMENT_GUIDE.md)
- **AI Agent Guidelines**: [AI_AGENT_GUIDELINES.md](AI_AGENT_GUIDELINES.md)
- **Scripts README**: [scripts/README.md](scripts/README.md)

## ⚠️ **IMPORTANT**
- **Never manually edit** navigation across multiple files
- **Always backup** before making changes: `git add . && git commit -m "Backup"`
- **Test thoroughly** after any navigation updates
- **Use scripts** instead of manual file editing

---
**Last Updated**: July 2025  
**For AI Agents**: Check this file first before making navigation changes. 