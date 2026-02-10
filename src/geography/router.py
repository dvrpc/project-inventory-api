from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import GeographyResponse, GeographyCreateRequest, GeographyUpdateRequest
from .models import Geography
from database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[GeographyResponse])
def get_geographies(db: Session = Depends(get_db)):
    return db.query(Geography).all()

@router.get("/{geography_id}", response_model=GeographyResponse)
def get_geography(geography_id: int, db: Session = Depends(get_db)):
    geography = db.query(Geography).filter(Geography.geography_id == geography_id).one_or_none()
    if not geography:
        raise HTTPException(status_code=404, detail="Geography not found")
    return geography

@router.post("/", response_model=GeographyResponse)
def create_geography(geography: GeographyCreateRequest, db: Session = Depends(get_db)):
    db_geography = Geography(
        name=geography.name,
        geo_type=geography.geo_type,
        geoid=geography.geoid
    )
    db.add(db_geography)
    db.commit()
    db.refresh(db_geography)
    return db_geography

@router.put("/{geography_id}", response_model=GeographyResponse)
def update_geography(geography_id: int, geography: GeographyUpdateRequest, db: Session = Depends(get_db)):
    db_geography = db.query(Geography).filter(Geography.geography_id == geography_id).one_or_none()
    if not db_geography:
        raise HTTPException(status_code=404, detail="Geography not found")
    
    update_data = geography.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_geography, field, value)
    
    db.commit()
    db.refresh(db_geography)
    return db_geography

@router.delete("/{geography_id}")
def delete_geography(geography_id: int, db: Session = Depends(get_db)):
    db_geography = db.query(Geography).filter(Geography.geography_id == geography_id).one_or_none()
    if not db_geography:
        raise HTTPException(status_code=404, detail="Geography not found")
    
    db.delete(db_geography)
    db.commit()
    return {"detail": "Geography deleted successfully"}
