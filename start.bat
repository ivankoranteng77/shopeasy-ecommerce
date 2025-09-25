@echo off
echo 🚀 Starting ShopEasy E-commerce App...

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Create database
echo 🗄️ Setting up database...
python -c "import sys; sys.path.append('.'); from app.database import engine, Base; Base.metadata.create_all(bind=engine); print('✅ Database created successfully!')"

REM Add sample data
echo 📊 Adding sample data...
python -c "import sys; sys.path.append('.'); from app.database import get_db; from app.models import Category, Product; from sqlalchemy.orm import sessionmaker; from app.database import engine; SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine); db = SessionLocal(); categories = ['Electronics', 'Clothing', 'Home ^& Garden', 'Books', 'Sports']; [db.add(Category(name=cat_name, description=f'{cat_name} products')) for cat_name in categories if not db.query(Category).filter(Category.name == cat_name).first()]; db.commit(); db.close(); print('✅ Sample data added successfully!')"

echo.
echo 🎉 Setup complete! Starting server...
echo.
echo 🌐 Your app will be available at:
echo    - Backend API: http://localhost:8000
echo    - Frontend: Open index.html in your browser
echo.
echo 👨‍💼 Admin Login:
echo    Username: ivan
echo    Password: admin123
echo.

REM Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload