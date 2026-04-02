from sqlalchemy.orm import Session
from src.need.schema import NeedCreateRequest, NeedUpdateRequest
from src.need.models import Need


def get(db: Session, need_id: int):
    return db.query(Need).filter(Need.need_id == need_id).one_or_none()


def get_all(db: Session):
    return db.query(Need).all()


def create(db: Session, need_in: NeedCreateRequest):
    need = Need(**need_in.model_dump())
    db.add(need)
    db.commit()
    db.refresh(need)
    return need


def update(db: Session, need: Need, need_in: NeedUpdateRequest):
    update_data = need_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(need, field, value)

    db.commit()
    db.refresh(need)
    return need


def delete(db: Session, need: Need):
    db.delete(need)
    db.commit()
