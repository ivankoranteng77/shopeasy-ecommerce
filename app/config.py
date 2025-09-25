from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite:///./ecommerce.db"  # Use SQLite for development
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # WhatsApp settings
    whatsapp_api_url: Optional[str] = None
    whatsapp_access_token: Optional[str] = None
    whatsapp_admin_number: str = "+1234567890"  # Admin's WhatsApp number
    
    # Application settings
    debug: bool = True
    environment: str = "development"
    cors_origins: str = "http://localhost:3000,http://localhost:8080"
    
    class Config:
        env_file = ".env"


settings = Settings()