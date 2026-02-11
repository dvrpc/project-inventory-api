
from sqlalchemy.orm import Session
from .schema import ProjectGeographyCreateRequest
from .models import ProjectGeography


def get(db: Session, project_id, geography_id):
    return db.query(ProjectGeography).filter(
        ProjectGeography.project_id == project_id,
        ProjectGeography.geography_id == geography_id
    ).one_or_none()

def get_all(db: Session):
    return db.query(ProjectGeography).all()

def get_all_by_project(db : Session, project_id: int):
    return db.query(ProjectGeography).filter(ProjectGeography.project_id == project_id).all()

def create(db: Session, project_geography_in: ProjectGeographyCreateRequest):
    project_geography = ProjectGeography(**project_geography_in.model_dump())
    db.add(project_geography)
    db.commit()
    db.refresh(project_geography)
    return project_geography


def delete(db: Session, project_geography: ProjectGeography):
    db.delete(project_geography)
    db.commit()
