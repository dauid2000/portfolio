"""Education endpoints: public reads, admin-only writes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from deps import require_admin
from models.education import Education
from schemas.education import EducationCreate, EducationOut, EducationUpdate

router = APIRouter(prefix="/api/education", tags=["Education"])


@router.get("", response_model=list[EducationOut], summary="List education records (public)")
def list_education(db: Session = Depends(get_db)):
    return db.query(Education).order_by(Education.id).all()


@router.post(
    "",
    response_model=EducationOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
    summary="Add an education record (admin)",
)
def create_education(data: EducationCreate, db: Session = Depends(get_db)):
    e = Education(**data.model_dump())
    db.add(e)
    db.commit()
    db.refresh(e)
    return e


@router.put(
    "/{education_id}",
    response_model=EducationOut,
    dependencies=[Depends(require_admin)],
    summary="Update an education record (admin)",
)
def update_education(education_id: int, data: EducationUpdate, db: Session = Depends(get_db)):
    e = db.get(Education, education_id)
    if e is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Education record not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(e, field, value)
    db.commit()
    db.refresh(e)
    return e


@router.delete(
    "/{education_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
    summary="Delete an education record (admin)",
)
def delete_education(education_id: int, db: Session = Depends(get_db)):
    e = db.get(Education, education_id)
    if e is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Education record not found")
    db.delete(e)
    db.commit()
