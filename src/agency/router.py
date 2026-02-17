from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import AgencyResponse, AgencyCreateRequest, AgencyUpdateRequest
from .service import get, get_all, create, update, delete
from src.database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[AgencyResponse])
def get_agencies(db: Session = Depends(get_db)):
    return get_all(db)

@router.get("/{agency_id}", response_model=AgencyResponse)
def get_agency(agency_id: int, db: Session = Depends(get_db)):
    agency = get(db, agency_id)
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    return agency

@router.post("/", response_model=AgencyResponse, status_code=201)
def create_agency(agency_in: AgencyCreateRequest, db: Session = Depends(get_db)):
    return create(db, agency_in)

@router.put("/{agency_id}", response_model=AgencyResponse)
def update_agency(agency_id: int, agency_in: AgencyUpdateRequest, db: Session = Depends(get_db)):
    agency = get(db, agency_id)
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    
    return update(db, agency, agency_in)

@router.delete("/{agency_id}")
def delete_agency(agency_id: int, db: Session = Depends(get_db)):
    agency = get(db, agency_id)

    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    
    delete(db, agency)
    return {"detail": "Agency deleted successfully"}

