from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import ProjectGeographyResponse, ProjectGeographyCreateRequest
from .models import ProjectGeography
from database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[ProjectGeographyResponse])
def get_project_geographies(db: Session = Depends(get_db)):
    return db.query(ProjectGeography).all()

@router.get("/{project_id}/{geography_id}", response_model=ProjectGeographyResponse)
def get_project_geography(project_id: int, geography_id: int, db: Session = Depends(get_db)):
    project_geography = db.query(ProjectGeography).filter(
        ProjectGeography.project_id == project_id,
        ProjectGeography.geography_id == geography_id
    ).one_or_none()
    if not project_geography:
        raise HTTPException(status_code=404, detail="Project Geography not found")
    return project_geography

@router.get("/project/{project_id}", response_model=List[ProjectGeographyResponse])
def get_geographies_by_project(project_id: int, db: Session = Depends(get_db)):
    return db.query(ProjectGeography).filter(ProjectGeography.project_id == project_id).all()

@router.post("/", response_model=ProjectGeographyResponse)
def create_project_geography(project_geography: ProjectGeographyCreateRequest, db: Session = Depends(get_db)):
    db_project_geography = ProjectGeography(
        project_id=project_geography.project_id,
        geography_id=project_geography.geography_id
    )
    db.add(db_project_geography)
    db.commit()
    db.refresh(db_project_geography)
    return db_project_geography

@router.delete("/{project_id}/{geography_id}")
def delete_project_geography(project_id: int, geography_id: int, db: Session = Depends(get_db)):
    project_geography = db.query(ProjectGeography).filter(
        ProjectGeography.project_id == project_id,
        ProjectGeography.geography_id == geography_id
    ).one_or_none()
    if not project_geography:
        raise HTTPException(status_code=404, detail="Project Geography not found")
    
    db.delete(project_geography)
    db.commit()
    return {"detail": "Project Geography deleted successfully"}
