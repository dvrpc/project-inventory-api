
from sqlalchemy.orm import Session
from .schema import ProjectCreateRequest, ProjectUpdateRequest
from .models import Project

def get(db : Session, project_id: int):
    return db.query(Project).filter(Project.project_id == project_id).one_or_none()

def get_all(db: Session):
    return db.query(Project).all()

def create(db: Session, project_in: ProjectCreateRequest):
    project = Project(**project_in.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def update(db: Session, project: Project, project_in: ProjectUpdateRequest):
    update_data = project_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project

def delete(db: Session, project: Project):
    db.delete(project)
    db.commit()
