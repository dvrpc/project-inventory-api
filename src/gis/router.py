from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.core import get_db
from src.gis.service import get_county_counts_geojson, get_mcd_phicpa_counts_geojson
from src.project.schema import ProjectFilters

router = APIRouter()

@router.get("/county_projects")
def get_county_projects(filters: ProjectFilters = Depends(ProjectFilters.as_query), db: Session = Depends(get_db)):
    return get_county_counts_geojson(db, filters)

@router.get("/mcd_phicpa_projects")
def get_county_projects(filters: ProjectFilters = Depends(ProjectFilters.as_query), db: Session = Depends(get_db)):
    return get_mcd_phicpa_counts_geojson(db, filters)