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


@router.get("", response_model=List[ProjectKeywordResponse])
def get_project_keywords(db: Session = Depends(get_db)):
    return get_all(db)


@router.get("/project/{pub_id}", response_model=List[ProjectKeywordResponse])
def get_keywords_by_project(pub_id: str, db: Session = Depends(get_db)):
    return get_all_by_project(db, pub_id)


@router.post("", response_model=ProjectKeywordResponse)
def create_project_keyword(
    project_keyword_in: ProjectKeywordCreateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return create(db, project_keyword_in)


@router.delete("/{pub_id}/{keyword_id}")
def delete_project_keyword(
    pub_id: str,
    keyword_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    project_keyword = get(db, pub_id, keyword_id)
    if not project_keyword:
        raise HTTPException(status_code=404, detail="Project Keyword not found")

    delete(db, project_keyword)
    return {"detail": "Project Keyword deleted successfully"}
