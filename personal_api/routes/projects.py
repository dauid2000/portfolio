"""Project endpoints: public reads, admin-only writes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from deps import require_admin  # noqa: F401 (documented dependency for private routes)
from models.project import Project
from schemas.project import ProjectCreate, ProjectOut, ProjectUpdate

router = APIRouter(prefix="/api/projects", tags=["Projects"])


def project_to_out(p: Project) -> ProjectOut:
    """Convert the comma-separated DB value into a JSON list."""
    return ProjectOut(
        id=p.id,
        name=p.name,
        description=p.description,
        tagline=p.tagline,
        technologies=[t.strip() for t in p.technologies.split(",") if t.strip()],
        project_url=p.project_url,
        created_at=p.created_at,
    )


def _apply_update(p: Project, data: ProjectUpdate) -> None:
    for field, value in data.model_dump(exclude_unset=True).items():
        if field == "technologies":
            value = ", ".join(value) if value else ""
        setattr(p, field, value)


@router.get("", response_model=list[ProjectOut], summary="List projects (public)")
def list_projects(db: Session = Depends(get_db)):
    return [project_to_out(p) for p in db.query(Project).order_by(Project.id).all()]


@router.get("/{project_id}", response_model=ProjectOut, summary="Get one project (public)")
def get_project(project_id: int, db: Session = Depends(get_db)):
    p = db.get(Project, project_id)
    if p is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    return project_to_out(p)


@router.post(
    "",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
    summary="Create a project (admin)",
)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    p = Project(
        name=data.name.strip(),
        description=data.description,
        tagline=data.tagline,
        technologies=", ".join(data.technologies),
        project_url=data.project_url,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return project_to_out(p)


@router.put(
    "/{project_id}",
    response_model=ProjectOut,
    dependencies=[Depends(require_admin)],
    summary="Update a project (admin)",
)
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
    p = db.get(Project, project_id)
    if p is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    _apply_update(p, data)
    db.commit()
    db.refresh(p)
    return project_to_out(p)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
    summary="Delete a project (admin)",
)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    p = db.get(Project, project_id)
    if p is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    db.delete(p)
    db.commit()
