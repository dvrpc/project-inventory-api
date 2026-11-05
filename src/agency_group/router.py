from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.agency_group.schema import AgencyGroupResponse
from src.agency_group.service import get_all
from src.database.core import get_db

router = APIRouter()


@router.get("", response_model=List[AgencyGroupResponse])
def get_agency_groups(db: Session = Depends(get_db)):
    return get_all(db)
