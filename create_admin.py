"""
Script to create the first admin user for the e-commerce system.
Run this script to create an admin account that can manage products and orders.
"""
import sys
import os
from getpass import getpass

# Add the app directory to Python path
sys.path.append(os.path.dirname(__file__))

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import SessionLocal, engine
from app.models.models import Admin, Base

# Create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_admin_user():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("=== Create First Admin User ===")
        
        # Check if any admin already exists
        existing_admin = db.query(Admin).first()
        if existing_admin:
            print(f"Admin user already exists: {existing_admin.username}")
            return
        
        # Get admin details
        username = input("Enter admin username: ").strip()
        if not username:
            print("Username cannot be empty!")
            return
        
        email = input("Enter admin email: ").strip()
        if not email:
            print("Email cannot be empty!")
            return
        
        password = getpass("Enter admin password: ").strip()
        if not password:
            print("Password cannot be empty!")
            return
        
        confirm_password = getpass("Confirm password: ").strip()
        if password != confirm_password:
            print("Passwords don't match!")
            return
        
        # Create admin user
        hashed_password = hash_password(password)
        admin_user = Admin(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"\n✅ Admin user '{username}' created successfully!")
        print(f"Email: {email}")
        print(f"ID: {admin_user.id}")
        print("\nYou can now login at: http://127.0.0.1:8000/docs")
        print("Use the POST /api/v1/auth/login endpoint")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()