"""
Add the new categories: Clothing, Perfume, Cosmetics
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

def add_categories():
    db = SessionLocal()
    try:
        # Define the new categories
        new_categories = [
            {'name': 'Clothing', 'description': 'Fashion and clothing items'},
            {'name': 'Perfume', 'description': 'Fragrances and perfumes'},
            {'name': 'Cosmetics', 'description': 'Beauty and cosmetic products'}
        ]
        
        print("Adding new categories...")
        
        for cat_data in new_categories:
            # Check if category already exists
            existing = db.query(Category).filter(Category.name == cat_data['name']).first()
            if not existing:
                category = Category(name=cat_data['name'], description=cat_data['description'])
                db.add(category)
                print(f"✅ Added category: {cat_data['name']}")
            else:
                print(f"⚠️ Category already exists: {cat_data['name']}")
        
        # Commit changes
        db.commit()
        
        # Show all categories
        print("\nCurrent categories in database:")
        categories = db.query(Category).all()
        for cat in categories:
            print(f"- {cat.name} (ID: {cat.id}) - {cat.description}")
            
        print(f"\nTotal categories: {len(categories)}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_categories()