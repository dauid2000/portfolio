"""Public profile endpoint."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.profile import Profile
from schemas.profile import ProfileOut

router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.get("", response_model=ProfileOut, summary="Get personal information (public)")
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    if profile is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Profile not configured yet")
    return profile
