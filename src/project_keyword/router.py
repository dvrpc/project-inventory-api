from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.project_keyword.schema import (
    ProjectKeywordResponse,
    ProjectKeywordCreateRequest,
)
from src.project_keyword.service import get, get_all, get_all_by_project, create, delete
from src.database.core import get_db
from src.auth.validate import require_admin

router = APIRouter()


@router.get("/", response_model=List[ProjectKeywordResponse])
def get_project_geographies(db: Session = Depends(get_db)):
    return get_all(db)


@router.get("/project/{project_id}", response_model=List[ProjectKeywordResponse])
def get_geographies_by_project(project_id: int, db: Session = Depends(get_db)):
    return get_all_by_project(db, project_id)


@router.post("/", response_model=ProjectKeywordResponse)
def create_project_keyword(
    project_keyword_in: ProjectKeywordCreateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return create(db, project_keyword_in)


@router.delete("/{project_id}/{keyword_id}")
def delete_project_keyword(
    project_id: int,
    keyword_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    project_keyword = get(db, project_id, keyword_id)
    if not project_keyword:
        raise HTTPException(status_code=404, detail="Project Keyword not found")

    delete(db, project_keyword)
    return {"detail": "Project Keyword deleted successfully"}
