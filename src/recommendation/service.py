from sqlalchemy.orm import Session
from src.recommendation.schema import (
    RecommendationCreateRequest,
    RecommendationUpdateRequest,
)
from src.recommendation.models import Recommendation


def get(db: Session, recommendation_id: int):
    return (
        db.query(Recommendation)
        .filter(Recommendation.recommendation_id == recommendation_id)
        .one_or_none()
    )


def get_all(db: Session):
    return db.query(Recommendation).all()


def create(db: Session, recommendation_in: RecommendationCreateRequest):
    recommendation = Recommendation(**recommendation_in.model_dump())
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    return recommendation


def update(
    db: Session,
    recommendation: Recommendation,
    recommendation_in: RecommendationUpdateRequest,
):
    update_data = recommendation_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(recommendation, field, value)

    db.commit()
    db.refresh(recommendation)
    return recommendation


def delete(db: Session, recommendation: Recommendation):
    db.delete(recommendation)
    db.commit()
