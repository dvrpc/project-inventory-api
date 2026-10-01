from sqlalchemy.orm import Session
from src.product_keyword.schema import ProductKeywordCreateRequest
from src.product_keyword.models import ProductKeyword


def get(db: Session, pub_id, keyword_id):
    return (
        db.query(ProductKeyword)
        .filter(
            ProductKeyword.pub_id == pub_id,
            ProductKeyword.keyword_id == keyword_id,
        )
        .one_or_none()
    )


def get_all(db: Session):
    return db.query(ProductKeyword).all()


def get_all_by_product(db: Session, pub_id: str):
    return (
        db.query(ProductKeyword).filter(ProductKeyword.pub_id == pub_id).all()
    )


def create(db: Session, product_keyword_in: ProductKeywordCreateRequest):
    product_keyword = ProductKeyword(**product_keyword_in.model_dump())
    db.add(product_keyword)
    db.commit()
    db.refresh(product_keyword)
    return product_keyword


def delete(db: Session, product_keyword: ProductKeyword):
    db.delete(product_keyword)
    db.commit()
