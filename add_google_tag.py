#!/usr/bin/env python3
"""
Script to add Google Analytics tag to all HTML files in the project.
Adds the tag immediately after the <head> element.
"""

import os
import re
from pathlib import Path

# Google Analytics tag to add
GOOGLE_TAG = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2573Q8G1WD"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-2573Q8G1WD');
</script>'''

def add_google_tag_to_file(file_path):
    """Add Google Analytics tag to a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if Google tag already exists
        if 'G-2573Q8G1WD' in content:
            print(f"✅ Google tag already exists in {file_path}")
            return False
        
        # Find <head> tag and add Google tag after it
        head_pattern = r'(<head[^>]*>)'
        match = re.search(head_pattern, content, re.IGNORECASE)
        
        if match:
            head_tag = match.group(1)
            new_content = content.replace(head_tag, head_tag + '\n' + GOOGLE_TAG)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Added Google tag to {file_path}")
            return True
        else:
            print(f"❌ No <head> tag found in {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def find_html_files(directory):
    """Find all HTML files in the directory and subdirectories."""
    html_files = []
    for root, dirs, files in os.walk(directory):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    return html_files

def main():
    """Main function to add Google tag to all HTML files."""
    current_dir = os.getcwd()
    html_files = find_html_files(current_dir)
    
    print(f"Found {len(html_files)} HTML files")
    print("=" * 50)
    
    updated_count = 0
    skipped_count = 0
    
    for file_path in html_files:
        if add_google_tag_to_file(file_path):
            updated_count += 1
        else:
            skipped_count += 1
    
    print("=" * 50)
    print(f"Summary:")
    print(f"✅ Updated: {updated_count} files")
    print(f"⏭️  Skipped: {skipped_count} files")
    print(f"📊 Total: {len(html_files)} files")

if __name__ == "__main__":
    main() 