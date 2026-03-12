
from sqlalchemy.orm import Session
from .schema import ProjectKeywordCreateRequest
from .models import ProjectKeyword


def get(db: Session, project_id, keyword_id):
    return db.query(ProjectKeyword).filter(
        ProjectKeyword.project_id == project_id,
        ProjectKeyword.keyword_id == keyword_id
    ).one_or_none()

def get_all(db: Session):
    return db.query(ProjectKeyword).all()

def get_all_by_project(db : Session, project_id: int):
    return db.query(ProjectKeyword).filter(ProjectKeyword.project_id == project_id).all()

def create(db: Session, project_keyword_in: ProjectKeywordCreateRequest):
    project_keyword = ProjectKeyword(**project_keyword_in.model_dump())
    db.add(project_keyword)
    db.commit()
    db.refresh(project_keyword)
    return project_keyword


def delete(db: Session, project_keyword: ProjectKeyword):
    db.delete(project_keyword)
    db.commit()
