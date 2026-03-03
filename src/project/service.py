
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from src.geography.models import Geography
from src.project_geography.models import ProjectGeography
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
        geographies=project.geographies
    )

def get_unmapped(db : Session, project_id: int):
    return db.query(Project).filter(Project.project_id == project_id).one_or_none()

def get(db : Session, project_id: int):
    project = (
        db.query(Project)
            .options(
                joinedload(Project.product),
                joinedload(Project.external_product),
                )
                .filter(Project.project_id == project_id)
                .one_or_none()
    )

    return map_project(project)

def get_all(db: Session, filters: Optional[ProjectFilters] = None) -> list[ProjectResponse]:
    query = db.query(Project)
    if filters.bbox:
        coords = filters.bbox.split(",")
        geoids = get_geoids_in_bounding_box(float(coords[0]), float(coords[1]), float(coords[2]), float(coords[3]))
        query = query.join(Project.geographies).filter(Geography.geoid.in_(geoids))
        
    return [map_project(p) for p in query.all()]


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
