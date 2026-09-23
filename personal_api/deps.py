"""Shared FastAPI dependencies: admin authentication guard.

Usage on a protected endpoint:
    def endpoint(admin: Admin = Depends(require_admin)): ...
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models.admin import Admin
from security import decode_access_token

# tokenUrl points at the login route so the Swagger "Authorize" button works
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def require_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Admin:
    """Validate the Bearer token and return the matching admin user."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = decode_access_token(token)
    if username is None:
        raise credentials_error

    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin is None:
        raise credentials_error

    return admin
