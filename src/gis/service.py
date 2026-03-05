from sqlalchemy.orm import Session

from src.database.gis  import SessionLocal
from sqlalchemy import text
from pathlib import Path
import src.project.service as project_service
import json
from collections import Counter

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
    
def get_county_counts_geojson(db: Session):
    json_file_path = current_dir / 'geojson' / 'county_centroids.geojson'
    with open(json_file_path, 'r', encoding='utf-8') as f: 
        data = json.load(f)

    geoids = project_service.get_geoids(db)

    county_geoids = [g for g in geoids if len(g) == 5]
    all_geoids_as_county = [g[:5] for g in geoids]
    
    county_counts = Counter(county_geoids)
    total_counts = Counter(all_geoids_as_county)

    for feature in data.get('features'):
        geoid = feature['properties']['geoid']
        feature['properties']['county_project_count'] = county_counts.get(geoid, 0)
        feature['properties']['total_project_count'] = total_counts.get(geoid, 0)
    
    return data

def get_mcd_phicpa_counts_geojson(db: Session):
    json_file_path = current_dir / 'geojson' / 'mcd_phicpa_centroids.geojson'
    with open(json_file_path, 'r', encoding='utf-8') as f: 
        data = json.load(f)

    geoids = project_service.get_geoids(db)
    mcd_geoids = [g for g in geoids if len(g) > 5]
    mcd_counts = Counter(mcd_geoids)

    for feature in data.get('features'):
        geoid = feature['properties']['geoid']
        feature['properties']['project_count'] = mcd_counts.get(geoid, 0)
    
    return data