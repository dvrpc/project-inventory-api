from datetime import datetime
from typing import Optional

from sqlalchemy import false, or_
from sqlalchemy.orm import Session, joinedload, selectinload

from src.agency.models import Agency
from src.external_project.models import ExternalProject
from src.external_project_geography.models import ExternalProjectGeography
from src.geography.models import Geography
from src.project.schema import ProjectDetailResponse, ProjectFilters


def map_external_project(project: ExternalProject) -> ProjectDetailResponse | None:
    if project is None:
        return None
    # return ProjectDetailResponse(
    #     id=project.pub_id,
    #     title=project.title,
    #     abstract=project.abstract,
    #     pub_date=project.pub_date,
    #     contact_name=project.s1,
    #     contact_email=email,
    #     status=project.status,
    #     wpids=project.wpids,
    #     geographies=[pg.geography for pg in project.project_geographies],
    #     keywords=[pk.keyword for pk in project.project_keywords],
    #     topics=[pt.topic for pt in project.project_topics],
    # )

    return ProjectDetailResponse(
        id="EX" + str(project.id),
        title=project.title,
        abstract=project.abstract,
        pub_date=datetime(project.year, 1, 1) if project.year else None,
        contact_name=None,
        contact_email=None,
        status=project.status,
        project_link=project.project_link,
        agency=project.agency.name if project.agency else project.agency_raw,
        agency_group=(
            project.agency.agency_group.name
            if project.agency and project.agency.agency_group
            else None
        ),

        funding_source=project.funding_source,
        internal=False,
        thumbnail_link=None,
        wpids=[],
        geographies=[
            link.geography for link in project.external_project_geographies
        ],
        keywords=[],
        topics=[],
    )


def apply_bbox_filter(query, bbox: str):
    from src.gis.service import get_bounding_box_locations

    coords = bbox.split(",")
    locations = get_bounding_box_locations(
        float(coords[0]), float(coords[1]), float(coords[2]), float(coords[3])
    )
    geoids = [
        location_id
        for location_type, location_id in locations
        if location_type == "geoid"
    ]

    if any(g.startswith("34") for g in geoids):
        geoids.append("34")
    if any(g.startswith("42") for g in geoids):
        geoids.append("42")

    return (
        query.filter(
            or_(
                Geography.geoid.in_(geoids),
                Geography.geo_type == "regional",
            )
        ),
        [location_id for _, location_id in locations],
    )


def apply_geographies_filter(
    query, geographies: str, db: Session, show_more: bool = False
):
    from src.project.service import expand_geoids

    geoids = [g.strip() for g in geographies.split(",")]

    # skip show more if more than 1 geography is selected
    if len(geoids) > 1:
        show_more = False

    # skip show more if no muni geoids present
    if show_more:
        muni_geoids = [g for g in geoids if len(g) == 10]
        if not muni_geoids:
            show_more = False

    # Expands the geoids to include parents, for use
    # in "show more" section.
    if show_more:
        show_more_geoids = []
        for geoid in geoids:
            if len(geoid) == 10:
                show_more_geoids.append(geoid[0:5])
                show_more_geoids.append(geoid[0:2])

        geoids = list(set(show_more_geoids + geoids))

    if any(g == "1" for g in geoids):
        return query.filter(Geography.geo_type == "regional")

    if not show_more:
        geoids = expand_geoids(geoids, db)

    return query.filter(Geography.geoid.in_(geoids))


def apply_agency_filter(query, agencies: str, db: Session):

    group_ids = [group_id.strip() for group_id in agencies.split(",")]
    group_ids = [group_id for group_id in group_ids if group_id != "0"]

    if not group_ids:
        return query.filter(false())
    return query.filter(
        ExternalProject.agency.has(Agency.agency_group_id.in_(group_ids))
    )


def apply_filters(
    query, filters: ProjectFilters, db: Session, is_dvrpc_user: bool = False
):
    if filters.project:
        return query.filter(ExternalProject.source_key == filters.project)

    if filters.fs:
        # DVRPC projects are internal projects only.
        if filters.fs == "DVRPC":
            return query.filter(false())
        query = query.filter(ExternalProject.funding_source == filters.fs)

    if filters.ag:
        query = apply_agency_filter(query, filters.ag, db)

    # External projects have no keywords, topics, or WPIDs
    if filters.keywords or filters.topics or filters.wpids:
        return query.filter(false())

    if not is_dvrpc_user:
        query = query.filter(ExternalProject.status == "Live")

    if filters.status and is_dvrpc_user:
        query = query.filter(ExternalProject.status == filters.status)
    if filters.yearFrom:
        query = query.filter(ExternalProject.year >= int(filters.yearFrom))
    if filters.yearTo:
        query = query.filter(ExternalProject.year <= int(filters.yearTo))

    if filters.geographies or (filters.bbox and not filters.showMore):
        geo_query = db.query(ExternalProjectGeography.external_project_id).join(
            Geography, ExternalProjectGeography.geoid == Geography.geoid
        )
        if filters.geographies:
            geo_query = apply_geographies_filter(
                geo_query,
                filters.geographies,
                db,
                filters.showMore,
            )
        if filters.bbox and not filters.showMore:
            geo_query, _ = apply_bbox_filter(geo_query, filters.bbox)
        query = query.filter(ExternalProject.id.in_(geo_query))

    return query


def get_geoids(
    db: Session, filters: Optional[ProjectFilters] = None, is_dvrpc_user: bool = False
) -> list[str]:
    query = db.query(ExternalProjectGeography.geoid)
    if filters:
        subquery = apply_filters(
            db.query(ExternalProject.id), filters, db, is_dvrpc_user
        ).scalar_subquery()
        query = query.filter(
            ExternalProjectGeography.external_project_id.in_(subquery)
        )

        if filters.geographies:
            geoids = [g.strip() for g in filters.geographies.split(",")]
            query = query.filter(
                or_(
                    *[
                        ExternalProjectGeography.geoid.like(f"{geoid}%")
                        for geoid in geoids
                    ]
                )
            )

    return [row.geoid for row in query.all()]


def get_all(
    db: Session, filters: Optional[ProjectFilters] = None, is_dvrpc_user: bool = False
) -> list[ProjectDetailResponse]:
    query = (
        db.query(ExternalProject)
        .options(
            selectinload(ExternalProject.external_project_geographies).joinedload(
                ExternalProjectGeography.geography
            ),
            joinedload(ExternalProject.agency).joinedload(Agency.agency_group),
        )
        .filter(ExternalProject.external_project_geographies.any())
    )
    if filters:
        query = apply_filters(query, filters, db, is_dvrpc_user)

    return [map_external_project(project) for project in query.all()]
