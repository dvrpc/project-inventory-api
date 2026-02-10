from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import AttachmentResponse, AttachmentCreateRequest, AttachmentUpdateRequest
from .models import Attachment
from database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[AttachmentResponse])
def get_attachments(db: Session = Depends(get_db)):
    return db.query(Attachment).all()

@router.get("/{attachment_id}", response_model=AttachmentResponse)
def get_attachment(attachment_id: int, db: Session = Depends(get_db)):
    attachment = db.query(Attachment).filter(Attachment.attachment_id == attachment_id).one_or_none()
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return attachment

@router.post("/", response_model=AttachmentResponse)
def create_attachment(attachment: AttachmentCreateRequest, db: Session = Depends(get_db)):
    db_attachment = Attachment(
        project_id=attachment.project_id,
        file_name=attachment.file_name,
        mime_type=attachment.mime_type,
        file_size=attachment.file_size,
        file_content=attachment.file_content
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

@router.put("/{attachment_id}", response_model=AttachmentResponse)
def update_attachment(attachment_id: int, attachment: AttachmentUpdateRequest, db: Session = Depends(get_db)):
    db_attachment = db.query(Attachment).filter(Attachment.attachment_id == attachment_id).one_or_none()
    if not db_attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    update_data = attachment.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_attachment, field, value)

    
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

@router.delete("/{attachment_id}")
def delete_attachment(attachment_id: int, db: Session = Depends(get_db)):
    db_attachment = db.query(Attachment).filter(Attachment.attachment_id == attachment_id).one_or_none()
    if not db_attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    db.delete(db_attachment)
    db.commit()
    return {"detail": "Attachment deleted successfully"}
