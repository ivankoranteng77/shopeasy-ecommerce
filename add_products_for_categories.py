"""
Add sample products for Perfume and Cosmetics categories
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

def add_sample_products():
    db = SessionLocal()
    try:
        # Get the category IDs
        clothing_cat = db.query(Category).filter(Category.name == 'Clothing').first()
        perfume_cat = db.query(Category).filter(Category.name == 'Perfume').first()
        cosmetics_cat = db.query(Category).filter(Category.name == 'Cosmetics').first()
        
        print(f"Clothing category ID: {clothing_cat.id if clothing_cat else 'Not found'}")
        print(f"Perfume category ID: {perfume_cat.id if perfume_cat else 'Not found'}")
        print(f"Cosmetics category ID: {cosmetics_cat.id if cosmetics_cat else 'Not found'}")
        
        # Sample products for each category
        sample_products = [
            # Clothing products
            {
                'name': 'Blue Crop Top',
                'description': 'Stylish blue crop top perfect for summer',
                'price': 25.99,
                'stock_quantity': 15,
                'sku': 'CLOTH001',
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300',
                'category': clothing_cat
            },
            {
                'name': 'Black Jeans',
                'description': 'Classic black denim jeans',
                'price': 59.99,
                'stock_quantity': 20,
                'sku': 'CLOTH002',
                'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=300',
                'category': clothing_cat
            },
            {
                'name': 'Summer Dress',
                'description': 'Light and comfortable summer dress',
                'price': 45.99,
                'stock_quantity': 10,
                'sku': 'CLOTH003',
                'image_url': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=300',
                'category': clothing_cat
            },
            
            # Perfume products
            {
                'name': 'Rose Garden Perfume',
                'description': 'Elegant floral fragrance with rose notes',
                'price': 89.99,
                'stock_quantity': 12,
                'sku': 'PERF001',
                'image_url': 'https://images.unsplash.com/photo-1541643600914-78c9066d13c5?w=300',
                'category': perfume_cat
            },
            {
                'name': 'Ocean Breeze Cologne',
                'description': 'Fresh and light aquatic fragrance',
                'price': 75.99,
                'stock_quantity': 8,
                'sku': 'PERF002',
                'image_url': 'https://images.unsplash.com/photo-1588405748880-12d1d2a59d75?w=300',
                'category': perfume_cat
            },
            {
                'name': 'Vanilla Nights Perfume',
                'description': 'Warm and sweet vanilla scented perfume',
                'price': 95.99,
                'stock_quantity': 6,
                'sku': 'PERF003',
                'image_url': 'https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=300',
                'category': perfume_cat
            },
            
            # Cosmetics products
            {
                'name': 'Matte Lipstick Set',
                'description': 'Set of 5 long-lasting matte lipsticks',
                'price': 35.99,
                'stock_quantity': 25,
                'sku': 'COSM001',
                'image_url': 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=300',
                'category': cosmetics_cat
            },
            {
                'name': 'Foundation Palette',
                'description': 'Professional makeup foundation palette',
                'price': 49.99,
                'stock_quantity': 18,
                'sku': 'COSM002',
                'image_url': 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=300',
                'category': cosmetics_cat
            },
            {
                'name': 'Eye Shadow Kit',
                'description': '12-color professional eyeshadow palette',
                'price': 29.99,
                'stock_quantity': 22,
                'sku': 'COSM003',
                'image_url': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=300',
                'category': cosmetics_cat
            },
            {
                'name': 'Blush & Bronzer Duo',
                'description': 'Perfect combination for a natural glow',
                'price': 24.99,
                'stock_quantity': 15,
                'sku': 'COSM004',
                'image_url': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=300',
                'category': cosmetics_cat
            }
        ]
        
        print("Adding sample products...")
        
        for product_data in sample_products:
            # Check if product already exists
            existing = db.query(Product).filter(Product.name == product_data['name']).first()
            if not existing:
                category = product_data.pop('category')  # Remove category from data
                product = Product(**product_data)
                if category:
                    product.categories.append(category)  # Add category relationship
                db.add(product)
                print(f"✅ Added product: {product.name}")
            else:
                print(f"⚠️ Product already exists: {product_data['name']}")
        
        # Commit changes
        db.commit()
        
        # Show total products per category
        print("\nProducts per category:")
        for cat in [clothing_cat, perfume_cat, cosmetics_cat]:
            if cat:
                count = db.query(Product).filter(Product.category_id == cat.id).count()
                print(f"- {cat.name}: {count} products")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_products()