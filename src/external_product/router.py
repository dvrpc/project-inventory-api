from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import ExternalProductResponse, ExternalProductCreateRequest, ExternalProductUpdateRequest
from .service import get, get_all, create, update, delete
from database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[ExternalProductResponse])
def get_external_products(db: Session = Depends(get_db)):
    return get_all(db)

@router.get("/{external_product_id}", response_model=ExternalProductResponse)
def get_external_product(external_product_id: int, db: Session = Depends(get_db)):
    external_product = get(db, external_product_id)
    if not external_product:
        raise HTTPException(status_code=404, detail="ExternalProduct not found")
    return external_product

@router.post("/", response_model=ExternalProductResponse, status_code=201)
def create_external_product(external_product_in: ExternalProductCreateRequest, db: Session = Depends(get_db)):
    return create(db, external_product_in)

@router.put("/{external_product_id}", response_model=ExternalProductResponse)
def update_external_product(external_product_id: int, external_product_in: ExternalProductUpdateRequest, db: Session = Depends(get_db)):
    external_product = get(db, external_product_id)
    if not external_product:
        raise HTTPException(status_code=404, detail="ExternalProduct not found")
    
    return update(db, external_product, external_product_in)

@router.delete("/{external_product_id}")
def delete_external_product(external_product_id: int, db: Session = Depends(get_db)):
    external_product = get(db, external_product_id)

    if not external_product:
        raise HTTPException(status_code=404, detail="ExternalProduct not found")
    
    delete(db, external_product)
    return {"detail": "ExternalProduct deleted successfully"}

