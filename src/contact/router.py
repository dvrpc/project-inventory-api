from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.contact.schema import (
    ContactResponse,
    ContactCreateRequest,
    ContactUpdateRequest,
)
from src.contact.service import get, get_all, create, update, delete
from src.database.core import get_db
from src.auth.validate import require_admin

router = APIRouter()


@router.get("/", response_model=List[ContactResponse])
def get_contacts(db: Session = Depends(get_db)):
    return get_all(db)


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = get(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(
    contact_in: ContactCreateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return create(db, contact_in)


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact_in: ContactUpdateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    contact = get(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return update(db, contact, contact_in)


@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)
):
    contact = get(db, contact_id)

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    delete(db, contact)
    return {"detail": "Contact deleted successfully"}
