// Admin Panel JavaScript
const API_BASE = 'http://127.0.0.1:8003';
let authToken = localStorage.getItem('adminToken');

// Check if already logged in
document.addEventListener('DOMContentLoaded', function() {
    if (authToken) {
        showAdminPanel();
        loadProducts();
        loadOrders();
    }
});

// Login form handler
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_BASE}/api/v1/auth/admin/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        });
        
        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            localStorage.setItem('adminToken', authToken);
            document.getElementById('adminName').textContent = username;
            showAdminPanel();
            loadProducts();
            loadOrders();
        } else {
            const error = await response.json();
            showError(error.detail || 'Login failed');
        }
    } catch (error) {
        showError('Network error. Please check if the backend server is running.');
    }
});

// Logout handler
document.getElementById('logoutBtn').addEventListener('click', function() {
    localStorage.removeItem('adminToken');
    authToken = null;
    showLoginForm();
});

// Add product form handler
document.getElementById('addProductForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const categoryName = document.getElementById('productCategory').value;
    const categoryId = await getCategoryId(categoryName);
    
    const productData = {
        name: document.getElementById('productName').value,
        sku: document.getElementById('productSku').value,
        description: document.getElementById('productDescription').value,
        price: parseFloat(document.getElementById('productPrice').value),
        stock_quantity: parseInt(document.getElementById('productStock').value),
        category_ids: categoryId ? [categoryId] : [],
        image_url: document.getElementById('productImage').value || null
    };
    
    try {
        const response = await fetch(`${API_BASE}/api/v1/products/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(productData)
        });
        
        if (response.ok) {
            alert('Product added successfully!');
            document.getElementById('addProductForm').reset();
            loadProducts(); // Refresh products list
        } else {
            const error = await response.json();
            alert('Error adding product: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    }
});

// Helper functions
function showAdminPanel() {
    document.getElementById('loginSection').style.display = 'none';
    document.getElementById('adminPanel').style.display = 'block';
}

function showLoginForm() {
    document.getElementById('loginSection').style.display = 'block';
    document.getElementById('adminPanel').style.display = 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('loginError');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// Load products
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE}/api/v1/products/`);
        const products = await response.json();
        
        const tbody = document.getElementById('productsTable');
        tbody.innerHTML = products.map(product => `
            <tr>
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>$${product.price}</td>
                <td>${product.stock_quantity}</td>
                <td>${product.category?.name || 'N/A'}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick="editProduct(${product.id})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteProduct(${product.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

// Load orders
async function loadOrders() {
    try {
        const response = await fetch(`${API_BASE}/api/v1/orders/admin/all`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            const orders = await response.json();
            
            const tbody = document.getElementById('ordersTable');
            tbody.innerHTML = orders.map(order => `
                <tr>
                    <td>#${order.order_number}</td>
                    <td>${order.customer_name}</td>
                    <td>${order.customer_phone}</td>
                    <td>$${order.total_amount}</td>
                    <td><span class="badge bg-${getStatusColor(order.status)}">${order.status}</span></td>
                    <td>${new Date(order.created_at).toLocaleDateString()}</td>
                    <td>
                        ${order.whatsapp_sent ? 
                            '<span class="badge bg-success">Sent</span>' : 
                            '<span class="badge bg-warning">Pending</span>'
                        }
                    </td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading orders:', error);
    }
}

// Get category ID (create if doesn't exist)
async function getCategoryId(categoryName) {
    if (!categoryName || categoryName === '') {
        return null;
    }
    
    try {
        // Try to get existing categories
        const response = await fetch(`${API_BASE}/api/v1/products/categories`);
        if (response.ok) {
            const categories = await response.json();
            const existingCategory = categories.find(cat => cat.name === categoryName);
            if (existingCategory) {
                return existingCategory.id;
            }
        }
        
        // Create new category if doesn't exist
        const createResponse = await fetch(`${API_BASE}/api/v1/products/categories/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ name: categoryName, description: categoryName })
        });
        
        if (createResponse.ok) {
            const newCategory = await createResponse.json();
            return newCategory.id;
        }
        
        console.error('Failed to create category');
        return null;
    } catch (error) {
        console.error('Error with category:', error);
        return null;
    }
}

// Delete product
async function deleteProduct(productId) {
    if (confirm('Are you sure you want to delete this product?')) {
        try {
            const response = await fetch(`${API_BASE}/api/v1/products/${productId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${authToken}`
                }
            });
            
            if (response.ok) {
                alert('Product deleted successfully!');
                loadProducts(); // Refresh products list
            } else {
                alert('Error deleting product');
            }
        } catch (error) {
            alert('Network error: ' + error.message);
        }
    }
}

// Edit product (placeholder - you can expand this)
function editProduct(productId) {
    alert(`Edit functionality for product ${productId} - to be implemented`);
}

// Get status color for badge
function getStatusColor(status) {
    switch(status) {
        case 'pending': return 'warning';
        case 'confirmed': return 'success';
        case 'shipped': return 'info';
        case 'delivered': return 'success';
        case 'cancelled': return 'danger';
        default: return 'secondary';
    }
}