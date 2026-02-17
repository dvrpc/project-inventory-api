from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import ProjectResponse, ProjectCreateRequest, ProjectUpdateRequest
from .service import get, get_all, create, update, delete
from src.database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return get_all(db)

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(project_in: ProjectCreateRequest, db: Session = Depends(get_db)):
    return create(db, project_in)

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_in: ProjectUpdateRequest, db: Session = Depends(get_db)):
    project = get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return update(db, project, project_in)

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = get(db, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    delete(db, project)
    return {"detail": "Project deleted successfully"}

