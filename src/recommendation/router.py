from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import RecommendationResponse, RecommendationCreateRequest, RecommendationUpdateRequest
from .service import get, get_all, create, update, delete
from src.database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[RecommendationResponse])
def get_recommendations(db: Session = Depends(get_db)):
    return get_all(db)

@router.get("/{recommendation_id}", response_model=RecommendationResponse)
def get_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    recommendation = get(db, recommendation_id)
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return recommendation

@router.post("/", response_model=RecommendationResponse, status_code=201)
def create_recommendation(recommendation_in: RecommendationCreateRequest, db: Session = Depends(get_db)):
    return create(db, recommendation_in)

@router.put("/{recommendation_id}", response_model=RecommendationResponse)
def update_recommendation(recommendation_id: int, recommendation_in: RecommendationUpdateRequest, db: Session = Depends(get_db)):
    recommendation = get(db, recommendation_id)
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    return update(db, recommendation, recommendation_in)

@router.delete("/{recommendation_id}")
def delete_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    recommendation = get(db, recommendation_id)

    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    delete(db, recommendation)
    return {"detail": "Recommendation deleted successfully"}

