"""
Quick script to check or reset admin password
"""
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(__file__))

from app.database import SessionLocal
from app.models.models import Admin
from app.utils.auth import verify_password, get_password_hash

def check_admin_login():
    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.username == "ivan").first()
        if not admin:
            print("Admin 'ivan' not found!")
            return
        
        print(f"Admin user found: {admin.username}")
        print(f"Email: {admin.email}")
        print(f"Active: {admin.is_active}")
        
        # Try common passwords
        test_passwords = ["admin123", "admin", "ivan", "password", "123456"]
        
        for pwd in test_passwords:
            if verify_password(pwd, admin.hashed_password):
                print(f"✅ Found working password: '{pwd}'")
                return
        
        print("❌ None of the common passwords work.")
        print("Resetting password to 'admin123'...")
        
        # Reset password to admin123
        new_hashed = get_password_hash("admin123")
        admin.hashed_password = new_hashed
        db.commit()
        
        print("✅ Password reset to 'admin123'")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    check_admin_login()