from sqlalchemy.orm import Session, joinedload
from .models import Product


def get(db: Session, pub_id: int):
    return (
        db.query(Product)
        .options(joinedload(Product.wpids))
        .filter(Product.pub_id == pub_id)
        .one_or_none()
    )


def get_all(db: Session):
    return db.query(Product).options(joinedload(Product.wpids)).all()
