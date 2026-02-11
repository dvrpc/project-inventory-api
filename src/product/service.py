
from sqlalchemy.orm import Session
from .models import Product

def get(db : Session, pub_id: int):
    return db.query(Product).filter(Product.pub_id == pub_id).one_or_none()

def get_all(db: Session):
    return db.query(Product).all()