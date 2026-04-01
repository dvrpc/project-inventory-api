from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.auth.validate import get_optional_dvrpc_user
from src.database.core import get_db
from src.gis.service import (
    get_county_counts_geojson,
    get_mcd_phicpa_counts_geojson,
    get_bbox_from_geoids,
)
from src.project.schema import ProjectFilters

router = APIRouter()


@router.get("/county_projects")
def get_county_projects(
    filters: ProjectFilters = Depends(ProjectFilters.as_query),
    db: Session = Depends(get_db),
    is_dvrpc_user: bool = Depends(get_optional_dvrpc_user),
):
    return get_county_counts_geojson(db, filters, is_dvrpc_user)


@router.get("/mcd_phicpa_projects")
def get_mcd_phicpa_projects(
    filters: ProjectFilters = Depends(ProjectFilters.as_query),
    db: Session = Depends(get_db),
    is_dvrpc_user: bool = Depends(get_optional_dvrpc_user),
):
    return get_mcd_phicpa_counts_geojson(db, filters, is_dvrpc_user)


@router.get("/bbox/{geoid}")
def get_bbox(geoid: str):
    return get_bbox_from_geoids(geoid)
