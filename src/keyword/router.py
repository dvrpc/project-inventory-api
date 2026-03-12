from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import KeywordResponse, KeywordCreateRequest, KeywordUpdateRequest
from .service import get, get_all, create, update, delete
from src.database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[KeywordResponse])
def get_keywords(db: Session = Depends(get_db)):
    return get_all(db)

@router.get("/{keyword_id}", response_model=KeywordResponse)
def get_keyword(keyword_id: int, db: Session = Depends(get_db)):
    keyword = get(db, keyword_id)
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return keyword

@router.post("/", response_model=KeywordResponse, status_code=201)
def create_keyword(keyword_in: KeywordCreateRequest, db: Session = Depends(get_db)):
    return create(db, keyword_in)

@router.put("/{keyword_id}", response_model=KeywordResponse)
def update_keyword(keyword_id: int, keyword_in: KeywordUpdateRequest, db: Session = Depends(get_db)):
    keyword = get(db, keyword_id)
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    
    return update(db, keyword, keyword_in)

@router.delete("/{keyword_id}")
def delete_keyword(keyword_id: int, db: Session = Depends(get_db)):
    keyword = get(db, keyword_id)

    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    
    delete(db, keyword)
    return {"detail": "Keyword deleted successfully"}

