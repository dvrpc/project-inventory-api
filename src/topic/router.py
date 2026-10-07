from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.topic.schema import (
    TopicResponse,

)
from src.topic.service import get_all
from src.database.core import get_db

router = APIRouter()


@router.get("", response_model=List[TopicResponse])
def get_topics(db: Session = Depends(get_db)):
    return get_all(db)



