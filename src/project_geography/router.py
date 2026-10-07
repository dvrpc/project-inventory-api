from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.project_geography.schema import (
    ProjectGeographyResponse,
)
from src.project_geography.service import (
    get_all,
    get_all_by_project,

)
from src.database.core import get_db

router = APIRouter()


@router.get("", response_model=List[ProjectGeographyResponse])
def get_project_geographies(db: Session = Depends(get_db)):
    return get_all(db)


@router.get("/project/{pub_id}", response_model=List[ProjectGeographyResponse])
def get_geographies_by_project(pub_id: str, db: Session = Depends(get_db)):
    return get_all_by_project(db, pub_id)


