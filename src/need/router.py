from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import NeedResponse, NeedCreateRequest, NeedUpdateRequest
from .models import Need
from database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[NeedResponse])
def get_needs(db: Session = Depends(get_db)):
    return db.query(Need).all()

@router.get("/{need_id}", response_model=NeedResponse)
def get_need(need_id: int, db: Session = Depends(get_db)):
    need = db.query(Need).filter(Need.need_id == need_id).one_or_none()
    if not need:
        raise HTTPException(status_code=404, detail="Need not found")
    return need

@router.post("/", response_model=NeedResponse)
def create_need(need: NeedCreateRequest, db: Session = Depends(get_db)):
    db_need = Need(
        project_id=need.project_id,
        description=need.description
    )
    db.add(db_need)
    db.commit()
    db.refresh(db_need)
    return db_need

@router.put("/{need_id}", response_model=NeedResponse)
def update_need(need_id: int, need: NeedUpdateRequest, db: Session = Depends(get_db)):
    db_need = db.query(Need).filter(Need.need_id == need_id).one_or_none()
    if not db_need:
        raise HTTPException(status_code=404, detail="Need not found")
    
    update_data = need.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_need, field, value)
    
    db.commit()
    db.refresh(db_need)
    return db_need

@router.delete("/{need_id}")
def delete_need(need_id: int, db: Session = Depends(get_db)):
    db_need = db.query(Need).filter(Need.need_id == need_id).one_or_none()
    if not db_need:
        raise HTTPException(status_code=404, detail="Need not found")
    
    db.delete(db_need)
    db.commit()
    return {"detail": "Need deleted successfully"}
