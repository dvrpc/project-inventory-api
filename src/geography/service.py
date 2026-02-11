
from sqlalchemy.orm import Session
from .schema import GeographyCreateRequest, GeographyUpdateRequest
from .models import Geography
import oracledb
from fastapi import HTTPException

def get(db : Session, geography_id: int):
    return db.query(Geography).filter(Geography.geography_id == geography_id).one_or_none()

def get_all(db: Session):
    return db.query(Geography).all()

def create(db: Session, geography_in: GeographyCreateRequest):
    geography = Geography(**geography_in.model_dump())
    db.add(geography)
    db.commit()
    db.refresh(geography)
    return geography

def update(db: Session, geography: Geography, geography_in: GeographyUpdateRequest):
    update_data = geography_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(geography, field, value)
    
    db.commit()
    db.refresh(geography)
    return geography


def delete(db: Session, geography: Geography):
    db.delete(geography)
    db.commit()
