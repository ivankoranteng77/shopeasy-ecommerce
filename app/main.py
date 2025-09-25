from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
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
    title="E-Commerce API",
    description="A comprehensive e-commerce backend API",
    version="1.0.0",
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.get("/")
async def root():
    return {"message": "E-Commerce API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.environment}


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["admin-authentication"])
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(cart.router, prefix="/api/v1/cart", tags=["cart"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])