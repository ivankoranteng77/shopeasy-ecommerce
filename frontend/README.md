# ShopEasy Frontend

A modern, responsive e-commerce frontend built with HTML, CSS, and JavaScript that connects to your FastAPI backend.

## Features

### 🛒 **Guest Shopping Experience**

- **No Registration Required**: Customers can shop immediately
- **Product Browsing**: View products with categories, search, and filtering
- **Shopping Cart**: Session-based cart that persists in browser
- **Easy Checkout**: Simple form with just name, phone, and address
- **Order Confirmation**: Instant feedback with order details

### 🎨 **Modern Design**

- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Bootstrap 5**: Professional, clean interface
- **Smooth Animations**: Hover effects and transitions
- **Category Colors**: Visual distinction for different product types
- **Loading States**: User-friendly loading indicators

### ⚡ **Smart Features**

- **Real-time Search**: Instant product filtering as you type
- **Category Filtering**: Filter products by category
- **Stock Management**: Shows stock levels and prevents overselling
- **Cart Persistence**: Cart contents saved in browser storage
- **Toast Notifications**: User feedback for actions

## Getting Started

### 1. Start the Backend

Make sure your FastAPI backend is running:

```bash
# From the main application directory
venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Backend should be available at: http://127.0.0.1:8000

### 2. Serve the Frontend

**Option A: Using Python Server (Recommended)**

```bash
# From the main application directory
venv\Scripts\python.exe serve_frontend.py
```

**Option B: Using any HTTP server**

```bash
# Navigate to frontend directory
cd frontend

# Using Python's built-in server
python -m http.server 3000

# Or using Node.js (if installed)
npx serve -p 3000

# Or using PHP (if installed)
php -S localhost:3000
```

### 3. Open in Browser

Visit: http://localhost:3000

## File Structure

```
frontend/
├── index.html          # Main HTML page
├── app.js             # JavaScript functionality
├── style.css          # Custom styles
└── README.md          # This file
```

## How It Works

### Customer Journey

1. **Browse Products**: View all products or filter by category
2. **Search**: Use the search bar to find specific items
3. **Add to Cart**: Click "Add to Cart" on desired products
4. **View Cart**: Click cart icon to see selected items
5. **Adjust Quantities**: Modify quantities in the cart
6. **Checkout**: Click "Checkout" and fill in delivery details
7. **Place Order**: Submit order (goes to admin's WhatsApp)

### Technical Flow

1. **Frontend** loads products from `GET /api/v1/products`
2. **Cart** is managed in browser localStorage
3. **Categories** loaded from `GET /api/v1/products/categories`
4. **Orders** submitted to `POST /api/v1/orders`
5. **Admin** receives WhatsApp notification (when configured)

## API Integration

The frontend communicates with these backend endpoints:

- `GET /api/v1/products` - Fetch all products
- `GET /api/v1/products/categories` - Fetch categories
- `POST /api/v1/orders` - Place guest order

## Customization

### Branding

- Update `<title>` and navbar brand in `index.html`
- Modify colors in `style.css` CSS variables
- Replace company info in footer

### Product Images

- Real product images can be added to the `product.image_url` field
- The frontend will display them automatically
- Currently shows category-colored placeholder boxes

### Categories

- Category colors are defined in `style.css`
- Add new category classes for custom styling
- Colors auto-assigned based on category names

## Browser Compatibility

- ✅ Chrome/Edge 88+
- ✅ Firefox 85+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Features

- **Lazy Loading**: Products load efficiently
- **Local Storage**: Cart persists between visits
- **Minimal Dependencies**: Only Bootstrap and Font Awesome CDNs
- **Optimized Images**: Placeholder system for fast loading

## Security Notes

- Frontend runs on different port from API (CORS enabled)
- No sensitive data stored in browser
- All order data sent securely to backend
- Input validation on both frontend and backend

## Troubleshooting

### Common Issues

**Products not loading:**

- Check if backend is running on http://127.0.0.1:8000
- Verify API endpoints are accessible
- Check browser console for errors

**Cart not working:**

- Enable localStorage in browser settings
- Check if JavaScript is enabled
- Clear browser cache and try again

**CORS errors:**

- Ensure backend has CORS middleware enabled
- Check API base URL in `app.js`
- Try serving frontend from different port

### Browser Console

Press F12 and check Console tab for error messages and debugging info.

## Next Steps

1. **Add Real Images**: Upload product images and update image URLs
2. **Custom Styling**: Modify colors and layout to match your brand
3. **Enhanced Features**: Add product reviews, wishlists, or recommendations
4. **PWA Features**: Add service worker for offline functionality
5. **Analytics**: Integrate Google Analytics or similar tracking
