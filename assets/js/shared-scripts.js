/**
 * ImmiWatch Shared Scripts
 * Auto-included functionality for all pages
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    initializeNavbar();
    initializeMobileMenu();
    initializeScrollEffects();
});

/**
 * Initialize navbar functionality
 */
function initializeNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

/**
 * Initialize mobile menu functionality
 */
function initializeMobileMenu() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            navMenu.classList.toggle('mobile-open');
            mobileMenuBtn.classList.toggle('active');
        });
    }
}

/**
 * Initialize scroll effects and animations
 */
function initializeScrollEffects() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
            }
        });
    }, observerOptions);

    // Observe elements with animation classes
    document.querySelectorAll('.feature-card, .stats-card, .card').forEach(el => {
        observer.observe(el);
    });
}

/**
 * Initialize news slider functionality
 */
function initializeNewsSlider() {
    const slider = document.querySelector('.news-slider');
    if (!slider) return;

    let currentSlide = 0;
    const slides = document.querySelectorAll('.news-slide');
    const totalSlides = slides.length;

    function updateSlider() {
        slides.forEach((slide, index) => {
            slide.style.transform = `translateX(${100 * (index - currentSlide)}%)`;
        });
    }

    function changeSlide(direction) {
        currentSlide = (currentSlide + direction + totalSlides) % totalSlides;
        updateSlider();
    }

    // Auto-play slider
    let autoPlayInterval = setInterval(() => {
        changeSlide(1);
    }, 5000);

    // Pause auto-play on hover
    const sliderContainer = document.querySelector('.news-slider-container');
    if (sliderContainer) {
        sliderContainer.addEventListener('mouseenter', () => {
            clearInterval(autoPlayInterval);
        });
        
        sliderContainer.addEventListener('mouseleave', () => {
            autoPlayInterval = setInterval(() => {
                changeSlide(1);
            }, 5000);
        });
    }

    // Touch/Swipe support for mobile
    let touchStartX = 0;
    let touchEndX = 0;
    
    slider.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
    });
    
    slider.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].clientX;
        handleSwipe();
    });

    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                changeSlide(1); // Swipe left, go to next
            } else {
                changeSlide(-1); // Swipe right, go to previous
            }
        }
    }

    // Initialize slider
    updateSlider();
}

/**
 * Initialize counter animations
 */
function initializeCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        const duration = 2000;
        const startTime = performance.now();
        const startValue = 0;
        
        function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth animation
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentValue = Math.floor(startValue + (target - startValue) * easeOutQuart);
            
            counter.textContent = currentValue;
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            }
        }
        
        requestAnimationFrame(updateCounter);
    });
}

/**
 * Initialize share functionality
 */
function initializeShareButtons() {
    const shareButtons = document.querySelectorAll('[data-share]');
    
    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const title = this.getAttribute('data-share-title') || document.title;
            const text = this.getAttribute('data-share-text') || '';
            const url = this.getAttribute('data-share-url') || window.location.href;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    text: text,
                    url: url
                });
            } else {
                // Fallback for browsers that don't support Web Share API
                const shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}%20${encodeURIComponent(url)}`;
                window.open(shareUrl, '_blank');
            }
        });
    });
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initializeSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 100; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Initialize all shared functionality
 */
function initializeAll() {
    initializeNavbar();
    initializeMobileMenu();
    initializeScrollEffects();
    initializeNewsSlider();
    initializeCounters();
    initializeShareButtons();
    initializeSmoothScrolling();
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initializeAll);

// Export functions for manual initialization if needed
window.ImmiWatchScripts = {
    initializeNavbar,
    initializeMobileMenu,
    initializeScrollEffects,
    initializeNewsSlider,
    initializeCounters,
    initializeShareButtons,
    initializeSmoothScrolling,
    initializeAll
}; 