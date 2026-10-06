from sqlalchemy.orm import Session
from src.project_wpid.models import ProjectWpid


def get_all_wpids(db: Session):
    result = (
        db.query(ProjectWpid.WORKPROGRAMID)
        .distinct()
        .order_by(ProjectWpid.WORKPROGRAMID.desc())
    )
    return [row[0] for row in result.all()]
