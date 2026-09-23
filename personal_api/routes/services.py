"""Public services endpoint."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.service import Service
from schemas.service import ServiceOut

router = APIRouter(prefix="/api/services", tags=["Services"])


@router.get("", response_model=list[ServiceOut], summary="List services (public)")
def list_services(db: Session = Depends(get_db)):
    return db.query(Service).order_by(Service.id).all()
