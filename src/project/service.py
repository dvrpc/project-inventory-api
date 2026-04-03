from datetime import date
from typing import Optional
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session, joinedload, selectinload
from src.geography.models import Geography
from src.keyword.models import Keyword
from src.product.models import Product
from src.product_wpid.models import ProductWpid
from src.project_geography.models import ProjectGeography
from src.project_keyword.models import ProjectKeyword
from src.project.schema import (
    ProjectCreateRequest,
    ProjectFilters,
    ProjectUpdateRequest,
    ProjectResponse,
)
from src.project.models import Project
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

    if any(g.startswith("34") for g in geoids):
        geoids.append("34")
    if any(g.startswith("42") for g in geoids):
        geoids.append("42")

    return (
        query.filter(
            or_(Geography.geoid.in_(geoids), Geography.geo_type == "regional")
        ),
        geoids,
    )


def apply_geographies_filter(query, geographies: str, db: Session):
    geoids = [g.strip() for g in geographies.split(",")]
    is_regional = any(g == "1" for g in geoids)

    if is_regional:
        return query.filter(Geography.geo_type == "regional")

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


def apply_wpids_filter(query, wpids: str, db: Session):
    wpid_list = [w.strip() for w in wpids.split(",")]
    return (
        query.join(ProductWpid, Product.pub_id == ProductWpid.PRODUCTID)
        .filter(ProductWpid.WORKPROGRAMID.in_(wpid_list))
        .distinct()
    )


def expand_geoids(geoids: list[str], db: Session) -> list[str]:

    state_geoids = [g for g in geoids if len(g) == 2]
    county_geoids = [g for g in geoids if len(g) == 5]
    municipality_geoids = [g for g in geoids if len(g) == 10]

    if state_geoids:
        if state_geoids[0] == "42":
            county_geoids = ["42091", "42101", "42017", "42029", "42045"]
        elif state_geoids[0] == "34":
            county_geoids = ["34007", "34015", "34021", "34005"]

    if county_geoids:
        child_geoids = (
            db.query(Geography.geoid).filter(Geography.fips.in_(county_geoids)).all()
        )
        municipality_geoids.extend([g.geoid for g in child_geoids])

    return list(set(state_geoids + municipality_geoids + county_geoids))


def apply_filters(
    query, filters: ProjectFilters, db: Session, is_dvrpc_user: bool = False
):
    if filters.project:
        query = query.filter(Project.project_id == filters.project)
        return query

    query = (
        query.join(Project.project_geographies)
        .join(ProjectGeography.geography)
        .join(Project.product)
        .distinct()
    )

    # Non-DVRPC users can only see projects with 'live' status

    if not is_dvrpc_user:
        query = query.filter(Product.status == "Live")

    if filters.geographies:
        query = apply_geographies_filter(query, filters.geographies, db)
    if filters.keywords:
        query = apply_keywords_filter(query, filters.keywords, db)
    if filters.status and is_dvrpc_user:
        query = query.filter(Product.status == filters.status)
    if filters.yearFrom:
        query = query.filter(Product.pub_date >= date(int(filters.yearFrom), 1, 1))
    if filters.yearTo:
        query = query.filter(Product.pub_date <= date(int(filters.yearTo), 12, 31))
    if filters.wpids:
        query = apply_wpids_filter(query, filters.wpids, db)

    return query


def get_all(
    db: Session, filters: Optional[ProjectFilters] = None, is_dvrpc_user: bool = False
) -> list[ProjectResponse]:
    ordered_geoids = None

    query = db.query(Project).options(
        selectinload(Project.product).selectinload(Product.wpids),
        joinedload(Project.external_product),
        selectinload(Project.needs),
        selectinload(Project.recommendations),
        selectinload(Project.project_geographies).joinedload(
            ProjectGeography.geography
        ),
        selectinload(Project.project_keywords).joinedload(ProjectKeyword.keyword),
    )
    if filters:
        query = apply_filters(query, filters, db, is_dvrpc_user)

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
            zoom = int(filters.zoom) if filters.zoom else 7

            geoid_order = (
                {geoid: i for i, geoid in enumerate(ordered_geoids)}
                if ordered_geoids
                else None
            )

            state_selected = filters.geographies and any(
                len(g.strip()) == 2 for g in filters.geographies.split(",")
            )
            county_selected = filters.geographies and any(
                len(g.strip()) == 5 for g in filters.geographies.split(",")
            )

            def default_sort_key(p: ProjectResponse):
                is_regional = any(g.geo_type == "regional" for g in p.geographies)
                is_state = any(g.geo_type == "state" for g in p.geographies)
                is_county = any(g.geo_type == "county" for g in p.geographies)
                is_muni = any(g.geo_type == "municipality" for g in p.geographies)

                if state_selected:
                    type_rank = 0 if is_state else (1 if is_county else 2)
                elif county_selected:
                    type_rank = 0 if is_county else (1 if is_muni else 2)
                elif zoom <= 7:
                    type_rank = (
                        0
                        if is_regional
                        else (1 if is_state else (2 if is_county else 3))
                    )
                elif zoom == 8:
                    type_rank = (
                        0
                        if is_county
                        else (1 if is_muni else (2 if is_regional else 3))
                    )
                else:  # zoom >= 9
                    type_rank = (
                        0
                        if is_muni
                        else (1 if is_county else (2 if is_regional else 3))
                    )

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


def get_geoids(
    db: Session, filters: Optional[ProjectFilters] = None, is_dvrpc_user: bool = False
) -> list[str]:
    query = (
        db.query(Geography.geoid)
        .join(Geography.project_geographies)
        .join(ProjectGeography.project)
    )
    if filters:
        subquery = apply_filters(
            db.query(Project.project_id), filters, db, is_dvrpc_user
        ).subquery()
        query = query.filter(Project.project_id.in_(subquery))

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
