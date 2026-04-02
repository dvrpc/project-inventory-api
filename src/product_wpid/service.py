from sqlalchemy.orm import Session
from src.product_wpid.models import ProductWpid


def get_all_wpids(db: Session):
    result = (
        db.query(ProductWpid.WORKPROGRAMID)
        .distinct()
        .order_by(ProductWpid.WORKPROGRAMID.desc())
    )
    return [row[0] for row in result.all()]
