from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.project_geography.schema import (
    ProjectGeographyResponse,
    ProjectGeographyCreateRequest,
)
from src.project_geography.service import (
    get,
    get_all,
    get_all_by_project,
    create,
    delete,
)
from src.database.core import get_db
from src.auth.validate import require_admin

router = APIRouter()


@router.get("", response_model=List[ProjectGeographyResponse])
def get_project_geographies(db: Session = Depends(get_db)):
    return get_all(db)


@router.get("/project/{pub_id}", response_model=List[ProjectGeographyResponse])
def get_geographies_by_project(pub_id: str, db: Session = Depends(get_db)):
    return get_all_by_project(db, pub_id)


@router.post("", response_model=ProjectGeographyResponse)
def create_project_geography(
    project_geography_in: ProjectGeographyCreateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return create(db, project_geography_in)


@router.delete("/{pub_id}/{geoid}")
def delete_project_geography(
    pub_id: str,
    geoid: str,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    project_geography = get(db, pub_id, geoid)
    if not project_geography:
        raise HTTPException(status_code=404, detail="Project Geography not found")

    delete(db, project_geography)
    return {"detail": "Project Geography deleted successfully"}
