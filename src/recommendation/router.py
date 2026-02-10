from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import RecommendationResponse, RecommendationCreateRequest, RecommendationUpdateRequest
from .models import Recommendation
from database.core import get_db

router = APIRouter()

@router.get("/", response_model=List[RecommendationResponse])
def get_recommendations(db: Session = Depends(get_db)):
    return db.query(Recommendation).all()

@router.get("/{recommendation_id}", response_model=RecommendationResponse)
def get_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    recommendation = db.query(Recommendation).filter(Recommendation.recommendation_id == recommendation_id).one_or_none()
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return recommendation

@router.post("/", response_model=RecommendationResponse)
def create_recommendation(recommendation: RecommendationCreateRequest, db: Session = Depends(get_db)):
    db_recommendation = Recommendation(
        project_id=recommendation.project_id,
        description=recommendation.description
    )
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation

@router.put("/{recommendation_id}", response_model=RecommendationResponse)
def update_recommendation(recommendation_id: int, recommendation: RecommendationUpdateRequest, db: Session = Depends(get_db)):
    db_recommendation = db.query(Recommendation).filter(Recommendation.recommendation_id == recommendation_id).one_or_none()
    if not db_recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    update_data = recommendation.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_recommendation, field, value)
    
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation

@router.delete("/{recommendation_id}")
def delete_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    db_recommendation = db.query(Recommendation).filter(Recommendation.recommendation_id == recommendation_id).one_or_none()
    if not db_recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    db.delete(db_recommendation)
    db.commit()
    return {"detail": "Recommendation deleted successfully"}
