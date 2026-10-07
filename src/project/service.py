from datetime import date, datetime
from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload, selectinload
from src.geography.models import Geography
from src.keyword.models import Keyword
from src.project.models import Project
from src.project_wpid.models import ProjectWpid
from src.project_geography.models import ProjectGeography
from src.project_keyword.models import ProjectKeyword
from src.project_topic.models import ProjectTopic
from src.project.schema import (
    ProjectDetailResponse,
    ProjectFilters,
)
from src.topic.models import Topic


def map_project_detail(project: Project) -> ProjectDetailResponse | None:
    if project is None:
        return None

    return ProjectDetailResponse(
        pub_id=project.pub_id,
        typecode=project.typecode,
        pub_num=project.pub_num,
        title=project.title,
        subtitle=project.subtitle,
        abstract=project.abstract,
        createdate=project.createdate,
        livedate=project.livedate,
        lastupdatedate=project.lastupdatedate,
        pub_date=project.pub_date,
        s1=project.s1,
        s1_id=project.s1_id,
        status=project.status,
        wpids=project.wpids,
        geographies=[pg.geography for pg in project.project_geographies],
        keywords=[pk.keyword for pk in project.project_keywords],
        topics=[pt.topic for pt in project.project_topics],
    )


def get(db: Session, pub_id: str):
    project = (
        db.query(Project)
        .options(
            joinedload(Project.wpids),
            joinedload(Project.project_geographies).joinedload(
                ProjectGeography.geography
            ),
            joinedload(Project.project_keywords).joinedload(ProjectKeyword.keyword),
            joinedload(Project.project_topics).joinedload(ProjectTopic.topic),
        )
        .filter(Project.pub_id == pub_id)
        .one_or_none()
    )

    return map_project_detail(project)


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
    custom_study_area_pub_ids = [
        location_id
        for location_type, location_id in locations
        if location_type == "csa"
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
                Project.pub_id.in_(custom_study_area_pub_ids),
            )
        ),
        [location_id for _, location_id in locations],
    )


def apply_geographies_filter(query, geographies: str, db: Session):
    from src.gis.service import get_csas_within_geoids

    geoids = [g.strip() for g in geographies.split(",")]
    is_regional = any(g == "1" for g in geoids)
    is_custom_study_area = any(g == "0" for g in geoids)

    if is_regional:
        return query.filter(Geography.geo_type == "regional")

    if is_custom_study_area:
        return query.filter(Geography.geo_type == "csa")

    expanded_geoids = expand_geoids(geoids, db)
    csas_within_geoids = get_csas_within_geoids(expanded_geoids)
   
    return query.filter(
        or_(
            Geography.geoid.in_(expanded_geoids),
            Project.pub_id.in_(csas_within_geoids),
        )
    )


def apply_keywords_filter(query, keywords: str, db: Session):
    keyword_ids = [k.strip() for k in keywords.split(",")]
    return (
        query.join(Project.project_keywords)
        .join(ProjectKeyword.keyword)
        .filter(Keyword.id.in_(keyword_ids))
        .distinct()
    )

def apply_topics_filter(query, topics: str, db: Session):
    topic_ids = [t.strip() for t in topics.split(",")]
    print(topic_ids)
    return (
        query.join(Project.project_topics)
        .join(ProjectTopic.topic)
        .filter(Topic.topic_id.in_(topic_ids))
        .distinct()
    )


def apply_wpids_filter(query, wpids: str, db: Session):
    wpid_list = [w.strip() for w in wpids.split(",")]
    return (
        query.join(ProjectWpid, Project.pub_id == ProjectWpid.PRODUCTID)
        .filter(ProjectWpid.WORKPROGRAMID.in_(wpid_list))
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
        query = query.filter(Project.pub_id == filters.project)
        return query

    query = (
        query.join(Project.project_geographies)
        .join(ProjectGeography.geography)
        .distinct()
    )

    # Non-DVRPC users can only see projects with 'live' status

    if not is_dvrpc_user:
        query = query.filter(Project.status == "Live")

    print(f"Filters: {filters}")
    if filters.geographies:
        query = apply_geographies_filter(query, filters.geographies, db)
    if filters.topics:
        query = apply_topics_filter(query, filters.topics, db)
    if filters.keywords:
        query = apply_keywords_filter(query, filters.keywords, db)
    if filters.status and is_dvrpc_user:
        query = query.filter(Project.status == filters.status)
    if filters.yearFrom:
        query = query.filter(Project.pub_date >= date(int(filters.yearFrom), 1, 1))
    if filters.yearTo:
        query = query.filter(Project.pub_date <= date(int(filters.yearTo), 12, 31))
    if filters.wpids:
        query = apply_wpids_filter(query, filters.wpids, db)

    return query


def get_all(
    db: Session, filters: Optional[ProjectFilters] = None, is_dvrpc_user: bool = False
) -> list[ProjectDetailResponse]:
    ordered_geoids = None

    query = db.query(Project).options(
        selectinload(Project.wpids),
        selectinload(Project.project_geographies).joinedload(
            ProjectGeography.geography
        ),
        selectinload(Project.project_keywords).joinedload(ProjectKeyword.keyword),
        selectinload(Project.project_topics).joinedload(ProjectTopic.topic),
    )
    if filters:
        query = apply_filters(query, filters, db, is_dvrpc_user)

    if filters and filters.bbox:
        query, ordered_geoids = apply_bbox_filter(query, filters.bbox)

    rows = query.all()
    projects = [map_project_detail(p) for p in rows]

    def normalize_date(d):
        if d is None:
            return datetime.min
        if isinstance(d, datetime):
            return d
        return datetime(d.year, d.month, d.day)

    match filters.sort if filters else None:
        case "oldest":
            projects.sort(key=lambda p: normalize_date(p.pub_date))
        case "az":
            projects.sort(key=lambda p: p.title or "")
        case "za":
            projects.sort(key=lambda p: p.title or "", reverse=True)
        case "newest":
            projects.sort(
                key=lambda p: normalize_date(p.pub_date), reverse=True
            )
        case _:
            # Default geographies sort. Groups county & municipality and chooses first based on zoom level
            # Each grouping is sorted by geography proximity to the center of the bounding box,
            # muni and csa get the same rank
            zoom = int(filters.zoom) if filters and filters.zoom else 7

            geoid_order = (
                {geoid: i for i, geoid in enumerate(ordered_geoids)}
                if ordered_geoids
                else None
            )

            state_selected = (
                filters.geographies
                and any(
                    len(g.strip()) == 2 for g in filters.geographies.split(",")
                )
            )
            county_selected = (
                filters.geographies
                and any(
                    len(g.strip()) == 5 for g in filters.geographies.split(",")
                )
            )

            def default_sort_key(p: ProjectDetailResponse):
                is_regional = any(g.geo_type == "regional" for g in p.geographies)
                is_state = any(g.geo_type == "state" for g in p.geographies)
                is_county = any(g.geo_type == "county" for g in p.geographies)
                is_muni = any(g.geo_type == "municipality" for g in p.geographies)
                is_csa = any(g.geo_type == "csa" for g in p.geographies)

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
                        if is_muni or is_csa
                        else (1 if is_county else (2 if is_regional else 3))
                    )

                proximity_rank = (
                    min(
                        [
                            geoid_order[g.geoid]
                            for g in p.geographies
                            if g.geoid in geoid_order
                        ]
                        + (
                            [geoid_order[p.pub_id]]
                            if p.pub_id in geoid_order
                            else []
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
            db.query(Project.pub_id), filters, db, is_dvrpc_user
        ).scalar_subquery()
        query = query.filter(Project.pub_id.in_(subquery))

        if filters.geographies:
            geoids = [g.strip() for g in filters.geographies.split(",")]
            query = query.filter(
                or_(*[Geography.geoid.like(f"{geoid}%") for geoid in geoids])
            )

    return [row.geoid for row in query.all()]
