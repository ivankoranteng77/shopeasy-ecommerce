// ShopEasy Frontend JavaScript
class ShopEasy {
    constructor() {
        this.apiBaseUrl = 'http://127.0.0.1:8003/api/v1';
        this.cart = this.loadCart();
        this.products = [];
        this.categories = [];
        this.currentCategory = 'all';
        this.searchQuery = '';
        
        this.init();
    }

    init() {
        console.log('ShopEasy init() called');
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
        const statusEl = document.getElementById('debugStatus');
        const countEl = document.getElementById('debugProductCount');
        const urlEl = document.getElementById('debugApiUrl');
        
        if (statusEl) statusEl.textContent = status;
        if (countEl) countEl.textContent = this.products.length;
        if (urlEl) urlEl.textContent = this.apiBaseUrl;
    }

    setupEventListeners() {
        // Search functionality
        document.getElementById('searchInput').addEventListener('input', (e) => {
            this.searchQuery = e.target.value.toLowerCase();
            this.filterProducts();
        });

        // Cart button
        document.getElementById('cartBtn').addEventListener('click', () => {
            this.updateCartDisplay();
        });

        // Checkout button
        document.getElementById('checkoutBtn').addEventListener('click', () => {
            this.showCheckoutModal();
        });

        // Place order button
        document.getElementById('placeOrderBtn').addEventListener('click', () => {
            this.placeOrder();
        });
    }

    async loadCategories() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/products/categories/`);
            if (response.ok) {
                this.categories = await response.json();
                this.renderCategoryFilter();
            }
        } catch (error) {
            console.error('Error loading categories:', error);
        }
    }

    async loadProducts() {
        try {
            console.log('Loading products from:', `${this.apiBaseUrl}/products/`);
            this.updateDebugInfo('Fetching products from API...');
            document.getElementById('loadingSpinner').style.display = 'block';
            document.getElementById('productsGrid').style.display = 'none';
            document.getElementById('noProducts').style.display = 'none';

            const response = await fetch(`${this.apiBaseUrl}/products/`);
            console.log('Products API response:', response.status, response.ok);
            
            if (response.ok) {
                this.products = await response.json();
                console.log('Products loaded:', this.products.length, 'products');
                console.log('First product:', this.products[0]);
                this.updateDebugInfo(`Loaded ${this.products.length} products, rendering...`);
                this.renderProducts();
                this.updateDebugInfo(`Successfully displayed ${this.products.length} products`);
            } else {
                throw new Error('Failed to load products');
            }
        } catch (error) {
            console.error('Error loading products:', error);
            this.updateDebugInfo(`Error: ${error.message}`);
            this.showError('Failed to load products. Please try again later.');
        } finally {
            document.getElementById('loadingSpinner').style.display = 'none';
        }
    }

    renderCategoryFilter() {
        const container = document.getElementById('categoryFilter');
        const allButton = container.querySelector('[data-category="all"]');
        
        this.categories.forEach(category => {
            const button = document.createElement('button');
            button.className = 'btn btn-outline-primary category-btn';
            button.dataset.category = category.id;
            button.textContent = category.name;
            button.addEventListener('click', () => this.filterByCategory(category.id));
            container.appendChild(button);
        });

        // Add event listener for "All Products" button
        allButton.addEventListener('click', () => this.filterByCategory('all'));
    }

    renderProducts() {
        console.log('Rendering products...');
        const container = document.getElementById('productsGrid');
        container.innerHTML = '';

        const filteredProducts = this.getFilteredProducts();
        console.log('Filtered products:', filteredProducts.length);

        if (filteredProducts.length === 0) {
            console.log('No products to display');
            document.getElementById('productsGrid').style.display = 'none';
            document.getElementById('noProducts').style.display = 'block';
            return;
        }

        console.log('Displaying products grid');
        document.getElementById('productsGrid').style.display = 'flex';
        document.getElementById('noProducts').style.display = 'none';

        filteredProducts.forEach(product => {
            console.log('Creating card for product:', product.name);
            const productCard = this.createProductCard(product);
            container.appendChild(productCard);
        });
    }

    createProductCard(product) {
        const col = document.createElement('div');
        col.className = 'col-lg-3 col-md-4 col-sm-6 fade-in-up';

        const categoryClass = this.getCategoryClass(product.categories);
        const isInStock = product.stock_quantity > 0;
        const stockBadge = isInStock 
            ? `<span class="badge bg-success stock-badge">In Stock (${product.stock_quantity})</span>`
            : '<span class="badge bg-danger stock-badge">Out of Stock</span>';

        col.innerHTML = `
            <div class="card product-card h-100">
                <div class="product-image ${categoryClass} position-relative">
                    <i class="fas fa-box"></i>
                    ${stockBadge}
                </div>
                <div class="card-body">
                    <h5 class="card-title product-title">${product.name}</h5>
                    <div class="product-price">$${product.price.toFixed(2)}</div>
                    <p class="product-description">${product.description}</p>
                    <div class="mt-auto">
                        <button class="btn btn-primary w-100 add-to-cart-btn" 
                                onclick="shopEasy.addToCart(${product.id})" 
                                ${!isInStock ? 'disabled' : ''}>
                            <i class="fas fa-cart-plus me-2"></i>
                            ${isInStock ? 'Add to Cart' : 'Out of Stock'}
                        </button>
                    </div>
                </div>
            </div>
        `;

        return col;
    }

    getCategoryClass(categories) {
        if (!categories || categories.length === 0) return 'category-default';
        
        const categoryName = categories[0].name.toLowerCase();
        if (categoryName.includes('electronic')) return 'category-electronics';
        if (categoryName.includes('clothing')) return 'category-clothing';
        if (categoryName.includes('book')) return 'category-books';
        if (categoryName.includes('home') || categoryName.includes('garden')) return 'category-home';
        if (categoryName.includes('sport')) return 'category-sports';
        return 'category-default';
    }

    getFilteredProducts() {
        let filtered = this.products;

        // Filter by category
        if (this.currentCategory !== 'all') {
            filtered = filtered.filter(product => 
                product.categories.some(cat => cat.id == this.currentCategory)
            );
        }

        // Filter by search query
        if (this.searchQuery) {
            filtered = filtered.filter(product =>
                product.name.toLowerCase().includes(this.searchQuery) ||
                product.description.toLowerCase().includes(this.searchQuery)
            );
        }

        return filtered;
    }

    filterByCategory(categoryId) {
        this.currentCategory = categoryId;
        
        // Update active button
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-category="${categoryId}"]`).classList.add('active');
        
        this.renderProducts();
    }

    filterProducts() {
        this.renderProducts();
    }

    addToCart(productId) {
        const product = this.products.find(p => p.id === productId);
        if (!product || product.stock_quantity <= 0) {
            this.showError('Product is out of stock!');
            return;
        }

        const existingItem = this.cart.find(item => item.product_id === productId);
        
        if (existingItem) {
            if (existingItem.quantity < product.stock_quantity) {
                existingItem.quantity += 1;
                this.showSuccess(`Added another ${product.name} to cart!`);
            } else {
                this.showError(`Cannot add more ${product.name}. Stock limit reached.`);
                return;
            }
        } else {
            this.cart.push({
                product_id: productId,
                product: product,
                quantity: 1
            });
            this.showSuccess(`${product.name} added to cart!`);
        }

        this.saveCart();
        this.updateCartUI();
    }

    removeFromCart(productId) {
        this.cart = this.cart.filter(item => item.product_id !== productId);
        this.saveCart();
        this.updateCartUI();
        this.updateCartDisplay();
    }

    updateCartQuantity(productId, newQuantity) {
        const item = this.cart.find(item => item.product_id === productId);
        if (item) {
            if (newQuantity <= 0) {
                this.removeFromCart(productId);
            } else if (newQuantity <= item.product.stock_quantity) {
                item.quantity = newQuantity;
                this.saveCart();
                this.updateCartUI();
                this.updateCartDisplay();
            } else {
                this.showError(`Only ${item.product.stock_quantity} items available in stock.`);
            }
        }
    }

    updateCartUI() {
        const cartCount = document.getElementById('cartCount');
        const checkoutBtn = document.getElementById('checkoutBtn');
        
        const totalItems = this.cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.textContent = totalItems;
        
        checkoutBtn.disabled = totalItems === 0;
        
        if (totalItems === 0) {
            cartCount.style.display = 'none';
        } else {
            cartCount.style.display = 'inline';
        }
    }

    updateCartDisplay() {
        const cartItems = document.getElementById('cartItems');
        const emptyCart = document.getElementById('emptyCart');
        const cartTotal = document.getElementById('cartTotal');

        if (this.cart.length === 0) {
            cartItems.style.display = 'none';
            emptyCart.style.display = 'block';
            cartTotal.textContent = '0.00';
            return;
        }

        cartItems.style.display = 'block';
        emptyCart.style.display = 'none';

        cartItems.innerHTML = this.cart.map(item => `
            <div class="cart-item">
                <div class="row align-items-center">
                    <div class="col-3">
                        <div class="cart-item-image ${this.getCategoryClass(item.product.categories)}">
                            <i class="fas fa-box"></i>
                        </div>
                    </div>
                    <div class="col-9">
                        <h6 class="mb-1">${item.product.name}</h6>
                        <div class="text-muted small mb-2">$${item.product.price.toFixed(2)} each</div>
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="quantity-controls">
                                <button onclick="shopEasy.updateCartQuantity(${item.product_id}, ${item.quantity - 1})">
                                    <i class="fas fa-minus"></i>
                                </button>
                                <input type="number" value="${item.quantity}" min="1" max="${item.product.stock_quantity}"
                                       onchange="shopEasy.updateCartQuantity(${item.product_id}, parseInt(this.value))">
                                <button onclick="shopEasy.updateCartQuantity(${item.product_id}, ${item.quantity + 1})">
                                    <i class="fas fa-plus"></i>
                                </button>
                            </div>
                            <button class="btn btn-sm btn-outline-danger" 
                                    onclick="shopEasy.removeFromCart(${item.product_id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                        <div class="text-end mt-2">
                            <strong>$${(item.product.price * item.quantity).toFixed(2)}</strong>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        const total = this.cart.reduce((sum, item) => sum + (item.product.price * item.quantity), 0);
        cartTotal.textContent = total.toFixed(2);
    }

    showCheckoutModal() {
        this.updateCartDisplay();
        
        // Update checkout summary
        const checkoutItems = document.getElementById('checkoutItems');
        const checkoutTotal = document.getElementById('checkoutTotal');

        checkoutItems.innerHTML = this.cart.map(item => `
            <div class="d-flex justify-content-between mb-2">
                <span>${item.product.name} × ${item.quantity}</span>
                <span>$${(item.product.price * item.quantity).toFixed(2)}</span>
            </div>
        `).join('');

        const total = this.cart.reduce((sum, item) => sum + (item.product.price * item.quantity), 0);
        checkoutTotal.textContent = total.toFixed(2);

        const modal = new bootstrap.Modal(document.getElementById('checkoutModal'));
        modal.show();
    }

    async placeOrder() {
        const form = document.getElementById('checkoutForm');
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        const orderData = {
            customer_name: document.getElementById('customerName').value,
            customer_phone: document.getElementById('customerPhone').value,
            customer_address: document.getElementById('customerAddress').value,
            notes: document.getElementById('orderNotes').value || null,
            items: this.cart.map(item => ({
                product_id: item.product_id,
                quantity: item.quantity,
                price: item.product.price
            }))
        };

        try {
            document.getElementById('placeOrderBtn').disabled = true;
            document.getElementById('placeOrderBtn').innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Placing Order...';

            const response = await fetch(`${this.apiBaseUrl}/orders/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(orderData)
            });

            if (response.ok) {
                const result = await response.json();
                this.cart = [];
                this.saveCart();
                this.updateCartUI();
                
                // Hide checkout modal
                const checkoutModal = bootstrap.Modal.getInstance(document.getElementById('checkoutModal'));
                checkoutModal.hide();
                
                // Show success modal
                document.getElementById('orderIdDisplay').textContent = result.id;
                const successModal = new bootstrap.Modal(document.getElementById('successModal'));
                successModal.show();
                
                // Clear form
                form.reset();
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to place order');
            }
        } catch (error) {
            console.error('Order placement error:', error);
            this.showError('Failed to place order. Please try again.');
        } finally {
            document.getElementById('placeOrderBtn').disabled = false;
            document.getElementById('placeOrderBtn').innerHTML = '<i class="fas fa-check me-2"></i>Place Order';
        }
    }

    loadCart() {
        const savedCart = localStorage.getItem('shopEasy_cart');
        return savedCart ? JSON.parse(savedCart) : [];
    }

    saveCart() {
        localStorage.setItem('shopEasy_cart', JSON.stringify(this.cart));
    }

    showSuccess(message) {
        this.showToast(message, 'success');
    }

    showError(message) {
        this.showToast(message, 'danger');
    }

    showToast(message, type = 'info') {
        const toastContainer = this.getOrCreateToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
        bsToast.show();
        
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    getOrCreateToastContainer() {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }
        return container;
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    try {
        console.log('DOM loaded, initializing ShopEasy...');
        const shopEasy = new ShopEasy();
        console.log('ShopEasy initialized successfully');
        window.shopEasy = shopEasy; // Make it globally available for debugging
    } catch (error) {
        console.error('Failed to initialize ShopEasy:', error);
        document.body.innerHTML = '<div style="color: red; padding: 20px;"><h1>Error</h1><p>Failed to initialize application: ' + error.message + '</p></div>';
    }
});

// Admin Login Functionality
class AdminLogin {
    constructor() {
        this.apiBaseUrl = 'http://127.0.0.1:8003/api/v1';
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Admin login form handler
        document.getElementById('adminLoginForm').addEventListener('submit', (e) => {
            this.handleAdminLogin(e);
        });
    }

    async handleAdminLogin(e) {
        e.preventDefault();
        
        const username = document.getElementById('adminUsername').value;
        const password = document.getElementById('adminPassword').value;
        const errorDiv = document.getElementById('adminLoginError');
        
        // Hide any previous errors
        errorDiv.style.display = 'none';
        
        // Show loading state
        const submitBtn = e.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Logging in...';
        submitBtn.disabled = true;
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/auth/admin/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Store the token
                localStorage.setItem('adminToken', data.access_token);
                
                // Show success message
                this.showSuccessToast('Login successful! Redirecting to admin panel...');
                
                // Close modal and redirect to admin panel
                const modal = bootstrap.Modal.getInstance(document.getElementById('adminLoginModal'));
                modal.hide();
                
                // Small delay for better UX
                setTimeout(() => {
                    window.location.href = 'admin.html';
                }, 1000);
                
            } else {
                const error = await response.json();
                this.showError(error.detail || 'Login failed. Please check your credentials.');
            }
        } catch (error) {
            this.showError('Network error. Please check if the server is running.');
        } finally {
            // Reset button state
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }

    showError(message) {
        const errorDiv = document.getElementById('adminLoginError');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }

    showSuccessToast(message) {
        // Create and show a success toast
        const toastHtml = `
            <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header bg-success text-white">
                    <i class="fas fa-check-circle me-2"></i>
                    <strong class="me-auto">Success</strong>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;
        
        const container = this.getToastContainer();
        container.insertAdjacentHTML('beforeend', toastHtml);
        
        const toastElement = container.lastElementChild;
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Remove toast after it's hidden
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }

    getToastContainer() {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }
        return container;
    }
}

// Initialize admin login functionality
document.addEventListener('DOMContentLoaded', function() {
    const adminLogin = new AdminLogin();
});