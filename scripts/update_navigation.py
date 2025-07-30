#!/usr/bin/env python3
"""
Navigation Update Script for ImmiWatch
Automatically updates navigation menus and footers across all HTML files.
"""

import os
import re
from pathlib import Path

class NavigationUpdater:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.html_files = []
        
    def find_html_files(self):
        """Find all HTML files in the project"""
        for file_path in self.root_dir.rglob("*.html"):
            if not file_path.name.startswith(".") and "node_modules" not in str(file_path):
                self.html_files.append(file_path)
        print(f"Found {len(self.html_files)} HTML files")
        
    def update_navigation(self, old_text, new_text):
        """Update navigation menu text across all files"""
        updated_files = []
        
        for file_path in self.html_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if file contains the old text
                if old_text in content:
                    # Replace the text
                    new_content = content.replace(old_text, new_text)
                    
                    # Write back to file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    updated_files.append(file_path)
                    print(f"✅ Updated: {file_path}")
                    
            except Exception as e:
                print(f"❌ Error updating {file_path}: {e}")
        
        return updated_files
    
    def update_footer(self, old_text, new_text):
        """Update footer links across all files"""
        return self.update_navigation(old_text, new_text)
    
    def update_meta_tags(self, old_text, new_text):
        """Update meta tags across all files"""
        return self.update_navigation(old_text, new_text)
    
    def batch_update(self, updates):
        """Perform multiple updates at once"""
        self.find_html_files()
        
        for update_type, old_text, new_text in updates:
            print(f"\n🔄 Updating {update_type}...")
            updated_files = self.update_navigation(old_text, new_text)
            print(f"📊 Updated {len(updated_files)} files for {update_type}")

def main():
    updater = NavigationUpdater()
    
    # Example: Change "Tools" to "Navigators" across all files
    updates = [
        ("navigation", 'class="nav-link">Tools</a>', 'class="nav-link">Navigators</a>'),
        ("footer", 'class="footer-link">Tools</a>', 'class="footer-link">Navigators</a>'),
        ("meta", 'Immigration Tools', 'Immigration Navigators'),
    ]
    
    updater.batch_update(updates)
    
    print("\n🎉 Navigation update completed!")

if __name__ == "__main__":
    main() 