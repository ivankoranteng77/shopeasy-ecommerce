from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models.models import Admin
from app.schemas.schemas import AdminCreate, Admin as AdminSchema, Token
from app.utils.auth import verify_password, get_password_hash, create_access_token
from app.config import settings

router = APIRouter()


@router.post("/admin/register", response_model=AdminSchema)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    """Register a new admin (for initial setup only)."""
    # Check if admin already exists
    db_admin = db.query(Admin).filter(
        (Admin.email == admin.email) | (Admin.username == admin.username)
    ).first()
    
    if db_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    # Create new admin
    hashed_password = get_password_hash(admin.password)
    db_admin = Admin(
        email=admin.email,
        username=admin.username,
        hashed_password=hashed_password
    )
    
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    
    return db_admin


@router.post("/admin/login", response_model=Token)
def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Admin login."""
    admin = db.query(Admin).filter(Admin.username == form_data.username).first()
    
    if not admin or not verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive admin account"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}