from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime
from app.database import get_db
from app.models.models import Order, OrderItem, CartItem, Product, Admin
from app.schemas.schemas import (
    Order as OrderSchema,
    GuestOrderCreate,
    OrderUpdate,
    OrderStatus
)
from app.utils.dependencies import get_current_admin_user
from app.utils.whatsapp import send_order_notification, send_order_status_update

router = APIRouter()


def generate_order_number() -> str:
    """Generate unique order number."""
    return f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"


@router.post("/", response_model=OrderSchema)
def create_guest_order(
    order: GuestOrderCreate,
    db: Session = Depends(get_db)
):
    """Create order from guest cart items or direct items."""
    order_items_data = []
    
    if order.items:
        # Direct items from frontend (localStorage cart)
        total_amount = 0
        
        for item_input in order.items:
            # Get product and validate
            product = db.query(Product).filter(Product.id == item_input.product_id).first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id {item_input.product_id} not found"
                )
            
            if not product.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product {product.name} is no longer available"
                )
            
            # Check stock availability
            if product.stock_quantity < item_input.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough stock for {product.name}. Available: {product.stock_quantity}"
                )
            
            # Calculate item total
            item_total = item_input.price * item_input.quantity
            total_amount += item_total
            
            order_items_data.append({
                'product_id': product.id,
                'quantity': item_input.quantity,
                'price': item_input.price
            })
            
    elif order.session_id:
        # Session-based cart items
        cart_items = db.query(CartItem).filter(CartItem.session_id == order.session_id).all()
        
        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty"
            )
        
        # Calculate total amount and validate stock
        total_amount = 0
        
        for cart_item in cart_items:
            product = cart_item.product
            
            # Check if product is active
            if not product.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product {product.name} is no longer available"
                )
            
            # Check stock availability
            if product.stock_quantity < cart_item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough stock for {product.name}. Available: {product.stock_quantity}"
                )
            
            # Calculate item total
    # Create order
    order_number = generate_order_number()
    db_order = Order(
        order_number=order_number,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        customer_address=order.customer_address,
        total_amount=total_amount,
        notes=order.notes
    )
    
    db.add(db_order)
    db.flush()  # Get the order ID
    
    # Create order items and update stock
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=db_order.id,
            product_id=item_data["product_id"],
            quantity=item_data["quantity"],
            price=item_data["price"]
        )
        db.add(order_item)
        
        # Update product stock
        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        product.stock_quantity -= item_data["quantity"]
    
    # Clear session cart if session_id was provided
    if order.session_id:
        db.query(CartItem).filter(CartItem.session_id == order.session_id).delete()
    
    db.commit()
    db.refresh(db_order)
    
    # Send WhatsApp notification to admin
    try:
        success = send_order_notification(db_order)
        if success:
            db_order.whatsapp_sent = True
            db.commit()
    except Exception as e:
        # Log error but don't fail the order
        print(f"Failed to send WhatsApp notification: {e}")
    
    return db_order


@router.get("/{order_number}", response_model=OrderSchema)
def get_order_by_number(
    order_number: str,
    customer_phone: str,
    db: Session = Depends(get_db)
):
    """Get order by order number and customer phone (for verification)."""
    order = db.query(Order).filter(
        Order.order_number == order_number,
        Order.customer_phone == customer_phone
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order


# Admin endpoints
@router.get("/admin/all", response_model=List[OrderSchema])
def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    current_admin: Admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all orders (admin only)."""
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status)
    
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders


@router.put("/admin/{order_id}", response_model=OrderSchema)
def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    current_admin: Admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update order status (admin only)."""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    old_status = order.status
    
    # Update order fields
    for field, value in order_update.dict(exclude_unset=True).items():
        setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    
    # Send WhatsApp status update to customer if status changed
    if order_update.status and order_update.status != old_status:
        try:
            send_order_status_update(order, order_update.status)
        except Exception as e:
            print(f"Failed to send WhatsApp status update: {e}")
    
    return order


@router.get("/admin/stats")
def get_order_stats(
    current_admin: Admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get order statistics (admin only)."""
    from sqlalchemy import func
    
    # Total orders
    total_orders = db.query(Order).count()
    
    # Orders by status
    status_counts = db.query(
        Order.status,
        func.count(Order.id).label('count')
    ).group_by(Order.status).all()
    
    # Total revenue
    total_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.status.in_(["confirmed", "preparing", "ready", "delivered"])
    ).scalar() or 0
    
    # Recent orders
    recent_orders = db.query(Order).order_by(Order.created_at.desc()).limit(10).all()
    
    return {
        "total_orders": total_orders,
        "status_breakdown": {status: count for status, count in status_counts},
        "total_revenue": total_revenue,
        "recent_orders": recent_orders
    }