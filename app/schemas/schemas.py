from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# Admin Schemas
class AdminBase(BaseModel):
    username: str
    email: EmailStr


class AdminCreate(AdminBase):
    password: str


class Admin(AdminBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class Category(CategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    sku: str
    stock_quantity: int = 0
    image_url: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

    @validator('stock_quantity')
    def stock_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Stock quantity cannot be negative')
        return v


class ProductCreate(ProductBase):
    category_ids: List[int] = []


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    category_ids: Optional[List[int]] = None

    @validator('price')
    def price_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Price must be positive')
        return v

    @validator('stock_quantity')
    def stock_must_be_non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError('Stock quantity cannot be negative')
        return v


class Product(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    categories: List[Category] = []

    class Config:
        from_attributes = True


# Cart Schemas (Guest Cart)
class CartItemBase(BaseModel):
    product_id: int
    quantity: int

    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v


class CartItemCreate(CartItemBase):
    session_id: str  # For guest cart identification


class CartItemUpdate(BaseModel):
    quantity: int

    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v


class CartItem(CartItemBase):
    id: int
    session_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    product: Product

    class Config:
        from_attributes = True


# Order Schemas (Guest Orders)
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    order_id: int
    created_at: datetime
    product: Product

    class Config:
        from_attributes = True


class OrderItemInput(BaseModel):
    product_id: int
    quantity: int
    price: float

    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v


class GuestOrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    customer_address: str
    notes: Optional[str] = None
    session_id: Optional[str] = None  # Optional for session-based cart
    items: Optional[List[OrderItemInput]] = None  # Direct items for frontend


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    notes: Optional[str] = None


class Order(BaseModel):
    id: int
    order_number: str
    customer_name: str
    customer_phone: str
    customer_address: str
    status: str
    total_amount: float
    notes: Optional[str] = None
    whatsapp_sent: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    order_items: List[OrderItem] = []

    class Config:
        from_attributes = True


# Authentication Schemas (Admin only)
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class AdminLogin(BaseModel):
    username: str
    password: str