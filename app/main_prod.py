from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
import os

# Try production config first, fallback to dev config
try:
    from app.config_prod import settings
except ImportError:
    from app.config import settings

from app.database import engine
from app.models import models
from app.utils.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from app.utils.middleware import LoggingMiddleware

# Import routers
from app.routers import auth, products, cart, orders

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ShopEasy E-Commerce API",
    description="A comprehensive e-commerce backend API",
    version="1.0.0",
    debug=settings.debug
)

# CORS middleware with production settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins if hasattr(settings, 'allowed_origins') else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Serve static files (for production)
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(cart.router, prefix="/api/v1/cart", tags=["Shopping Cart"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])

@app.get("/")
async def root():
    return {
        "message": "ShopEasy E-Commerce API", 
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)