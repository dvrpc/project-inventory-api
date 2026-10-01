from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.product_keyword.schema import (
    ProductKeywordResponse,
    ProductKeywordCreateRequest,
)
from src.product_keyword.service import get, get_all, get_all_by_product, create, delete
from src.database.core import get_db
from src.auth.validate import require_admin

router = APIRouter()


@router.get("", response_model=List[ProductKeywordResponse])
def get_product_geographies(db: Session = Depends(get_db)):
    return get_all(db)


# TODO: rename paths /product/{pub_id} -> /product/{pub_id} once frontend is updated.
@router.get("/product/{pub_id}", response_model=List[ProductKeywordResponse])
def get_geographies_by_product(pub_id: str, db: Session = Depends(get_db)):
    return get_all_by_product(db, pub_id)


@router.post("", response_model=ProductKeywordResponse)
def create_product_keyword(
    product_keyword_in: ProductKeywordCreateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return create(db, product_keyword_in)


@router.delete("/{pub_id}/{keyword_id}")
def delete_product_keyword(
    pub_id: str,
    keyword_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    product_keyword = get(db, pub_id, keyword_id)
    if not product_keyword:
        raise HTTPException(status_code=404, detail="Product Keyword not found")

    delete(db, product_keyword)
    return {"detail": "Product Keyword deleted successfully"}
