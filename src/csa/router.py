from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.csa.service import get_csa_polygon
from src.database.core import get_db


router = APIRouter()

@router.get("/{pub_id}")
def find_csa_polygon(pub_id: str, db: Session = Depends(get_db)):
    return get_csa_polygon(db, pub_id)
