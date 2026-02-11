
from sqlalchemy.orm import Session
from .schema import AttachmentCreateRequest, AttachmentUpdateRequest
from .models import Attachment

def get(db : Session, attachment_id: int):
    return db.query(Attachment).filter(Attachment.attachment_id == attachment_id).one_or_none()

def get_all(db: Session):
    return db.query(Attachment).all()

def create(db: Session, attachment_in: AttachmentCreateRequest):
    attachment = Attachment(**attachment_in.model_dump())
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment

def update(db: Session, attachment: Attachment, attachment_in: AttachmentUpdateRequest):
    update_data = attachment_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(attachment, field, value)
    
    db.commit()
    db.refresh(attachment)
    return attachment

def delete(db: Session, attachment: Attachment):
    db.delete(attachment)
    db.commit()
