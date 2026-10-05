from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.project.schema import ProjectDetailResponse, ProjectFilters
from src.project.service import get, get_all
from src.database.core import get_db
from src.auth.validate import get_optional_dvrpc_user

router = APIRouter()


@router.get("", response_model=List[ProjectDetailResponse])
def get_projects(
    filters: ProjectFilters = Depends(ProjectFilters.as_query),
    db: Session = Depends(get_db),
    is_dvrpc_user: bool = Depends(get_optional_dvrpc_user),
):
    return get_all(db, filters, is_dvrpc_user)


@router.get("/{pub_id}", response_model=ProjectDetailResponse)
def get_project(pub_id: str, db: Session = Depends(get_db)):
    project = get(db, pub_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
