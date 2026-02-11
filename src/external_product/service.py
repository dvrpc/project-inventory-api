
from sqlalchemy.orm import Session
from .schema import ExternalProductCreateRequest, ExternalProductUpdateRequest
from .models import ExternalProduct

def get(db : Session, external_product_id: int):
    return db.query(ExternalProduct).filter(ExternalProduct.external_product_id == external_product_id).one_or_none()

def get_all(db: Session):
    return db.query(ExternalProduct).all()

def create(db: Session, external_product_in: ExternalProductCreateRequest):
    external_product = ExternalProduct(**external_product_in.model_dump())
    db.add(external_product)
    db.commit()
    db.refresh(external_product)
    return external_product

def update(db: Session, external_product: ExternalProduct, external_product_in: ExternalProductUpdateRequest):
    update_data = external_product_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(external_product, field, value)
    
    db.commit()
    db.refresh(external_product)
    return external_product

def delete(db: Session, external_product: ExternalProduct):
    db.delete(external_product)
    db.commit()
