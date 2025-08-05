# ImmiWatch Page Template Guide

## Quick Start Template

When creating new pages, use this template to automatically include all shared functionality:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Page Title | ImmiWatch</title>
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Shared Styles (includes hamburger menu CSS) -->
    <link rel="stylesheet" href="/assets/css/shared-styles.css">
    
    <!-- Shared Scripts (includes hamburger menu JS) -->
    <script src="/assets/js/shared-scripts.js"></script>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar" id="navbar">
        <div class="nav-content">
            <div class="logo">
                <div class="logo-icon"></div>
                <div class="logo-text">
                    <span class="logo-main">ImmiWatch</span>
                    <span class="logo-subtitle">By Lexpoint.io</span>
                </div>
            </div>
            
            <ul class="nav-menu">
                <li><a href="/" class="nav-link">Home</a></li>
                <li><a href="/reports/" class="nav-link">Reports</a></li>
                <li><a href="/tools/" class="nav-link">Navigators</a></li>
                <li><a href="/news/" class="nav-link">News</a></li>
                <li><a href="/about/" class="nav-link">About</a></li>
                <li><a href="https://intake.immigratic.com/t/eELGpk1aGhus" target="_blank" class="nav-link nav-cta">Get Started</a></li>
            </ul>
            
            <!-- Hamburger menu button (automatically functional) -->
            <button class="mobile-menu-btn">
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
            </button>
        </div>
    </nav>

    <!-- Your page content here -->
    <main>
        <!-- Your content -->
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-logo">ImmiWatch Data Studio</div>
                <p class="footer-description">
                    Professional Canada immigration analytics and insights. A premium product by Lexpoint.io, delivering data-driven immigration intelligence since 2025.
                </p>
                
                <div class="footer-links">
                    <a href="/reports/" class="footer-link">Reports</a>
                    <a href="/tools/" class="footer-link">Navigators</a>
                    <a href="/news/" class="footer-link">News</a>
                    <a href="/about/" class="footer-link">About</a>
                    <a href="mailto:hi@lexpoint.io" class="footer-link">Contact</a>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2025 ImmiWatch Data Studio - Part of Lexpoint.io</p>
            </div>
        </div>
    </footer>
</body>
</html>
```

## What's Automatically Included

### CSS Features (from shared-styles.css):
- ✅ Hamburger menu CSS with animations
- ✅ Mobile responsive navigation
- ✅ Navbar scroll effects
- ✅ All brand colors and variables
- ✅ Typography and spacing
- ✅ Card layouts and hover effects
- ✅ Button styles
- ✅ Footer styles

### JavaScript Features (from shared-scripts.js):
- ✅ Hamburger menu functionality
- ✅ Navbar scroll effects
- ✅ Smooth scrolling for anchor links
- ✅ Intersection Observer animations
- ✅ News slider functionality
- ✅ Counter animations
- ✅ Share button functionality

## Key Benefits

1. **No JavaScript Required**: Just include the shared-scripts.js file and everything works automatically
2. **Consistent Design**: All pages automatically get the same hamburger menu and styling
3. **Future-Proof**: Updates to shared files automatically apply to all pages
4. **Performance**: Single CSS and JS file reduces HTTP requests

## Optional Features

If you need additional functionality, you can manually initialize specific features:

```html
<script>
// Manual initialization (optional - usually not needed)
document.addEventListener('DOMContentLoaded', function() {
    // Initialize specific features if needed
    ImmiWatchScripts.initializeNewsSlider();
    ImmiWatchScripts.initializeCounters();
});
</script>
```

## File Structure

```
assets/
├── css/
│   └── shared-styles.css      # All shared CSS including hamburger menu
└── js/
    └── shared-scripts.js      # All shared JavaScript including hamburger menu
```

## Notes

- The hamburger menu automatically works on mobile devices (screen width < 1024px)
- All animations and transitions are included
- The navbar automatically becomes sticky and changes appearance on scroll
- All brand colors and design tokens are available as CSS variables 