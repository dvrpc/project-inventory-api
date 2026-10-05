from sqlalchemy.orm import Session
from src.project_keyword.schema import ProjectKeywordCreateRequest
from src.project_keyword.models import ProjectKeyword


def get(db: Session, pub_id, keyword_id):
    return (
        db.query(ProjectKeyword)
        .filter(
            ProjectKeyword.pub_id == pub_id,
            ProjectKeyword.keyword_id == keyword_id,
        )
        .one_or_none()
    )


def get_all(db: Session):
    return db.query(ProjectKeyword).all()


def get_all_by_project(db: Session, pub_id: str):
    return (
        db.query(ProjectKeyword).filter(ProjectKeyword.pub_id == pub_id).all()
    )


def create(db: Session, project_keyword_in: ProjectKeywordCreateRequest):
    project_keyword = ProjectKeyword(**project_keyword_in.model_dump())
    db.add(project_keyword)
    db.commit()
    db.refresh(project_keyword)
    return project_keyword


def delete(db: Session, project_keyword: ProjectKeyword):
    db.delete(project_keyword)
    db.commit()
