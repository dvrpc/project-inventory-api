from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.product.schema import ProductDetailResponse, ProductFilters
from src.product.service import get, get_all
from src.database.core import get_db
from src.auth.validate import get_optional_dvrpc_user

router = APIRouter()


@router.get("", response_model=List[ProductDetailResponse])
def get_products(
    filters: ProductFilters = Depends(ProductFilters.as_query),
    db: Session = Depends(get_db),
    is_dvrpc_user: bool = Depends(get_optional_dvrpc_user),
):
    return get_all(db, filters, is_dvrpc_user)


@router.get("/{pub_id}", response_model=ProductDetailResponse)
def get_product(pub_id: str, db: Session = Depends(get_db)):
    product = get(db, pub_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
