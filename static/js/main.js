// static/js/main.js

// Debounce function to limit scroll event firing
function debounce(func, wait = 10) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Use passive event listeners
const passiveListenerOpts = { passive: true };

// Efficient scroll handler using requestAnimationFrame
let ticking = false;
const animateElements = document.querySelectorAll('.animate-on-scroll');

function onScroll() {
    if (!ticking) {
        requestAnimationFrame(() => {
            const windowHeight = window.innerHeight;
            animateElements.forEach(element => {
                const rect = element.getBoundingClientRect();
                if (rect.top <= windowHeight * 0.75) {
                    element.classList.add('animate-start');
                }
            });
            ticking = false;
        });
        ticking = true;
    }
}

// Initialize once DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Check if there are elements to animate
    if (animateElements.length > 0) {
        // Efficient event binding with debounce
        window.addEventListener('scroll', debounce(onScroll), passiveListenerOpts);
        
        // Initial check for elements
        onScroll();
    }
    
    // Initialize image lazy loading
    initializeLazyLoading();
}, { once: true });

// Separate function for lazy loading
function initializeLazyLoading() {
    // Check if native lazy loading is supported
    if ('loading' in HTMLImageElement.prototype) {
        // Browser supports lazy loading
        document.querySelectorAll('img[data-src]').forEach(img => {
            img.src = img.dataset.src;
        });
    } else {
        // Fallback to Intersection Observer
        const imageObserver = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                            imageObserver.unobserve(img);
                        }
                    }
                });
            },
            {
                rootMargin: '50px 0px',
                threshold: 0.01
            }
        );

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}