"""Contact endpoints.

POST /api/contact is public (the portfolio contact form).
Submitted messages are PRIVATE — reading them requires admin auth.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from deps import require_admin
from models.contact import ContactMessage
from schemas.contact import ContactCreate, ContactOut

router = APIRouter(prefix="/api/contact", tags=["Contact"])


@router.post(
    "",
    response_model=ContactOut,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a contact message (public)",
)
def submit_contact(data: ContactCreate, db: Session = Depends(get_db)):
    """Validate and store a message from the portfolio contact form."""
    msg = ContactMessage(
        name=data.name.strip(),
        email=data.email,
        phone=data.phone,
        subject=data.subject,
        message=data.message.strip(),
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@router.get(
    "/messages",
    response_model=list[ContactOut],
    dependencies=[Depends(require_admin)],
    summary="Read contact submissions (admin only)",
)
def list_messages(db: Session = Depends(get_db)):
    """Private: newest submissions first. Never exposed publicly."""
    return (
        db.query(ContactMessage)
        .order_by(ContactMessage.created_at.desc())
        .all()
    )
