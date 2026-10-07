from sqlalchemy.orm import Session
from src.keyword.models import Keyword
from src.project_keyword.models import ProjectKeyword




def get_all(db: Session):
    return db.query(Keyword).join(ProjectKeyword).distinct().all()

