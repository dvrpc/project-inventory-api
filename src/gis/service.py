from src.database.gis  import SessionLocal
from sqlalchemy import text

def get_geoids_in_bounding_box(min_lon: float, min_lat: float, max_lon: float, max_lat: float) -> list[str]:
    sql = text("""
        SELECT fips AS geoid 
        FROM boundaries.countyboundaries
        WHERE ST_MakeEnvelope(:min_lon, :min_lat, :max_lon, :max_lat, 4326) && st_transform(shape, 4326)
        UNION ALL
        SELECT geoid 
        FROM boundaries.dvrpc_mcd_phicpa
        WHERE ST_MakeEnvelope(:min_lon, :min_lat, :max_lon, :max_lat, 4326) && st_transform(shape, 4326)
    """)

    with SessionLocal() as db:
        result = db.execute(sql, {
            "min_lon": min_lon,
            "min_lat": min_lat,
            "max_lon": max_lon,
            "max_lat": max_lat,
        })
        return [row.geoid for row in result]