from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.geography.schema import (
    GeographyResponse,
)
from src.geography.service import get, get_all
from src.database.core import get_db

router = APIRouter()


@router.get("", response_model=List[GeographyResponse])
def get_geographies(db: Session = Depends(get_db)):
    return get_all(db)


@router.get("/{geography_id}", response_model=GeographyResponse)
def get_geography(geography_id: int, db: Session = Depends(get_db)):
    geography = get(db, geography_id)
    if not geography:
        raise HTTPException(status_code=404, detail="Geography not found")
    return geography

