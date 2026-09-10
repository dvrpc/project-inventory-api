from sqlalchemy.orm import Session

from src.database.gis import SessionLocal
from sqlalchemy import text
from pathlib import Path
from src.project.schema import ProjectFilters
import src.project.service as project_service
import json
from collections import Counter, defaultdict

current_dir = Path(__file__).parent.absolute()

STATE_COUNTY_CODE_MAP = {
    "42": ["42091", "42101", "42017", "42029", "42045"],
    "34": ["34007", "34015", "34021", "34005"],
}


def get_bbox_from_geoids(geoid_list: str) -> dict | None:
    geoids = [g.strip() for g in geoid_list.split(",")]

    if len(geoids[0]) == 2:
        geoids = STATE_COUNTY_CODE_MAP.get(geoids[0], geoids)

    with SessionLocal() as db:
        row = (
            db.execute(build_bbox_sql(geoids), {"geoids": geoids}).mappings().fetchone()
        )

    if row is None or row["min_lng"] is None:
        return None

    return dict(row)

def get_bbox_from_csa(pub_id: str) -> dict | None:
    with SessionLocal() as db:
        sql = text("""
            SELECT ST_XMin(bbox) AS min_lng,
                   ST_YMin(bbox) AS min_lat,
                   ST_XMax(bbox) AS max_lng,
                   ST_YMax(bbox) AS max_lat
            FROM (
                SELECT ST_Transform(ST_SetSRID(ST_Extent(shape), 26918), 4326) AS bbox
                FROM planning.project_inventory_tool_custom_study_areas_polygon
                WHERE pub_id = :pub_id
            ) AS envelope
        """)
        row = db.execute(sql, {"pub_id": pub_id}).mappings().fetchone()

    if row is None or row["min_lng"] is None:
        return None

    return dict(row)


def build_bbox_sql(geoids: list[str]):
    lengths = {len(g) for g in geoids}

    if lengths == {5}:
        source = (
            "SELECT shape FROM boundaries.countyboundaries WHERE fips = ANY(:geoids)"
        )
    elif lengths == {10}:
        source = (
            "SELECT shape FROM boundaries.dvrpc_mcd_phicpa WHERE geoid = ANY(:geoids)"
        )
    else:
        source = """
            SELECT shape FROM boundaries.countyboundaries WHERE fips = ANY(:geoids)
            UNION ALL
            SELECT shape FROM boundaries.dvrpc_mcd_phicpa WHERE geoid = ANY(:geoids)
        """

    return text(f"""
        WITH envelope AS (
            SELECT ST_Transform(ST_SetSRID(ST_Extent(shape), 26918), 4326) AS bbox
            FROM ({source}) combined
        )
        SELECT
            ST_XMin(bbox) AS min_lng,
            ST_YMin(bbox) AS min_lat,
            ST_XMax(bbox) AS max_lng,
            ST_YMax(bbox) AS max_lat
        FROM envelope
    """)


def get_bounding_box_locations(
    min_lon: float, min_lat: float, max_lon: float, max_lat: float
) -> list[tuple[str, str]]:
    sql = text("""
        WITH bbox AS (
            SELECT ST_Transform(
                ST_MakeEnvelope(:min_lon, :min_lat, :max_lon, :max_lat, 4326),
                26918
            ) AS shape
        ), center AS (
            SELECT ST_Transform(
                ST_SetSRID(
                    ST_MakePoint(
                        (:min_lon + :max_lon) / 2,
                        (:min_lat + :max_lat) / 2
                    ),
                    4326
                ),
                26918
            ) AS point
        ), locations AS (
            SELECT 'geoid' AS location_type, fips AS location_id, county.shape
            FROM boundaries.countyboundaries AS county
            CROSS JOIN bbox
            WHERE county.shape && bbox.shape
            UNION ALL
            SELECT 'geoid' AS location_type, geoid AS location_id, municipality.shape
            FROM boundaries.dvrpc_mcd_phicpa AS municipality
            CROSS JOIN bbox
            WHERE municipality.shape && bbox.shape
            UNION ALL
            SELECT 'csa' AS location_type, pub_id AS location_id, csa.shape
            FROM planning.project_inventory_tool_custom_study_areas_polygon AS csa
            CROSS JOIN bbox
            WHERE csa.shape && bbox.shape
        )
        SELECT combined.location_type, combined.location_id
        FROM locations AS combined
        CROSS JOIN center
        ORDER BY ST_Distance(
            CASE
                WHEN location_type = 'csa'
                THEN ST_ClosestPoint(combined.shape, center.point)
                ELSE ST_Centroid(combined.shape)
            END,
            center.point
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
        return [(row.location_type, row.location_id) for row in result]


def get_geoids_in_bounding_box(
    min_lon: float, min_lat: float, max_lon: float, max_lat: float
) -> list[str]:
    return [
        location_id
        for location_type, location_id in get_bounding_box_locations(
            min_lon, min_lat, max_lon, max_lat
        )
        if location_type == "geoid"
    ]


def get_custom_study_area_pub_ids_in_bounding_box(
    min_lon: float, min_lat: float, max_lon: float, max_lat: float
) -> list[str]:
    return [
        location_id
        for location_type, location_id in get_bounding_box_locations(
            min_lon, min_lat, max_lon, max_lat
        )
        if location_type == "csa"
    ]


def get_state_counts_geojson(db: Session, filters: ProjectFilters, is_dvrpc_user: bool):
    json_file_path = current_dir / "geojson" / "state_centroids.geojson"
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    geoids = project_service.get_geoids(db, filters, is_dvrpc_user)
    state_geoid_counts = Counter(geoids)

    for feature in data.get("features"):
        geoid = feature["properties"]["geoid"]
        count = state_geoid_counts.get(geoid)
        feature["properties"]["project_count"] = count

    return data


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


def get_csas_within_geoids(geoids: list[str]) -> list[str]:
    normalized_geoids = [geoid.strip() for geoid in geoids]

    with SessionLocal() as db:
        sql = text("""
            SELECT pub_id
            FROM planning.project_inventory_tool_custom_study_areas_polygon
            WHERE string_to_array(
                regexp_replace(concat_ws(',', cnty_fips, mcd_geo), '\\s+', '', 'g'),
                ','
            ) && CAST(:geoids AS text[])
        """)
        result = db.execute(sql, {"geoids": normalized_geoids})

    return [row.pub_id for row in result]

