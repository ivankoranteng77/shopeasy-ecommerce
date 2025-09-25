// Production configuration
const CONFIG = {
    // Auto-detect API URL based on environment
    API_BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? 'http://127.0.0.1:8003/api/v1'  // Development
        : 'https://your-api-domain.railway.app/api/v1', // Production - UPDATE THIS
    
    WHATSAPP_ENABLED: true,
    DEBUG: window.location.hostname === 'localhost'
};

// ShopEasy Frontend JavaScript - Production Ready
class ShopEasy {
    constructor() {
        this.apiBaseUrl = CONFIG.API_BASE_URL;
        this.cart = this.loadCart();
        this.products = [];
        this.categories = [];
        this.currentCategory = 'all';
        this.searchQuery = '';
        
        this.init();
    }

    init() {
        console.log('ShopEasy init() called');
        console.log('API Base URL:', this.apiBaseUrl);
        this.updateDebugInfo('Setting up event listeners...');
        this.setupEventListeners();
        this.updateDebugInfo('Updating cart UI...');
        this.updateCartUI();
        this.updateDebugInfo('Loading categories...');
        this.loadCategories();
        this.updateDebugInfo('Loading products...');
        this.loadProducts();
    }

    updateDebugInfo(status) {
        if (!CONFIG.DEBUG) return; // Only show debug in development
        
        const statusEl = document.getElementById('debugStatus');
        const countEl = document.getElementById('debugProductCount');
        const urlEl = document.getElementById('debugApiUrl');
        
        if (statusEl) statusEl.textContent = status;
        if (countEl) countEl.textContent = this.products.length;
        if (urlEl) urlEl.textContent = this.apiBaseUrl;
    }