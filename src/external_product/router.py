from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import ExternalProductResponse, ExternalProductCreateRequest, ExternalProductUpdateRequest
from .models import ExternalProduct
from database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[ExternalProductResponse])
def get_external_products(db: Session = Depends(get_db)):
    return db.query(ExternalProduct).all()

@router.get("/{product_id}", response_model=ExternalProductResponse)
def get_external_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ExternalProduct).filter(ExternalProduct.product_id == product_id).one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="External Product not found")
    return product

@router.post("/", response_model=ExternalProductResponse)
def create_external_product(product: ExternalProductCreateRequest, db: Session = Depends(get_db)):
    db_product = ExternalProduct(
        title=product.title,
        link=product.link,
        abstract=product.abstract
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=ExternalProductResponse)
def update_external_product(product_id: int, product: ExternalProductUpdateRequest, db: Session = Depends(get_db)):
    db_product = db.query(ExternalProduct).filter(ExternalProduct.product_id == product_id).one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="External Product not found")
    
    if product.title is not None:
        db_product.title = product.title
    if product.link is not None:
        db_product.link = product.link
    if product.abstract is not None:
        db_product.abstract = product.abstract
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_external_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(ExternalProduct).filter(ExternalProduct.product_id == product_id).one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="External Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"detail": "External Product deleted successfully"}
