from sqlalchemy.orm import Session
from src.geography.models import Geography


def get(db: Session, geography_id: int):
    return (
        db.query(Geography).filter(Geography.geography_id == geography_id).one_or_none()
    )


def get_all(db: Session):
    return db.query(Geography).all()


