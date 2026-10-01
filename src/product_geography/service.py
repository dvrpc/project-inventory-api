from sqlalchemy.orm import Session
from src.product_geography.schema import ProductGeographyCreateRequest
from src.product_geography.models import ProductGeography


def get(db: Session, pub_id, geography_id):
    return (
        db.query(ProductGeography)
        .filter(
            ProductGeography.pub_id == pub_id,
            ProductGeography.geography_id == geography_id,
        )
        .one_or_none()
    )


def get_all(db: Session):
    return db.query(ProductGeography).all()


def get_all_by_product(db: Session, pub_id: str):
    return (
        db.query(ProductGeography)
        .filter(ProductGeography.pub_id == pub_id)
        .all()
    )


def create(db: Session, product_geography_in: ProductGeographyCreateRequest):
    product_geography = ProductGeography(**product_geography_in.model_dump())
    db.add(product_geography)
    db.commit()
    db.refresh(product_geography)
    return product_geography


def delete(db: Session, product_geography: ProductGeography):
    db.delete(product_geography)
    db.commit()
