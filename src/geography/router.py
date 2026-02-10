from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import GeographyResponse
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

