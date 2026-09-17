from sqlalchemy.orm import Session

from src.database.gis import SessionLocal
from sqlalchemy import text


def get_csa_polygon(pub_id: str):
    sql = text("""
        select pub_id, title, state, cnty_fips, mcd_geo from planning.project_inventory_tool_custom_study_areas_polygon pitcsap where pub_id = :pub_id
        """)
    with SessionLocal() as db:
        result = db.execute(sql, {"pub_id": pub_id})
        print(result)
        row = result.mappings().fetchone()
        return dict(row) if row is not None else None

def get_csas_by_county():
    sql = text("""
        SELECT
            TRIM(fips) AS cnty_fips,
            STRING_AGG(pub_id, ', ' ORDER BY pub_id) AS pub_ids
        FROM
            planning.project_inventory_tool_custom_study_areas pitcsa,
            UNNEST(STRING_TO_ARRAY(cnty_fips, ',')) AS fips
        GROUP BY
            TRIM(fips)
        ORDER BY
            cnty_fips;
        """)
    with SessionLocal() as db:
        result = db.execute(sql)

        return [{"fips": row.cnty_fips, "pub_ids": row.pub_ids} for row in result]

            