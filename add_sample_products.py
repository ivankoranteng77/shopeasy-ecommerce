#!/usr/bin/env python3
"""
Script to add sample products and categories to the e-commerce system.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import Product, Category, Admin

def add_sample_data():
    """Add sample categories and products."""
    print("🛍️ Adding Sample Products and Categories")
    print("=" * 50)
    
    db: Session = SessionLocal()
    
    try:
        # Check if admin exists
        admin = db.query(Admin).first()
        if not admin:
            print("❌ No admin user found! Please create an admin first.")
            return False
        
        # Check if products already exist
        existing_products = db.query(Product).count()
        if existing_products > 0:
            print(f"ℹ️ Database already has {existing_products} products.")
            response = input("Do you want to add more sample products? (y/n): ").strip().lower()
            if response != 'y':
                return True
        
        # Create sample categories
        print("\n📁 Creating Categories...")
        categories_data = [
            {"name": "Electronics", "description": "Electronic devices and gadgets"},
            {"name": "Clothing", "description": "Shirts, pants, dresses and accessories"},
            {"name": "Books", "description": "Physical and digital books"},
            {"name": "Home & Garden", "description": "Home improvement and gardening supplies"},
            {"name": "Sports", "description": "Sports equipment and fitness gear"}
        ]
        
        categories = {}
        for cat_data in categories_data:
            # Check if category already exists
            existing_cat = db.query(Category).filter(Category.name == cat_data["name"]).first()
            if existing_cat:
                categories[cat_data["name"]] = existing_cat
                print(f"   ✅ Category '{cat_data['name']}' already exists")
            else:
                category = Category(**cat_data)
                db.add(category)
                db.commit()
                db.refresh(category)
                categories[cat_data["name"]] = category
                print(f"   ✅ Created category: {cat_data['name']}")
        
        # Create sample products
        print("\n📦 Creating Products...")
        products_data = [
            {
                "name": "iPhone 15 Pro",
                "description": "Latest Apple iPhone with advanced camera and A17 Pro chip",
                "price": 999.99,
                "sku": "IPHONE15PRO",
                "stock_quantity": 25,
                "image_url": "https://example.com/iphone15pro.jpg",
                "weight": 0.187,
                "dimensions": "146.6 x 70.6 x 8.25 mm",
                "categories": ["Electronics"]
            },
            {
                "name": "Samsung Galaxy S24",
                "description": "Powerful Android smartphone with excellent display",
                "price": 799.99,
                "sku": "GALAXY-S24",
                "stock_quantity": 30,
                "image_url": "https://example.com/galaxys24.jpg",
                "weight": 0.167,
                "dimensions": "147.0 x 70.6 x 7.6 mm",
                "categories": ["Electronics"]
            },
            {
                "name": "Nike Air Max 90",
                "description": "Classic running shoes with comfortable cushioning",
                "price": 120.00,
                "sku": "NIKE-AM90",
                "stock_quantity": 50,
                "image_url": "https://example.com/nikeairmax90.jpg",
                "weight": 0.8,
                "dimensions": "Size varies",
                "categories": ["Sports", "Clothing"]
            },
            {
                "name": "Python Programming Book",
                "description": "Complete guide to Python programming for beginners",
                "price": 39.99,
                "sku": "BOOK-PYTHON",
                "stock_quantity": 100,
                "image_url": "https://example.com/pythonbook.jpg",
                "weight": 0.5,
                "dimensions": "23.4 x 18.5 x 2.8 cm",
                "categories": ["Books"]
            },
            {
                "name": "Wireless Headphones",
                "description": "Noise-cancelling Bluetooth headphones with long battery life",
                "price": 199.99,
                "sku": "HEADPHONES-WL",
                "stock_quantity": 40,
                "image_url": "https://example.com/headphones.jpg",
                "weight": 0.25,
                "dimensions": "17.8 x 15.9 x 8.2 cm",
                "categories": ["Electronics"]
            },
            {
                "name": "Cotton T-Shirt",
                "description": "Comfortable 100% cotton t-shirt available in multiple colors",
                "price": 19.99,
                "sku": "TSHIRT-COTTON",
                "stock_quantity": 200,
                "image_url": "https://example.com/tshirt.jpg",
                "weight": 0.15,
                "dimensions": "Size varies",
                "categories": ["Clothing"]
            },
            {
                "name": "Garden Hose 50ft",
                "description": "Durable garden hose with spray nozzle included",
                "price": 49.99,
                "sku": "HOSE-50FT",
                "stock_quantity": 15,
                "image_url": "https://example.com/gardenhose.jpg",
                "weight": 3.5,
                "dimensions": "50ft length",
                "categories": ["Home & Garden"]
            },
            {
                "name": "Yoga Mat",
                "description": "Premium non-slip yoga mat for workout and meditation",
                "price": 29.99,
                "sku": "YOGA-MAT",
                "stock_quantity": 75,
                "image_url": "https://example.com/yogamat.jpg",
                "weight": 1.2,
                "dimensions": "183 x 61 x 0.6 cm",
                "categories": ["Sports"]
            }
        ]
        
        created_count = 0
        for product_data in products_data:
            # Check if product already exists
            existing_product = db.query(Product).filter(Product.sku == product_data["sku"]).first()
            if existing_product:
                print(f"   ⚠️ Product '{product_data['name']}' already exists")
                continue
            
            # Extract categories and create product
            category_names = product_data.pop("categories")
            product = Product(**product_data)
            
            # Add categories
            for cat_name in category_names:
                if cat_name in categories:
                    product.categories.append(categories[cat_name])
            
            db.add(product)
            created_count += 1
            print(f"   ✅ Created product: {product_data['name']} (${product_data['price']})")
        
        db.commit()
        
        print(f"\n🎉 Successfully added {created_count} products!")
        print(f"📊 Total products in database: {db.query(Product).count()}")
        print(f"📁 Total categories in database: {db.query(Category).count()}")
        
        print(f"\n🌐 You can now:")
        print(f"   • View products at: http://127.0.0.1:8000/api/v1/products")
        print(f"   • Test the API at: http://127.0.0.1:8000/docs")
        print(f"   • Login as admin with username: {admin.username}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        db.rollback()
        return False
        
    finally:
        db.close()


if __name__ == "__main__":
    try:
        success = add_sample_data()
        if success:
            print("\n✨ Sample data setup complete!")
        else:
            print("\n💥 Failed to add sample data.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)