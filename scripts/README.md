# Navigation Update Scripts

This directory contains scripts to efficiently update navigation menus and footers across all HTML files in the ImmiWatch project.

## 🚀 Quick Start

### Option 1: Simple Text Replacement
```bash
python3 scripts/update_navigation.py
```

### Option 2: Template-Based Updates
```bash
python3 scripts/template_generator.py
```

## 📋 Available Scripts

### 1. `update_navigation.py`
- **Purpose**: Simple text replacement across all HTML files
- **Use Case**: Quick changes like "Tools" → "Navigators"
- **Features**: 
  - Batch updates
  - Error handling
  - Progress reporting

### 2. `template_generator.py`
- **Purpose**: Generate navigation/footer with correct relative paths
- **Use Case**: Complete navigation restructure
- **Features**:
  - Automatic relative path calculation
  - Template-based generation
  - Handles different file depths

## 🎯 Usage Examples

### Change Navigation Text
```python
# In update_navigation.py, modify the updates list:
updates = [
    ("navigation", 'class="nav-link">Tools</a>', 'class="nav-link">Navigators</a>'),
    ("footer", 'class="footer-link">Tools</a>', 'class="footer-link">Navigators</a>'),
]
```

### Add New Navigation Item
```python
# In template_generator.py, modify nav_template:
'<li><a href="{new_path}" class="nav-link">New Item</a></li>'
```

## 🔧 Customization

### Adding New Paths
In `template_generator.py`, add to `calculate_paths()`:
```python
'new_path': f'{prefix}new-section/',
```

### Modifying Templates
Edit the `nav_template` and `footer_template` variables in `template_generator.py`.

## ⚠️ Best Practices

1. **Backup First**: Always commit current changes before running scripts
2. **Test on Sample**: Run on a few files first to verify changes
3. **Review Changes**: Check the generated HTML for correctness
4. **Commit After**: Always commit the changes after verification

## 🛠️ Manual Override

If you need to exclude certain files or make specific changes:

```python
# In update_navigation.py
def find_html_files(self):
    for file_path in self.root_dir.rglob("*.html"):
        # Add exclusion logic
        if "exclude-this" not in str(file_path):
            self.html_files.append(file_path)
```

## 📊 Monitoring

The scripts provide detailed output:
- ✅ Successfully updated files
- ❌ Files with errors
- 📊 Summary statistics

## 🔄 Future Improvements

1. **Git Integration**: Automatic commit after updates
2. **Dry Run Mode**: Preview changes without applying
3. **Selective Updates**: Update only specific file types
4. **Backup Creation**: Automatic backup before changes 