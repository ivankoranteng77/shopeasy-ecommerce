"""
Clean up Home & Garden and Sports categories - move products to Clothing
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

def cleanup_remaining_categories():
    db = SessionLocal()
    try:
        # Get the unwanted categories
        home_garden_cat = db.query(Category).filter(Category.name == 'Home & Garden').first()
        sports_cat = db.query(Category).filter(Category.name == 'Sports').first()
        clothing_cat = db.query(Category).filter(Category.name == 'Clothing').first()
        
        # Reassign Home & Garden products to Clothing
        if home_garden_cat:
            home_products = home_garden_cat.products
            print(f"Reassigning {len(home_products)} Home & Garden products to Clothing...")
            for product in home_products:
                product.categories.remove(home_garden_cat)
                if clothing_cat and clothing_cat not in product.categories:
                    product.categories.append(clothing_cat)
                print(f"✅ Reassigned: {product.name}")
            home_garden_cat.is_active = False
            print(f"✅ Deactivated Home & Garden category")
        
        # Reassign Sports products to Clothing
        if sports_cat:
            sports_products = sports_cat.products
            print(f"Reassigning {len(sports_products)} Sports products to Clothing...")
            for product in sports_products:
                product.categories.remove(sports_cat)
                if clothing_cat and clothing_cat not in product.categories:
                    product.categories.append(clothing_cat)
                print(f"✅ Reassigned: {product.name}")
            sports_cat.is_active = False
            print(f"✅ Deactivated Sports category")
        
        # Commit changes
        db.commit()
        
        print("\nFinal active categories:")
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
    cleanup_remaining_categories()