from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")
    
    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS settings - updated for production
    allowed_origins: list = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "https://your-domain.vercel.app",  # Add your production domain
        "https://your-domain.netlify.app"  # Or Netlify domain
    ]
    
    # WhatsApp settings
    whatsapp_token: str = os.getenv("WHATSAPP_TOKEN", "")
    whatsapp_phone_id: str = os.getenv("WHATSAPP_PHONE_ID", "")
    admin_whatsapp: str = os.getenv("ADMIN_WHATSAPP", "+1234567890")
    
    # App settings
    app_name: str = "ShopEasy E-Commerce"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Production settings
    production: bool = os.getenv("PRODUCTION", "False").lower() == "true"
    
    class Config:
        env_file = ".env"

settings = Settings()