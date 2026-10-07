from sqlalchemy.orm import Session
from src.topic.models import Topic

def get_all(db: Session):
    return db.query(Topic).all()


