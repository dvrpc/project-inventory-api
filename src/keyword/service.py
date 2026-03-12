
from sqlalchemy.orm import Session
from .schema import KeywordCreateRequest, KeywordUpdateRequest
from .models import Keyword

def get(db : Session, keyword_id: int):
    return db.query(Keyword).filter(Keyword.keyword_id == keyword_id).one_or_none()

def get_all(db: Session):
    return db.query(Keyword).all()

def create(db: Session, keyword_in: KeywordCreateRequest):
    keyword = Keyword(**keyword_in.model_dump())
    db.add(keyword)
    db.commit()
    db.refresh(keyword)
    return keyword

def update(db: Session, keyword: Keyword, keyword_in: KeywordUpdateRequest):
    update_data = keyword_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(keyword, field, value)
    
    db.commit()
    db.refresh(keyword)
    return keyword

def delete(db: Session, keyword: Keyword):
    db.delete(keyword)
    db.commit()
