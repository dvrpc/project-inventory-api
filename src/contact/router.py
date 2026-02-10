from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import ContactResponse, ContactCreateRequest, ContactUpdateRequest
from .models import Contact
from database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[ContactResponse])
def get_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()

@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.contact_id == contact_id).one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.post("/", response_model=ContactResponse)
def create_contact(contact: ContactCreateRequest, db: Session = Depends(get_db)):
    db_contact = Contact(
        agency_id=contact.agency_id,
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone=contact.phone,
        job_title=contact.job_title,
        verified=contact.verified
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactUpdateRequest, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.contact_id == contact_id).one_or_none()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    update_data = contact.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_contact, field, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.contact_id == contact_id).one_or_none()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(db_contact)
    db.commit()
    return {"detail": "Contact deleted successfully"}
