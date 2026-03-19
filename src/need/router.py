from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import NeedResponse, NeedCreateRequest, NeedUpdateRequest
from .service import get, get_all, create, update, delete
from src.database.core import get_db
from src.auth.require_admin import require_admin

router = APIRouter()

@router.get("/", response_model=List[NeedResponse])
def get_needs(db: Session = Depends(get_db)):
    return get_all(db)

@router.get("/{need_id}", response_model=NeedResponse)
def get_need(need_id: int, db: Session = Depends(get_db)):
    need = get(db, need_id)
    if not need:
        raise HTTPException(status_code=404, detail="Need not found")
    return need

@router.post("/", response_model=NeedResponse, status_code=201)
def create_need(need_in: NeedCreateRequest, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return create(db, need_in)

@router.put("/{need_id}", response_model=NeedResponse)
def update_need(need_id: int, need_in: NeedUpdateRequest, db: Session = Depends(get_db), admin=Depends(require_admin)):
    need = get(db, need_id)
    if not need:
        raise HTTPException(status_code=404, detail="Need not found")
    
    return update(db, need, need_in)

@router.delete("/{need_id}")
def delete_need(need_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    need = get(db, need_id)

    if not need:
        raise HTTPException(status_code=404, detail="Need not found")
    
    delete(db, need)
    return {"detail": "Need deleted successfully"}

