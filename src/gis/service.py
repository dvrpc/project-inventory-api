from sqlalchemy.orm import Session

from src.database.gis  import SessionLocal
from sqlalchemy import text
from pathlib import Path
from src.project.schema import ProjectFilters
import src.project.service as project_service
import json
from collections import Counter, defaultdict

current_dir = Path(__file__).parent.absolute()

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
    
def get_county_counts_geojson(db: Session, filters: ProjectFilters):
    json_file_path = current_dir / 'geojson' / 'county_centroids.geojson'
    with open(json_file_path, 'r', encoding='utf-8') as f: 
        data = json.load(f)

    geoids = project_service.get_geoids(db, filters)

    county_geoids_by_county = defaultdict(list)
    mcd_geoids_by_county = defaultdict(list)
    for g in geoids:
        if len(g) == 5:
            county_geoids_by_county[g].append(g)
        else:
            mcd_geoids_by_county[g[:5]].append(g)

    for feature in data.get('features'):
        geoid = feature['properties']['geoid']
        county_geoids = county_geoids_by_county.get(geoid, [])
        mcd_geoids = mcd_geoids_by_county.get(geoid, [])
        feature['properties']['county_project_count'] = len(county_geoids)
        feature['properties']['total_project_count'] = len(county_geoids) + len(mcd_geoids)
        feature['properties']['county_geoids'] = ','.join(county_geoids)
        feature['properties']['other_geoids'] = ','.join(mcd_geoids)
    
    return data

def get_mcd_phicpa_counts_geojson(db: Session, filters: ProjectFilters):
    json_file_path = current_dir / 'geojson' / 'mcd_phicpa_centroids.geojson'
    with open(json_file_path, 'r', encoding='utf-8') as f: 
        data = json.load(f)

    geoids = project_service.get_geoids(db, filters)
    mcd_geoid_set = set(g for g in geoids if len(g) > 5)

    for feature in data.get('features'):
        geoid = feature['properties']['geoid']
        count = 1 if geoid in mcd_geoid_set else 0
        feature['properties']['project_count'] = count
        feature['properties']['geoids'] = geoid if count else ''
    
    return data