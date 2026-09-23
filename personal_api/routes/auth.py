"""Admin authentication: exchange credentials for a JWT token."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models.admin import Admin
from schemas.auth import TokenResponse
from security import create_access_token, verify_password

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse, summary="Admin login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Validate credentials and return a bearer token for private endpoints.

    Use the Swagger UI "Authorize" button (/docs) or POST form data:
    username=...&password=...
    """
    admin = db.query(Admin).filter(Admin.username == form.username).first()
    if admin is None or not verify_password(form.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return TokenResponse(access_token=create_access_token(admin.username))
