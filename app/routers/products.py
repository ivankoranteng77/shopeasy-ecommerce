from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from app.database import get_db
from app.models.models import Product, Category
from app.schemas.schemas import (
    Product as ProductSchema,
    ProductCreate,
    ProductUpdate,
    Category as CategorySchema,
    CategoryCreate,
    CategoryUpdate
)
from app.utils.dependencies import get_current_admin_user

router = APIRouter()


# Product endpoints
@router.post("/", response_model=ProductSchema)
def create_product(
    product: ProductCreate,
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new product (admin only)."""
    # Check if SKU already exists
    existing_product = db.query(Product).filter(Product.sku == product.sku).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this SKU already exists"
        )
    
    # Create product
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        sku=product.sku,
        stock_quantity=product.stock_quantity,
        image_url=product.image_url,
        weight=product.weight,
        dimensions=product.dimensions
    )
    
    # Add categories
    if product.category_ids:
        categories = db.query(Category).filter(Category.id.in_(product.category_ids)).all()
        db_product.categories = categories
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product


@router.get("/", response_model=List[ProductSchema])
def read_products(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Search in product name and description"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    in_stock: Optional[bool] = Query(None, description="Filter products in stock"),
    db: Session = Depends(get_db)
):
    """Get products with filtering and search."""
    query = db.query(Product).filter(Product.is_active == True)
    
    # Search filter
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
        )
    
    # Category filter
    if category_id:
        query = query.join(Product.categories).filter(Category.id == category_id)
    
    # Price filters
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    # Stock filter
    if in_stock is not None:
        if in_stock:
            query = query.filter(Product.stock_quantity > 0)
        else:
            query = query.filter(Product.stock_quantity == 0)
    
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID."""
    product = db.query(Product).filter(
        and_(Product.id == product_id, Product.is_active == True)
    ).first()
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update product (admin only)."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update fields
    update_data = product_update.dict(exclude_unset=True, exclude={'category_ids'})
    for field, value in update_data.items():
        setattr(product, field, value)
    
    # Update categories if provided
    if product_update.category_ids is not None:
        categories = db.query(Category).filter(Category.id.in_(product_update.category_ids)).all()
        product.categories = categories
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete product (admin only)."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Soft delete by setting is_active to False
    product.is_active = False
    db.commit()
    return {"message": "Product deleted successfully"}


# Category endpoints
@router.post("/categories/", response_model=CategorySchema)
def create_category(
    category: CategoryCreate,
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new category (admin only)."""
    # Check if category already exists
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    
    db_category = Category(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.get("/categories/", response_model=List[CategorySchema])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all categories."""
    categories = db.query(Category).filter(Category.is_active == True).offset(skip).limit(limit).all()
    return categories


@router.get("/categories/{category_id}", response_model=CategorySchema)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Get category by ID."""
    category = db.query(Category).filter(
        and_(Category.id == category_id, Category.is_active == True)
    ).first()
    
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/categories/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update category (admin only)."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    for field, value in category_update.dict(exclude_unset=True).items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    return category


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete category (admin only)."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Soft delete by setting is_active to False
    category.is_active = False
    db.commit()
    return {"message": "Category deleted successfully"}