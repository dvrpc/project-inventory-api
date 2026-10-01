from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.product_geography.schema import (
    ProjectGeographyResponse,
    ProjectGeographyCreateRequest,
)
from src.product_geography.service import (
    get,
    get_all,
    get_all_by_product,
    create,
    delete,
)
from src.database.core import get_db
from src.auth.validate import require_admin

router = APIRouter()


@router.get("", response_model=List[ProjectGeographyResponse])
def get_project_geographies(db: Session = Depends(get_db)):
    return get_all(db)


# TODO: rename paths /project/{project_id} -> /product/{pub_id} once frontend is updated.
@router.get("/project/{project_id}", response_model=List[ProjectGeographyResponse])
def get_geographies_by_project(project_id: str, db: Session = Depends(get_db)):
    return get_all_by_product(db, project_id)


@router.post("", response_model=ProjectGeographyResponse)
def create_project_geography(
    project_geography_in: ProjectGeographyCreateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return create(db, project_geography_in)


@router.delete("/{project_id}/{geography_id}")
def delete_project_geography(
    project_id: str,
    geography_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    project_geography = get(db, project_id, geography_id)
    if not project_geography:
        raise HTTPException(status_code=404, detail="Project Geography not found")

    delete(db, project_geography)
    return {"detail": "Project Geography deleted successfully"}
