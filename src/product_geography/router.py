from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.product_geography.schema import (
    ProductGeographyResponse,
    ProductGeographyCreateRequest,
)
from src.product_geography.service import (
    get,
    get_all,
    get_all_by_product,
    create,
    delete,
)
from src.database.core import get_db
from src.auth.validate import require_admin

router = APIRouter()


@router.get("", response_model=List[ProductGeographyResponse])
def get_product_geographies(db: Session = Depends(get_db)):
    return get_all(db)


# TODO: rename paths /product/{pub_id} -> /product/{pub_id} once frontend is updated.
@router.get("/product/{pub_id}", response_model=List[ProductGeographyResponse])
def get_geographies_by_product(pub_id: str, db: Session = Depends(get_db)):
    return get_all_by_product(db, pub_id)


@router.post("", response_model=ProductGeographyResponse)
def create_product_geography(
    product_geography_in: ProductGeographyCreateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return create(db, product_geography_in)


@router.delete("/{pub_id}/{geography_id}")
def delete_product_geography(
    pub_id: str,
    geography_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    product_geography = get(db, pub_id, geography_id)
    if not product_geography:
        raise HTTPException(status_code=404, detail="Product Geography not found")

    delete(db, product_geography)
    return {"detail": "Product Geography deleted successfully"}
