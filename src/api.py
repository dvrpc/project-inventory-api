from fastapi import APIRouter, Depends
from src.geography.router import router as geography_router
from src.agency_group.router import router as agency_group_router
from src.attachment.router import router as attachment_router
from src.contact.router import router as contact_router
from src.need.router import router as need_router
from src.project.router import router as project_router
from src.project_geography.router import router as project_geography_router
from src.recommendation.router import router as recommendation_router
from src.gis.router import router as geo_router
from src.keyword.router import router as keyword_router
from src.project_keyword.router import router as project_keyword_router
from src.project_wpid.router import router as project_wpid_router
from src.topic.router import router as topic_router
from src.csa.router import router as csa_router
from src.user.router import router as user_router
api_router = APIRouter()

api_router.include_router(geography_router, prefix="/geography", tags=["geography"])
api_router.include_router(
    agency_group_router, prefix="/agency-group", tags=["agency-group"]
)
api_router.include_router(project_router, prefix="/project", tags=["project"])
api_router.include_router(geo_router, prefix="/gis", tags=["gis"])
api_router.include_router(keyword_router, prefix="/keyword", tags=["keyword"])
api_router.include_router(topic_router, prefix="/topic", tags=["topic"])
api_router.include_router(
    project_wpid_router, prefix="/project-wpid", tags=["project-wpid"]
)
api_router.include_router(csa_router, prefix="/csa", tags=["csa"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
