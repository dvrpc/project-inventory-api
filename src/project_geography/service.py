from sqlalchemy.orm import Session
from src.project_geography.models import ProjectGeography


def get(db: Session, pub_id, geoid):
    return (
        db.query(ProjectGeography)
        .filter(
            ProjectGeography.pub_id == pub_id,
            ProjectGeography.geoid == geoid,
        )
        .one_or_none()
    )


def get_all(db: Session):
    return db.query(ProjectGeography).all()


def get_all_by_project(db: Session, pub_id: str):
    return (
        db.query(ProjectGeography)
        .filter(ProjectGeography.pub_id == pub_id)
        .all()
    )

