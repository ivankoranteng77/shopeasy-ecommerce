from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import CartItem, Product
from app.schemas.schemas import CartItem as CartItemSchema, CartItemCreate, CartItemUpdate

router = APIRouter()


@router.get("/{session_id}", response_model=List[CartItemSchema])
def get_cart_items(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get cart items for a guest session."""
    cart_items = db.query(CartItem).filter(CartItem.session_id == session_id).all()
    return cart_items


@router.post("/", response_model=CartItemSchema)
def add_to_cart(
    cart_item: CartItemCreate,
    db: Session = Depends(get_db)
):
    """Add item to guest cart or update quantity if item already exists."""
    # Check if product exists and is active
    product = db.query(Product).filter(
        Product.id == cart_item.product_id,
        Product.is_active == True
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if item already in cart
    existing_item = db.query(CartItem).filter(
        CartItem.session_id == cart_item.session_id,
        CartItem.product_id == cart_item.product_id
    ).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        # Create new cart item
        db_cart_item = CartItem(
            session_id=cart_item.session_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        db.add(db_cart_item)
        db.commit()
        db.refresh(db_cart_item)
        return db_cart_item


@router.put("/{cart_item_id}", response_model=CartItemSchema)
def update_cart_item(
    cart_item_id: int,
    cart_item_update: CartItemUpdate,
    session_id: str,
    db: Session = Depends(get_db)
):
    """Update cart item quantity."""
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.session_id == session_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    cart_item.quantity = cart_item_update.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.delete("/{cart_item_id}")
def remove_from_cart(
    cart_item_id: int,
    session_id: str,
    db: Session = Depends(get_db)
):
    """Remove item from cart."""
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.session_id == session_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}


@router.delete("/{session_id}/clear")
def clear_cart(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Clear all items from cart."""
    db.query(CartItem).filter(CartItem.session_id == session_id).delete()
    db.commit()
    return {"message": "Cart cleared successfully"}


@router.get("/{session_id}/total")
def get_cart_total(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get cart total amount."""
    cart_items = db.query(CartItem).filter(CartItem.session_id == session_id).all()
    
    total = 0
    item_count = 0
    
    for item in cart_items:
        total += item.product.price * item.quantity
        item_count += item.quantity
    
    return {
        "total_amount": total,
        "item_count": item_count,
        "items": len(cart_items)
    }