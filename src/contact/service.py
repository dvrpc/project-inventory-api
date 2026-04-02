from sqlalchemy.orm import Session
from src.contact.schema import ContactCreateRequest, ContactUpdateRequest
from src.contact.models import Contact


def get(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.contact_id == contact_id).one_or_none()


def get_all(db: Session):
    return db.query(Contact).all()


def create(db: Session, contact_in: ContactCreateRequest):
    contact = Contact(**contact_in.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def update(db: Session, contact: Contact, contact_in: ContactUpdateRequest):
    update_data = contact_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(contact, field, value)

    db.commit()
    db.refresh(contact)
    return contact


def delete(db: Session, contact: Contact):
    db.delete(contact)
    db.commit()
