from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.product.schema import ProductResponse
from src.product.service import get, get_all
from src.database.core import get_db

router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return get_all(db)


@router.get("/{pub_id}", response_model=ProductResponse)
def get_product(pub_id: str, db: Session = Depends(get_db)):
    product = get(db, pub_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
