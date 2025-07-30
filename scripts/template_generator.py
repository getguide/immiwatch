#!/usr/bin/env python3
"""
Template Generator for ImmiWatch
Generates navigation and footer with correct relative paths based on file location.
"""

import os
from pathlib import Path

class TemplateGenerator:
    def __init__(self):
        self.nav_template = """<nav class="navbar">
    <div class="nav-content">
        <div class="nav-brand">
            <a href="{home_path}" class="logo">
                <span class="logo-title">ImmiWatch</span>
                <span class="logo-subtitle">By Lexpoint.io</span>
            </div>
        </div>
        
        <ul class="nav-menu">
            <li><a href="{home_path}" class="nav-link">Home</a></li>
            <li><a href="{reports_path}" class="nav-link">Reports</a></li>
            <li><a href="{tools_path}" class="nav-link">Navigators</a></li>
            <li><a href="{news_path}" class="nav-link">News</a></li>
            <li><a href="{about_path}" class="nav-link">About</a></li>
            <li><a href="https://intake.immigratic.com/t/eELGpk1aGhus" target="_blank" class="nav-link nav-cta">Get Started</a></li>
        </ul>
        
        <button class="mobile-menu-btn">
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
        </button>
    </div>
</nav>"""

        self.footer_template = """<footer class="footer">
    <div class="container">
        <div class="footer-content">
            <div class="footer-section">
                <h3>ImmiWatch Data Studio</h3>
                <p>Professional immigration intelligence and strategic insights for Canada's immigration landscape.</p>
            </div>
            
            <div class="footer-section">
                <h4>Quick Links</h4>
                <div class="footer-links">
                    <a href="{reports_path}" class="footer-link">Reports</a>
                    <a href="{tools_path}" class="footer-link">Navigators</a>
                    <a href="{news_path}" class="footer-link">News</a>
                    <a href="{about_path}" class="footer-link">About</a>
                </div>
            </div>
            
            <div class="footer-section">
                <h4>Resources</h4>
                <div class="footer-links">
                    <a href="{updates_path}" class="footer-link">Updates</a>
                    <a href="mailto:hi@lexpoint.io" class="footer-link">Contact</a>
                    <a href="https://immiwatch.ca" target="_blank" class="footer-link">immiwatch.ca</a>
                </div>
            </div>
        </div>
        
        <div class="footer-bottom">
            <p>&copy; 2025 ImmiWatch Data Studio - Professional Immigration Intelligence</p>
        </div>
    </div>
</footer>"""

    def calculate_paths(self, file_path):
        """Calculate relative paths from file location to root"""
        file_path = Path(file_path)
        depth = len(file_path.parts) - 1
        
        if depth == 0:  # Root level
            return {
                'home_path': './',
                'reports_path': './reports/',
                'tools_path': './tools/',
                'news_path': './news/',
                'about_path': './about/',
                'updates_path': './updates/'
            }
        else:
            # Calculate relative paths based on depth
            prefix = '../' * depth
            return {
                'home_path': f'{prefix}',
                'reports_path': f'{prefix}reports/',
                'tools_path': f'{prefix}tools/',
                'news_path': f'{prefix}news/',
                'about_path': f'{prefix}about/',
                'updates_path': f'{prefix}updates/'
            }

    def generate_nav(self, file_path):
        """Generate navigation HTML for a specific file"""
        paths = self.calculate_paths(file_path)
        return self.nav_template.format(**paths)

    def generate_footer(self, file_path):
        """Generate footer HTML for a specific file"""
        paths = self.calculate_paths(file_path)
        return self.footer_template.format(**paths)

    def update_file(self, file_path):
        """Update navigation and footer in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate new nav and footer
            new_nav = self.generate_nav(file_path)
            new_footer = self.generate_footer(file_path)
            
            # Replace existing nav (simple pattern matching)
            nav_pattern = r'<nav class="navbar">.*?</nav>'
            content = re.sub(nav_pattern, new_nav, content, flags=re.DOTALL)
            
            # Replace existing footer
            footer_pattern = r'<footer class="footer">.*?</footer>'
            content = re.sub(footer_pattern, new_footer, content, flags=re.DOTALL)
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Updated: {file_path}")
            
        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")

    def update_all_files(self):
        """Update all HTML files in the project"""
        import re
        
        html_files = []
        for file_path in Path('.').rglob("*.html"):
            if not file_path.name.startswith(".") and "node_modules" not in str(file_path):
                html_files.append(file_path)
        
        print(f"Found {len(html_files)} HTML files to update")
        
        for file_path in html_files:
            self.update_file(file_path)

def main():
    generator = TemplateGenerator()
    generator.update_all_files()
    print("\n🎉 Template update completed!")

if __name__ == "__main__":
    main() 