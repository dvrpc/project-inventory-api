from datetime import date
from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from src.geography.models import Geography
from src.keyword.models import Keyword
from src.product.models import Product
from src.project_geography.models import ProjectGeography
from src.project_keyword.models import ProjectKeyword
from .schema import (
    ProjectCreateRequest,
    ProjectFilters,
    ProjectUpdateRequest,
    ProjectResponse,
)
from .models import Project
from src.gis.service import get_geoids_in_bounding_box


def map_project(project: Project) -> ProjectResponse:
    selected_product = project.product if project.internal else project.external_product

    return ProjectResponse(
        project_id=project.project_id,
        internal=project.internal,
        created_at=project.created_at,
        updated_at=project.updated_at,
        product=selected_product,
        needs=project.needs,
        recommendations=project.recommendations,
        geographies=[pg.geography for pg in project.project_geographies],
        keywords=[pk.keyword for pk in project.project_keywords],
    )


def get_unmapped(db: Session, project_id: int):
    return db.query(Project).filter(Project.project_id == project_id).one_or_none()


def get(db: Session, project_id: int):
    project = (
        db.query(Project)
        .options(
            joinedload(Project.product),
            joinedload(Project.external_product),
            joinedload(Project.project_geographies).joinedload(
                ProjectGeography.geography
            ),
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
    return query.filter(Geography.geoid.in_(geoids)), geoids


def apply_geographies_filter(query, geographies: str, db: Session):
    geoids = [g.strip() for g in geographies.split(",")]
    expanded_geoids = expand_geoids(geoids, db)
    return query.filter(Geography.geoid.in_(expanded_geoids))


def apply_keywords_filter(query, keywords: str, db: Session):
    keyword_ids = [k.strip() for k in keywords.split(",")]
    return (
        query.join(Project.project_keywords)
        .join(ProjectKeyword.keyword)
        .filter(Keyword.keyword_id.in_(keyword_ids))
        .distinct()
    )


def expand_geoids(geoids: list[str], db: Session) -> list[str]:
    county_geoids = [g for g in geoids if len(g) == 5]
    municipality_geoids = [g for g in geoids if len(g) == 10]

    if county_geoids:
        child_geoids = (
            db.query(Geography.geoid).filter(Geography.fips.in_(county_geoids)).all()
        )
        municipality_geoids.extend([g.geoid for g in child_geoids])

    return list(set(municipality_geoids + county_geoids))


def apply_filters(query, filters: ProjectFilters, db: Session):
    if filters.project:
        query = query.filter(Project.project_id == filters.project)
        return query

    query = (
        query.join(Project.project_geographies)
        .join(ProjectGeography.geography)
        .join(Project.product)
        .distinct()
    )
    if filters.geographies:
        query = apply_geographies_filter(query, filters.geographies, db)
    if filters.keywords:
        query = apply_keywords_filter(query, filters.keywords, db)
    if filters.status:
        query = query.join(Project.product).filter(Product.status == filters.status)
    if filters.yearFrom:
        query = query.filter(Product.pub_date >= date(int(filters.yearFrom), 1, 1))
    if filters.yearTo:
        query = query.filter(Product.pub_date <= date(int(filters.yearTo), 12, 31))

    return query


def get_all(
    db: Session, filters: Optional[ProjectFilters] = None
) -> list[ProjectResponse]:
    ordered_geoids = None

    query = db.query(Project).options(
        joinedload(Project.product),
        joinedload(Project.external_product),
        joinedload(Project.project_geographies).joinedload(ProjectGeography.geography),
        joinedload(Project.project_keywords).joinedload(ProjectKeyword.keyword),
    )

    if filters:
        query = apply_filters(query, filters, db)

    if filters.bbox:
        query, ordered_geoids = apply_bbox_filter(query, filters.bbox)

    rows = query.all()
    projects = [map_project(p) for p in rows]

    match filters.sort if filters else None:
        case "oldest":
            projects.sort(key=lambda p: p.product.pub_date or date.min)
        case "az":
            projects.sort(key=lambda p: p.product.title or "")
        case "za":
            projects.sort(key=lambda p: p.product.title or "", reverse=True)
        case "newest":
            projects.sort(key=lambda p: p.product.pub_date or date.min, reverse=True)
        case _:
            # Default geographies sort. Groups county & municipality and chooses first based on zoom level
            # Each grouping is sorted by geography proximity to the center of the bounding box
            if filters.geographies:
                county_first = (
                    len([g.strip() for g in filters.geographies.split(",")][0]) == 5
                )
            else:
                zoom = int(filters.zoom) if filters.zoom else 8
                county_first = zoom <= 8

            geoid_order = (
                {geoid: i for i, geoid in enumerate(ordered_geoids)}
                if ordered_geoids
                else None
            )

            def default_sort_key(p: ProjectResponse):
                is_county = any(len(g.geoid) == 5 for g in p.geographies)
                type_rank = 0 if (is_county == county_first) else 1
                proximity_rank = (
                    min(
                        (
                            geoid_order[g.geoid]
                            for g in p.geographies
                            if g.geoid in geoid_order
                        ),
                        default=float("inf"),
                    )
                    if geoid_order
                    else 0
                )
                return (type_rank, proximity_rank)

            projects.sort(key=default_sort_key)

    return projects


def get_geoids(db: Session, filters: Optional[ProjectFilters] = None) -> list[str]:
    query = (
        db.query(Geography.geoid)
        .join(Geography.project_geographies)
        .join(ProjectGeography.project)
    )
    if filters:
        project_query = apply_filters(db.query(Project.project_id), filters, db)
        matching_ids = [row.project_id for row in project_query.all()]
        query = query.filter(Project.project_id.in_(matching_ids))

        if filters.geographies:
            geoids = [g.strip() for g in filters.geographies.split(",")]
            query = query.filter(
                or_(*[Geography.geoid.like(f"{geoid}%") for geoid in geoids])
            )

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
