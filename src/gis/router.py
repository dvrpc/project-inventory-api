from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.core import get_db
from src.gis.service import get_county_counts_geojson, get_mcd_phicpa_counts_geojson

router = APIRouter()

@router.get("/county_projects")
def get_county_projects(db: Session = Depends(get_db)):
    return get_county_counts_geojson(db)

@router.get("/mcd_phicpa_projects")
def get_county_projects(db: Session = Depends(get_db)):
    return get_mcd_phicpa_counts_geojson(db)