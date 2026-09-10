from sqlalchemy.orm import Session

from src.database.gis import SessionLocal
from sqlalchemy import text


def get_csa_polygon(db: Session, pub_id: str):
    sql = text("""
        select pub_id, title, state, cnty_fips, mcd_geo from planning.project_inventory_tool_custom_study_areas_polygon pitcsap where pub_id = :pub_id
        """)
    with SessionLocal() as db:
        result = db.execute(sql, {"pub_id": pub_id})
        print(result)
        row = result.mappings().fetchone()
        return dict(row) if row is not None else None
    