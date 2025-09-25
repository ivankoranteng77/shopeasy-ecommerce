#!/usr/bin/env python3
"""
Startup script for the e-commerce API
"""
import sys
import subprocess
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def main():
    """Main startup function."""
    print("🚀 Starting E-Commerce API Setup")
    print("=" * 40)
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        if not run_command("python -m venv venv", "Virtual environment creation"):
            sys.exit(1)
    
    # Activate virtual environment and install dependencies
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        print("⚠️  Dependency installation failed. Please install manually:")
        print(f"   {activate_cmd}")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("📄 Creating .env file from template...")
        if Path(".env.example").exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ .env file created. Please update with your database credentials.")
        else:
            print("❌ .env.example not found")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your database credentials")
    print("2. Set up PostgreSQL database")
    print("3. Run database migrations: alembic upgrade head")
    print("4. Start the server: uvicorn app.main:app --reload")
    print("\n📖 API Documentation will be available at:")
    print("   - Swagger UI: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc")

if __name__ == "__main__":
    main()