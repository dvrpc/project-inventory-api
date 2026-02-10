from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import ProductResponse, ProductCreateRequest, ProductUpdateRequest
from .models import Product
from database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/{pub_id}", response_model=ProductResponse)
def get_product(pub_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.pub_id == pub_id).one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

