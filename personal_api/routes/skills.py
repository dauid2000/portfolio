"""Skill endpoints: public reads, admin-only writes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from deps import require_admin
from models.skill import Skill
from schemas.skill import SkillCreate, SkillOut, SkillUpdate

router = APIRouter(prefix="/api/skills", tags=["Skills"])


def _normalize(name: str) -> str:
    return name.strip()


def _find_duplicate(db: Session, name: str, exclude_id: int | None = None):
    query = db.query(Skill).filter(func.lower(Skill.name) == name.lower())
    if exclude_id is not None:
        query = query.filter(Skill.id != exclude_id)
    return query.first()


@router.get("", response_model=list[SkillOut], summary="List skills (public)")
def list_skills(db: Session = Depends(get_db)):
    return db.query(Skill).order_by(Skill.id).all()


@router.get("/{skill_id}", response_model=SkillOut, summary="Get one skill (public)")
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    s = db.get(Skill, skill_id)
    if s is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Skill not found")
    return s


@router.post(
    "",
    response_model=SkillOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
    summary="Add a skill (admin)",
)
def create_skill(data: SkillCreate, db: Session = Depends(get_db)):
    data.name = _normalize(data.name)
    if _find_duplicate(db, data.name):
        raise HTTPException(status.HTTP_409_CONFLICT, "Skill already exists")
    s = Skill(name=data.name, category=data.category)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.put(
    "/{skill_id}",
    response_model=SkillOut,
    dependencies=[Depends(require_admin)],
    summary="Update a skill (admin)",
)
def update_skill(skill_id: int, data: SkillUpdate, db: Session = Depends(get_db)):
    s = db.get(Skill, skill_id)
    if s is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Skill not found")
    updates = data.model_dump(exclude_unset=True)
    if "name" in updates:
        updates["name"] = _normalize(updates["name"])
        if _find_duplicate(db, updates["name"], exclude_id=skill_id):
            raise HTTPException(status.HTTP_409_CONFLICT, "Skill already exists")
    for field, value in updates.items():
        setattr(s, field, value)
    db.commit()
    db.refresh(s)
    return s


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
    summary="Delete a skill (admin)",
)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    s = db.get(Skill, skill_id)
    if s is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Skill not found")
    db.delete(s)
    db.commit()
