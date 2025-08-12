/**
 * Endirimall Main JavaScript
 * Handles search, favorites, newsletter subscription, and other interactive features
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeSearch();
    initializeFavorites();
    initializeNewsletterForms();
    initializeTooltips();
    initializeScrollToTop();
    
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

/**
 * Search functionality with real-time suggestions
 */
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchSuggestions = document.getElementById('searchSuggestions');
    let searchTimeout;

    if (!searchInput || !searchSuggestions) return;

    // Handle search input
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        // Clear previous timeout
        clearTimeout(searchTimeout);
        
        if (query.length < 2) {
            hideSearchSuggestions();
            return;
        }
        
        // Debounce search requests
        searchTimeout = setTimeout(() => {
            fetchSearchSuggestions(query);
        }, 300);
    });

    // Hide suggestions when clicking outside
    document.addEventListener('click', function(event) {
        if (!searchInput.contains(event.target) && !searchSuggestions.contains(event.target)) {
            hideSearchSuggestions();
        }
    });

    // Handle keyboard navigation
    searchInput.addEventListener('keydown', function(event) {
        const suggestions = searchSuggestions.querySelectorAll('.search-suggestion-item');
        const activeSuggestion = searchSuggestions.querySelector('.search-suggestion-item.active');
        
        switch (event.key) {
            case 'ArrowDown':
                event.preventDefault();
                navigateSuggestions(suggestions, activeSuggestion, 'down');
                break;
            case 'ArrowUp':
                event.preventDefault();
                navigateSuggestions(suggestions, activeSuggestion, 'up');
                break;
            case 'Enter':
                if (activeSuggestion) {
                    event.preventDefault();
                    activeSuggestion.click();
                }
                break;
            case 'Escape':
                hideSearchSuggestions();
                break;
        }
    });
}

/**
 * Fetch search suggestions from API
 */
function fetchSearchSuggestions(query) {
    const searchSuggestions = document.getElementById('searchSuggestions');
    
    // Show loading state
    searchSuggestions.innerHTML = '<div class="search-suggestion-item"><div class="loading-spinner"></div> Searching...</div>';
    searchSuggestions.style.display = 'block';
    
    fetch(`/deals/api/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchSuggestions(data.results);
        })
        .catch(error => {
            console.error('Search error:', error);
            searchSuggestions.innerHTML = '<div class="search-suggestion-item text-muted">Search unavailable</div>';
        });
}

/**
 * Display search suggestions
 */
function displaySearchSuggestions(results) {
    const searchSuggestions = document.getElementById('searchSuggestions');
    
    if (results.length === 0) {
        searchSuggestions.innerHTML = '<div class="search-suggestion-item text-muted">No results found</div>';
        return;
    }
    
    const suggestionsHTML = results.map(result => {
        let icon = '';
        let subtitle = '';
        
        switch (result.type) {
            case 'product':
                icon = result.image ? `<img src="${result.image}" alt="${result.title}" class="search-suggestion-image">` : '<i class="bi bi-box fs-4"></i>';
                subtitle = `<small class="text-muted">${result.store} - $${result.price}</small>`;
                break;
            case 'store':
                icon = result.image ? `<img src="${result.image}" alt="${result.title}" class="search-suggestion-image">` : '<i class="bi bi-shop fs-4"></i>';
                subtitle = '<small class="text-muted">Store</small>';
                break;
            case 'category':
                icon = result.icon ? `<i class="bi bi-${result.icon} fs-4"></i>` : '<i class="bi bi-grid fs-4"></i>';
                subtitle = '<small class="text-muted">Category</small>';
                break;
        }
        
        return `
            <a href="${result.url}" class="search-suggestion-item text-decoration-none text-dark">
                ${icon}
                <div class="flex-grow-1">
                    <div>${result.title}</div>
                    ${subtitle}
                </div>
            </a>
        `;
    }).join('');
    
    searchSuggestions.innerHTML = suggestionsHTML;
    searchSuggestions.style.display = 'block';
}

/**
 * Navigate through search suggestions with keyboard
 */
function navigateSuggestions(suggestions, activeSuggestion, direction) {
    if (suggestions.length === 0) return;
    
    // Remove active class from current suggestion
    if (activeSuggestion) {
        activeSuggestion.classList.remove('active');
    }
    
    let nextIndex = 0;
    
    if (activeSuggestion) {
        const currentIndex = Array.from(suggestions).indexOf(activeSuggestion);
        nextIndex = direction === 'down' 
            ? (currentIndex + 1) % suggestions.length
            : (currentIndex - 1 + suggestions.length) % suggestions.length;
    }
    
    suggestions[nextIndex].classList.add('active');
    suggestions[nextIndex].scrollIntoView({ block: 'nearest' });
}

/**
 * Hide search suggestions
 */
function hideSearchSuggestions() {
    const searchSuggestions = document.getElementById('searchSuggestions');
    if (searchSuggestions) {
        searchSuggestions.style.display = 'none';
    }
}

/**
 * Favorites functionality
 */
function initializeFavorites() {
    document.addEventListener('click', function(event) {
        if (event.target.closest('.favorite-btn')) {
            event.preventDefault();
            handleFavoriteToggle(event.target.closest('.favorite-btn'));
        }
    });
}

/**
 * Handle favorite toggle
 */
function handleFavoriteToggle(button) {
    const productId = button.dataset.productId;
    const icon = button.querySelector('i');
    
    // Check if user is authenticated
    if (!document.body.dataset.userAuthenticated) {
        showAlert('Please log in to add favorites', 'warning');
        return;
    }
    
    // Show loading state
    const originalIcon = icon.className;
    icon.className = 'bi bi-arrow-clockwise spin fs-5';
    
    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/deals/api/toggle-favorite/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update button state
            if (data.is_favorited) {
                icon.className = 'bi bi-heart-fill text-danger fs-5';
                button.classList.add('favorited');
            } else {
                icon.className = 'bi bi-heart fs-5';
                button.classList.remove('favorited');
            }
            
            // Update favorites count in navbar
            updateFavoritesCount(data.is_favorited);
            
            // Show success message
            showAlert(data.message, 'success');
        } else {
            // Restore original icon
            icon.className = originalIcon;
            showAlert(data.message, 'danger');
        }
    })
    .catch(error => {
        console.error('Favorite toggle error:', error);
        icon.className = originalIcon;
        showAlert('An error occurred. Please try again.', 'danger');
    });
}

/**
 * Update favorites count in navbar
 */
function updateFavoritesCount(isAdded) {
    const favoritesLink = document.querySelector('a[href*="favorites"]');
    if (!favoritesLink) return;
    
    const badge = favoritesLink.querySelector('.badge');
    let currentCount = badge ? parseInt(badge.textContent) : 0;
    
    if (isAdded) {
        currentCount++;
        if (badge) {
            badge.textContent = currentCount;
        } else {
            favoritesLink.innerHTML += ` <span class="badge bg-danger">${currentCount}</span>`;
        }
    } else {
        currentCount--;
        if (currentCount <= 0) {
            if (badge) badge.remove();
        } else {
            badge.textContent = currentCount;
        }
    }
}

/**
 * Newsletter subscription functionality
 */
function initializeNewsletterForms() {
    // Handle footer newsletter form
    const footerForm = document.getElementById('newsletterForm');
    if (footerForm) {
        footerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            handleNewsletterSubscription(this, 'newsletterMessage');
        });
    }
    
    // Handle home page newsletter form
    const homeForm = document.getElementById('homeNewsletterForm');
    if (homeForm) {
        homeForm.addEventListener('submit', function(event) {
            event.preventDefault();
            handleNewsletterSubscription(this, 'homeNewsletterMessage');
        });
    }
}

/**
 * Handle newsletter subscription
 */
function handleNewsletterSubscription(form, messageElementId) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    const messageElement = document.getElementById(messageElementId);
    
    // Show loading state
    const originalButtonContent = submitButton.innerHTML;
    submitButton.innerHTML = '<div class="loading-spinner"></div>';
    submitButton.disabled = true;
    
    fetch('/marketing/api/subscribe/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            form.reset();
            showMessage(messageElement, data.message, 'success');
        } else {
            showMessage(messageElement, data.message, 'danger');
        }
    })
    .catch(error => {
        console.error('Newsletter subscription error:', error);
        showMessage(messageElement, 'An error occurred. Please try again.', 'danger');
    })
    .finally(() => {
        // Restore button
        submitButton.innerHTML = originalButtonContent;
        submitButton.disabled = false;
    });
}

/**
 * Show message in specific element
 */
function showMessage(element, message, type) {
    if (!element) return;
    
    element.innerHTML = `<div class="alert alert-${type} alert-sm">${message}</div>`;
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        element.innerHTML = '';
    }, 5000);
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    // Create alert element
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Find or create alerts container
    let alertsContainer = document.querySelector('.alerts-container');
    if (!alertsContainer) {
        alertsContainer = document.createElement('div');
        alertsContainer.className = 'alerts-container position-fixed top-0 end-0 p-3';
        alertsContainer.style.zIndex = '9999';
        document.body.appendChild(alertsContainer);
    }
    
    // Add alert
    const alertElement = document.createElement('div');
    alertElement.innerHTML = alertHTML;
    alertsContainer.appendChild(alertElement.firstElementChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        const alert = alertsContainer.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    // Add tooltips to favorite buttons
    document.querySelectorAll('.favorite-btn').forEach(button => {
        const isAuthenticated = document.body.dataset.userAuthenticated;
        const tooltipText = isAuthenticated 
            ? (button.classList.contains('favorited') ? 'Remove from favorites' : 'Add to favorites')
            : 'Login to add favorites';
        
        button.setAttribute('data-bs-toggle', 'tooltip');
        button.setAttribute('title', tooltipText);
    });
}

/**
 * Scroll to top functionality
 */
function initializeScrollToTop() {
    // Create scroll to top button
    const scrollButton = document.createElement('button');
    scrollButton.innerHTML = '<i class="bi bi-arrow-up"></i>';
    scrollButton.className = 'btn btn-primary position-fixed bottom-0 end-0 m-3 rounded-circle scroll-to-top';
    scrollButton.style.display = 'none';
    scrollButton.style.zIndex = '9998';
    scrollButton.style.width = '50px';
    scrollButton.style.height = '50px';
    
    document.body.appendChild(scrollButton);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    });
    
    // Handle click
    scrollButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/**
 * Utility function to get CSRF token
 */
function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

/**
 * Utility function to format currency
 */
function formatCurrency(amount, currency = '$') {
    return `${currency}${parseFloat(amount).toFixed(2)}`;
}

/**
 * Utility function to debounce function calls
 */
function debounce(func, wait) {
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

/**
 * Image lazy loading
 */
function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Initialize lazy loading when DOM is ready
document.addEventListener('DOMContentLoaded', initializeLazyLoading);