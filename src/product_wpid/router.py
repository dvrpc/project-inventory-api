from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .service import get_all_wpids
from src.database.core import get_db

router = APIRouter()


@router.get("/", response_model=List[str])
def get_all(
    db: Session = Depends(get_db),
):
    # Return a list of distinct WORKPROGRAMIDs from the PRODUCTS_WPID table
    return get_all_wpids(db)
