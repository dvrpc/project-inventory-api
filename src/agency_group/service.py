from sqlalchemy.orm import Session

from src.agency_group.models import AgencyGroup


def get_all(db: Session):
    return db.query(AgencyGroup).order_by(AgencyGroup.name).all()
