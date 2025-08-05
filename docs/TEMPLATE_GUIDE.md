# ImmiWatch Complete Page Template Guide

## 🎯 Complete Master Template

When creating new pages, use this **complete template** to automatically include all shared functionality:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-2573Q8G1WD"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-2573Q8G1WD');
    </script>
    
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Your page description here">
    <meta name="keywords" content="Canada immigration, Express Entry, OINP, BCPNP, LMIA, immigration data, analytics, ImmiWatch, Lexpoint">
    <meta name="author" content="ImmiWatch by Lexpoint">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://immiwatch.ca/your-page/">
    <meta property="og:title" content="Your Page Title | ImmiWatch">
    <meta property="og:description" content="Your page description here">
    <meta property="og:image" content="https://20597210.fs1.hubspotusercontent-na1.net/hubfs/20597210/logo%20banner.jpg">
    
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://immiwatch.ca/your-page/">
    <meta name="twitter:title" content="Your Page Title | ImmiWatch">
    <meta name="twitter:description" content="Your page description here">
    <meta name="twitter:image" content="https://20597210.fs1.hubspotusercontent-na1.net/hubfs/20597210/logo%20banner.jpg">
    
    <title>Your Page Title | ImmiWatch</title>
    
    <!-- Favicon - Consistent across all pages -->
    <link rel="icon" type="image/svg+xml" href="/favicon.svg?v=3&t=1737962580">
    <link rel="shortcut icon" href="/favicon.svg?v=3&t=1737962580">
    <link rel="apple-touch-icon" sizes="180x180" href="/favicon.svg?v=3&t=1737962580">
    <meta name="msapplication-TileColor" content="#4338ca">
    <meta name="theme-color" content="#4338ca">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    
    <!-- Shared Styles (includes EVERYTHING: hamburger menu, colors, footer, etc.) -->
    <link rel="stylesheet" href="/assets/css/shared-styles.css">
    
    <!-- Shared Scripts (includes hamburger menu JS and all functionality) -->
    <script src="/assets/js/shared-scripts.js"></script>
</head>
<body>
    <!-- Navigation - Complete with hamburger menu -->
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

    <!-- Breadcrumb (optional) -->
    <div class="breadcrumb">
        <div class="container">
            <div class="breadcrumb-content">
                <a href="/" class="breadcrumb-link">Home</a>
                <span>›</span>
                <a href="/your-section/" class="breadcrumb-link">Your Section</a>
                <span>›</span>
                <span>Your Page</span>
            </div>
        </div>
    </div>

    <!-- Page Header -->
    <section class="page-header">
        <div class="container">
            <div class="page-header-content">
                <div class="page-badge">
                    🎯 <span>Your Badge Text</span>
                </div>
                
                <h1 class="page-title">Your Page Title</h1>
                <p class="page-subtitle">
                    Your page description here. This should be a compelling description of what this page offers.
                </p>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">1000+</div>
                        <div class="stat-label">Users Served</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">50+</div>
                        <div class="stat-label">Reports Published</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">24/7</div>
                        <div class="stat-label">Support Available</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Your page content here -->
    <main>
        <div class="container">
            <!-- Content Section -->
            <section class="content-section">
                <div class="section-header">
                    <div class="section-badge">
                        📊 <span>Your Section</span>
                    </div>
                    <h2 class="section-title">Your Section Title</h2>
                    <p class="section-description">
                        Your section description here.
                    </p>
                </div>
                
                <!-- Card Grid Example -->
                <div class="card-grid">
                    <div class="card">
                        <div class="card-icon">📈</div>
                        <h3 class="card-title">Card Title</h3>
                        <p class="card-description">
                            Your card description here.
                        </p>
                        <a href="#" class="card-link">
                            Learn More →
                        </a>
                    </div>
                    
                    <div class="card">
                        <div class="card-icon">🎯</div>
                        <h3 class="card-title">Another Card</h3>
                        <p class="card-description">
                            Another card description here.
                        </p>
                        <a href="#" class="card-link">
                            Learn More →
                        </a>
                    </div>
                </div>
            </section>
            
            <!-- CTA Section -->
            <section class="content-section cta">
                <div class="container-narrow">
                    <h2>Ready to Get Started?</h2>
                    <p>Join thousands of immigration professionals who rely on ImmiWatch for accurate, up-to-date information.</p>
                    <a href="https://intake.immigratic.com/t/eELGpk1aGhus" target="_blank" class="btn btn-primary">
                        Get Started Today
                    </a>
                </div>
            </section>
        </div>
    </main>

    <!-- Footer - Complete with all links -->
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
                <p style="margin-top: 0.5rem; font-size: 0.875rem;">
                    Professional Immigration Analytics | 
                    <a href="mailto:hi@lexpoint.io" style="color: var(--primary-400);">hi@lexpoint.io</a>
                </p>
            </div>
        </div>
    </footer>
</body>
</html>
```

## 🎨 What's Automatically Included

### **Complete Design System:**
- ✅ **Favicon** - Consistent across all pages
- ✅ **Hamburger menu** - With cool animations
- ✅ **Navigation** - Complete with logo and all links
- ✅ **Color system** - All brand colors and variables
- ✅ **Typography** - Complete font system
- ✅ **Spacing** - Consistent spacing scale
- ✅ **Shadows** - Complete shadow system
- ✅ **Border radius** - Consistent rounded corners
- ✅ **Transitions** - Smooth animations everywhere
- ✅ **Footer** - Complete with all links and branding
- ✅ **Breadcrumbs** - Navigation breadcrumbs
- ✅ **Page headers** - Hero sections with stats
- ✅ **Card system** - Consistent card layouts
- ✅ **Button system** - Primary and secondary buttons
- ✅ **Badge system** - Status and category badges
- ✅ **Alert system** - Info, success, warning alerts
- ✅ **Stats system** - Number displays with labels
- ✅ **Responsive design** - Mobile-first approach

### **JavaScript Functionality:**
- ✅ **Hamburger menu** - Mobile navigation
- ✅ **Navbar scroll effects** - Sticky navigation
- ✅ **Smooth scrolling** - Anchor link navigation
- ✅ **Animations** - Intersection Observer effects
- ✅ **News slider** - Carousel functionality
- ✅ **Counter animations** - Number counting effects
- ✅ **Share buttons** - Social media sharing
- ✅ **Touch/swipe support** - Mobile gestures

## 🚀 Key Benefits

1. **Zero Setup Required** - Just copy the template and everything works
2. **Consistent Design** - All pages look and feel the same
3. **Future-Proof** - Updates to shared files apply everywhere
4. **Performance Optimized** - Single CSS and JS files
5. **SEO Ready** - Complete meta tags and structure
6. **Mobile First** - Responsive design out of the box
7. **Accessibility** - Proper semantic HTML structure

## 📁 File Structure

```
assets/
├── css/
│   └── shared-styles.css      # Complete design system
└── js/
    └── shared-scripts.js      # All JavaScript functionality

docs/
└── TEMPLATE_GUIDE.md         # This guide
```

## 🎯 Usage Instructions

1. **Copy the template** above
2. **Replace placeholder content** with your actual content
3. **Update meta tags** for SEO
4. **Add your specific content** in the main section
5. **That's it!** Everything else works automatically

## 🔧 Customization

### **Colors:**
All colors are available as CSS variables:
```css
.my-element {
    color: var(--primary-600);
    background: var(--gradient-primary);
}
```

### **Spacing:**
Use the spacing scale:
```css
.my-element {
    padding: var(--spacing-lg);
    margin: var(--spacing-xl);
}
```

### **Typography:**
Use the font system:
```css
.my-element {
    font-size: var(--font-size-xl);
    font-weight: var(--font-weight-semibold);
}
```

## 📱 Mobile Features

- **Hamburger menu** automatically appears on mobile
- **Touch gestures** supported for sliders
- **Responsive grid** adapts to screen size
- **Optimized typography** for mobile reading
- **Fast loading** with optimized assets

## 🎨 Brand Consistency

- **Logo** - Consistent across all pages
- **Colors** - Brand colors enforced via CSS variables
- **Typography** - Inter font family throughout
- **Spacing** - Consistent spacing scale
- **Animations** - Smooth, professional transitions
- **Icons** - Consistent icon usage

This template ensures **100% consistency** across all ImmiWatch pages! 🎉 