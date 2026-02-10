from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import AgencyResponse, AgencyCreateRequest
from .models import Agency
from database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[AgencyResponse])
def get_agencies(db: Session = Depends(get_db)):
    return db.query(Agency).all()

@router.get("/{agency_id}", response_model=AgencyResponse)
def get_agency(agency_id: int, db: Session = Depends(get_db)):
    agency = db.query(Agency).filter(Agency.agency_id == agency_id).one_or_none()
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    return agency

@router.post("/", response_model=AgencyResponse)
def create_agency(agency: AgencyCreateRequest, db: Session = Depends(get_db)):
    db_agency = Agency(
        name=agency.name,
        address=agency.address,
        email=agency.email,
        phone=agency.phone
    )
    db.add(db_agency)
    db.commit()
    db.refresh(db_agency)
    return db_agency

@router.put("/{agency_id}", response_model=AgencyResponse)
def update_agency(agency_id: int, agency: AgencyResponse, db: Session = Depends(get_db)):
    db_agency = db.query(Agency).filter(Agency.agency_id == agency_id).one_or_none()
    if not db_agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    
    update_data = agency.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_agency, field, value)
    
    db.commit()
    db.refresh(db_agency)
    return db_agency

@router.delete("/{agency_id}")
def delete_agency(agency_id: int, db: Session = Depends(get_db)):
    db_agency = db.query(Agency).filter(Agency.agency_id == agency_id).one_or_none()
    if not db_agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    
    db.delete(db_agency)
    db.commit()
    return {"detail": "Agency deleted successfully"}

