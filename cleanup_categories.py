"""
Clean up Electronics and Books categories
"""
import sys
import os

# Add the project root to Python path
sys.path.append('.')

from app.database import get_db, engine
from app.models.models import Category, Product
from sqlalchemy.orm import sessionmaker

# Create a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def cleanup_categories():
    db = SessionLocal()
    try:
        # Get Electronics and Books categories
        electronics_cat = db.query(Category).filter(Category.name == 'Electronics').first()
        books_cat = db.query(Category).filter(Category.name == 'Books').first()
        clothing_cat = db.query(Category).filter(Category.name == 'Clothing').first()
        
        print("Current categories in database:")
        all_categories = db.query(Category).all()
        for cat in all_categories:
            product_count = len(cat.products)
            print(f"- {cat.name} (ID: {cat.id}) - {product_count} products")
        
        # Reassign Electronics products to Clothing (or you can choose another category)
        if electronics_cat:
            electronics_products = electronics_cat.products
            print(f"\nReassigning {len(electronics_products)} Electronics products to Clothing...")
            for product in electronics_products:
                product.categories.remove(electronics_cat)
                if clothing_cat and clothing_cat not in product.categories:
                    product.categories.append(clothing_cat)
                print(f"✅ Reassigned: {product.name}")
        
        # Reassign Books products to Clothing (or you can choose another category)
        if books_cat:
            books_products = books_cat.products
            print(f"\nReassigning {len(books_products)} Books products to Clothing...")
            for product in books_products:
                product.categories.remove(books_cat)
                if clothing_cat and clothing_cat not in product.categories:
                    product.categories.append(clothing_cat)
                print(f"✅ Reassigned: {product.name}")
        
        # Deactivate or delete the unwanted categories
        if electronics_cat:
            electronics_cat.is_active = False
            print(f"✅ Deactivated Electronics category")
            
        if books_cat:
            books_cat.is_active = False
            print(f"✅ Deactivated Books category")
        
        # Commit changes
        db.commit()
        
        print("\nUpdated categories (active only):")
        active_categories = db.query(Category).filter(Category.is_active == True).all()
        for cat in active_categories:
            product_count = len(cat.products)
            print(f"- {cat.name} (ID: {cat.id}) - {product_count} products")
        
        print(f"\nTotal active categories: {len(active_categories)}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_categories()