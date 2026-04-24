from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.attachment.schema import (
    AttachmentResponse,
    AttachmentCreateRequest,
    AttachmentUpdateRequest,
)
from src.attachment.service import get, get_all, create, update, delete
from src.database.core import get_db
from src.auth.validate import require_admin

router = APIRouter()


@router.get("", response_model=List[AttachmentResponse])
def get_attachments(db: Session = Depends(get_db)):
    return get_all(db)


@router.get("/{attachment_id}", response_model=AttachmentResponse)
def get_attachment(attachment_id: int, db: Session = Depends(get_db)):
    attachment = get(db, attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return attachment


@router.post("", response_model=AttachmentResponse, status_code=201)
def create_attachment(
    attachment_in: AttachmentCreateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return create(db, attachment_in)


@router.put("/{attachment_id}", response_model=AttachmentResponse)
def update_attachment(
    attachment_id: int,
    attachment_in: AttachmentUpdateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    attachment = get(db, attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    return update(db, attachment, attachment_in)


@router.delete("/{attachment_id}")
def delete_attachment(
    attachment_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)
):
    attachment = get(db, attachment_id)

    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    delete(db, attachment)
    return {"detail": "Attachment deleted successfully"}
