
from sqlalchemy.orm import Session
from .schema import AgencyCreateRequest, AgencyUpdateRequest
from .models import Agency

def get(db : Session, agency_id: int):
    return db.query(Agency).filter(Agency.agency_id == agency_id).one_or_none()

def get_all(db: Session):
    return db.query(Agency).all()

def create(db: Session, agency_in: AgencyCreateRequest):
    agency = Agency(**agency_in.model_dump())
    db.add(agency)
    db.commit()
    db.refresh(agency)
    return agency

def update(db: Session, agency: Agency, agency_in: AgencyUpdateRequest):
    update_data = agency_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(agency, field, value)
    
    db.commit()
    db.refresh(agency)
    return agency

def delete(db: Session, agency: Agency):
    db.delete(agency)
    db.commit()
