from geography.models import Geography


def get(*, db_session, geography_id: int) -> Geography:
    """Get a Geography by its ID."""
    return db_session.query(Geography).filter(Geography.geography_id == geography_id).one_or_none()

def get_all(*, db_session) -> list[Geography]:
    """Get all Geography records."""
    return db_session.query(Geography).all()