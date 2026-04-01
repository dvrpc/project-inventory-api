from sqlalchemy.orm import Session

from src.database.gis import SessionLocal
from sqlalchemy import text
from pathlib import Path
from src.project.schema import ProjectFilters
import src.project.service as project_service
import json
from collections import Counter, defaultdict

current_dir = Path(__file__).parent.absolute()


# From a list of geoids (or single), finds bounding box of unioned geometries
def get_bbox_from_geoids(geoid_list: str) -> dict | None:
    geoids = [g.strip() for g in geoid_list.split(",")]

    sql = text("""
        SELECT 
            ST_XMin(ST_Transform(ST_SetSRID(ST_Extent(shape), 26918), 4326)) AS min_lng,
            ST_YMin(ST_Transform(ST_SetSRID(ST_Extent(shape), 26918), 4326)) AS min_lat,
            ST_XMax(ST_Transform(ST_SetSRID(ST_Extent(shape), 26918), 4326)) AS max_lng,
            ST_YMax(ST_Transform(ST_SetSRID(ST_Extent(shape), 26918), 4326)) AS max_lat
        FROM (
            SELECT shape FROM boundaries.countyboundaries WHERE fips = ANY(:geoids)
            UNION ALL
            SELECT shape FROM boundaries.dvrpc_mcd_phicpa WHERE geoid = ANY(:geoids)
        ) combined
    """)

    with SessionLocal() as db:
        result = db.execute(sql, {"geoids": geoids})
        row = result.fetchone()

    if row is None or row[0] is None:
        return None

    return {"min_lng": row[0], "min_lat": row[1], "max_lng": row[2], "max_lat": row[3]}


def get_geoids_in_bounding_box(
    min_lon: float, min_lat: float, max_lon: float, max_lat: float
) -> list[str]:
    sql = text("""
        SELECT geoid
        FROM (
            SELECT fips AS geoid, st_transform(shape, 4326) AS geom
            FROM boundaries.countyboundaries
            WHERE ST_MakeEnvelope(:min_lon, :min_lat, :max_lon, :max_lat, 4326) && st_transform(shape, 4326)
            UNION ALL
            SELECT geoid, st_transform(shape, 4326) AS geom
            FROM boundaries.dvrpc_mcd_phicpa
            WHERE ST_MakeEnvelope(:min_lon, :min_lat, :max_lon, :max_lat, 4326) && st_transform(shape, 4326)
        ) combined
        ORDER BY
            ST_Distance(
                ST_Centroid(geom),
                ST_SetSRID(ST_MakePoint((:min_lon + :max_lon) / 2, (:min_lat + :max_lat) / 2), 4326)
            )
    """)

    with SessionLocal() as db:
        result = db.execute(
            sql,
            {
                "min_lon": min_lon,
                "min_lat": min_lat,
                "max_lon": max_lon,
                "max_lat": max_lat,
            },
        )
        return [row.geoid for row in result]


def get_county_counts_geojson(
    db: Session, filters: ProjectFilters, is_dvrpc_user: bool
):
    json_file_path = current_dir / "geojson" / "county_centroids.geojson"
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    geoids = project_service.get_geoids(db, filters, is_dvrpc_user)

    county_geoids_by_county = defaultdict(list)
    mcd_geoids_by_county = defaultdict(list)
    for g in geoids:
        if len(g) == 5:
            county_geoids_by_county[g].append(g)
        else:
            mcd_geoids_by_county[g[:5]].append(g)

    for feature in data.get("features"):
        geoid = feature["properties"]["geoid"]
        county_geoids = county_geoids_by_county.get(geoid, [])
        mcd_geoids = mcd_geoids_by_county.get(geoid, [])
        feature["properties"]["county_project_count"] = len(county_geoids)
        feature["properties"]["total_project_count"] = len(county_geoids) + len(
            mcd_geoids
        )
        feature["properties"]["county_geoids"] = ",".join(county_geoids)
        feature["properties"]["other_geoids"] = ",".join(mcd_geoids)

    return data


def get_mcd_phicpa_counts_geojson(
    db: Session, filters: ProjectFilters, is_dvrpc_user: bool
):
    json_file_path = current_dir / "geojson" / "mcd_phicpa_centroids.geojson"
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    geoids = project_service.get_geoids(db, filters, is_dvrpc_user)
    mcd_geoid_counts = Counter(geoids)

    for feature in data.get("features"):
        geoid = feature["properties"]["geoid"]
        count = mcd_geoid_counts.get(geoid)
        feature["properties"]["project_count"] = count
        feature["properties"]["geoids"] = geoid if count else ""

    return data
