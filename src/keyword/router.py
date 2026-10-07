from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.keyword.schema import (
    KeywordResponse,
)
from src.keyword.service import get_all
from src.database.core import get_db

router = APIRouter()

@router.get("", response_model=List[KeywordResponse])
def get_keywords(db: Session = Depends(get_db)):
    return get_all(db)


