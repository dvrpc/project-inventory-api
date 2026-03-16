
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from src.geography.models import Geography
from src.keyword.models import Keyword
from src.project_geography.models import ProjectGeography
from src.project_keyword.models import ProjectKeyword
from .schema import ProjectCreateRequest, ProjectFilters, ProjectUpdateRequest, ProjectResponse
from .models import Project
from src.gis.service import get_geoids_in_bounding_box

def map_project(project: Project) -> ProjectResponse:
    selected_product = (
        project.product if project.internal else project.external_product
    )

    return ProjectResponse(
        project_id=project.project_id,
        internal=project.internal,
        created_at=project.created_at,
        updated_at=project.updated_at,
        product=selected_product,
        needs=project.needs,
        recommendations=project.recommendations,
        geographies=[pg.geography for pg in project.project_geographies],
        keywords=[pk.keyword for pk in project.project_keywords]
    )

def get_unmapped(db : Session, project_id: int):
    return db.query(Project).filter(Project.project_id == project_id).one_or_none()

def get(db : Session, project_id: int):
    project = (
        db.query(Project)
            .options(
                joinedload(Project.product),
                joinedload(Project.external_product),
                joinedload(Project.project_geographies).joinedload(ProjectGeography.geography),
                joinedload(Project.project_keywords).joinedload(ProjectKeyword.keyword),
                )
                .filter(Project.project_id == project_id)
                .one_or_none()
    )

    return map_project(project)

def apply_bbox_filter(query, bbox: str):
    coords = bbox.split(",")
    geoids = get_geoids_in_bounding_box(
        float(coords[0]), float(coords[1]), float(coords[2]), float(coords[3])
    )
    return query.filter(Geography.geoid.in_(geoids))

def apply_geographies_filter(query, geographies: str, db: Session):
    geoids = [g.strip() for g in geographies.split(",")]
    expanded_geoids = expand_geoids(geoids, db)
    return query.filter(Geography.geoid.in_(expanded_geoids))

def apply_keywords_filter(query, keywords: str, db: Session):
    keyword_ids = [k.strip() for k in keywords.split(",")]
    return (
        query
        .join(Project.project_keywords)
        .join(ProjectKeyword.keyword)
        .filter(Keyword.keyword_id.in_(keyword_ids))
        .distinct()
    )

def expand_geoids(geoids: list[str], db: Session) -> list[str]:
    county_geoids = [g for g in geoids if len(g) == 5]
    municipality_geoids = [g for g in geoids if len(g) == 10]

    if county_geoids:
        child_geoids = (
            db.query(Geography.geoid)
            .filter(Geography.fips.in_(county_geoids))
            .all()
        )
        municipality_geoids.extend([g.geoid for g in child_geoids])

    return list(set(municipality_geoids + county_geoids))

def apply_filters(query, filters: ProjectFilters, db: Session):
    needs_geography_join = filters.bbox or filters.geographies
    if needs_geography_join:
        query = (
            query
            .join(Project.project_geographies)
            .join(ProjectGeography.geography)
            .distinct()
        )

    if filters.bbox:
        query = apply_bbox_filter(query, filters.bbox)
    if filters.geographies:
        query = apply_geographies_filter(query, filters.geographies, db)
    if filters.keywords:
        query = apply_keywords_filter(query, filters.keywords, db)

    return query


def get_all(db: Session, filters: Optional[ProjectFilters] = None) -> list[ProjectResponse]:
    query = db.query(Project)

    if filters:
        query = apply_filters(query, filters, db)

    return [map_project(p) for p in query.all()]


def get_geoids(db: Session, filters: Optional[ProjectFilters] = None) -> list[str]:
    query = (
        db.query(Geography.geoid)
        .join(Geography.project_geographies)
        .join(ProjectGeography.project)
    )
    print(filters)
    if filters:
        project_query = apply_filters(db.query(Project.project_id), filters, db)
        matching_ids = [row.project_id for row in project_query.all()]
        query = query.filter(Project.project_id.in_(matching_ids))

    return [row.geoid for row in query.all()]

def create(db: Session, project_in: ProjectCreateRequest):
    project = Project(**project_in.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return map_project(project)

def update(db: Session, project: Project, project_in: ProjectUpdateRequest):
    update_data = project_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return map_project(project)

def delete(db: Session, project: Project):
    db.delete(project)
    db.commit()
