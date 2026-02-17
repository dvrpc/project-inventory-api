from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import GeographyResponse, GeographyCreateRequest, GeographyUpdateRequest
from .service import get, get_all, create, update, delete
from src.database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[GeographyResponse])
def get_geographies(db: Session = Depends(get_db)):
    return get_all(db)

@router.get("/{geography_id}", response_model=GeographyResponse)
def get_geography(geography_id: int, db: Session = Depends(get_db)):
    geography = get(db, geography_id)
    if not geography:
        raise HTTPException(status_code=404, detail="Geography not found")
    return geography

@router.post("/", response_model=GeographyResponse, status_code=201)
def create_geography(geography_in: GeographyCreateRequest, db: Session = Depends(get_db)):
    return create(db, geography_in)

@router.put("/{geography_id}", response_model=GeographyResponse)
def update_geography(geography_id: int, geography_in: GeographyUpdateRequest, db: Session = Depends(get_db)):
    geography = get(db, geography_id)
    if not geography:
        raise HTTPException(status_code=404, detail="Geography not found")
    
    return update(db, geography, geography_in)

@router.delete("/{geography_id}")
def delete_geography(geography_id: int, db: Session = Depends(get_db)):
    geography = get(db, geography_id)

    if not geography:
        raise HTTPException(status_code=404, detail="Geography not found")
    
    delete(db, geography)
    return {"detail": "Geography deleted successfully"}

