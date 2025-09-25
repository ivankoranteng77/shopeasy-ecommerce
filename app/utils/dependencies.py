from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Admin
from app.utils.auth import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/admin/login")


async def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current authenticated admin."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = verify_token(token)
    if username is None:
        raise credentials_exception
    
    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin is None:
        raise credentials_exception
    
    return admin


async def get_current_admin_user(current_admin: Admin = Depends(get_current_admin)):
    """Get current active admin user."""
    if not current_admin.is_active:
        raise HTTPException(status_code=400, detail="Inactive admin account")
    return current_admin