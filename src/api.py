from fastapi import APIRouter, Depends
from src.geography.router import router as geography_router
from src.agency.router import router as agency_router
from src.attachment.router import router as attachment_router
from src.contact.router import router as contact_router
from src.external_product.router import router as external_product_router
from src.need.router import router as need_router
from src.product.router import router as product_router
from src.project.router import router as project_router
from src.project_geography.router import router as project_geography_router
from src.recommendation.router import router as recommendation_router
from src.gis.router import router as geo_router
from src.keyword.router import router as keyword_router
from src.project_keyword.router import router as project_keyword_router
from src.product_wpid.router import router as product_wpid_router

api_router = APIRouter()

api_router.include_router(geography_router, prefix="/geography", tags=["geography"])
api_router.include_router(agency_router, prefix="/agency", tags=["agency"])
api_router.include_router(attachment_router, prefix="/attachment", tags=["attachment"])
api_router.include_router(contact_router, prefix="/contact", tags=["contact"])
api_router.include_router(
    external_product_router, prefix="/external-product", tags=["external-product"]
)
api_router.include_router(need_router, prefix="/need", tags=["need"])
api_router.include_router(product_router, prefix="/product", tags=["product"])
api_router.include_router(project_router, prefix="/project", tags=["project"])
api_router.include_router(
    project_geography_router, prefix="/project-geography", tags=["project-geography"]
)
api_router.include_router(
    recommendation_router, prefix="/recommendation", tags=["recommendation"]
)
api_router.include_router(geo_router, prefix="/gis", tags=["gis"])
api_router.include_router(keyword_router, prefix="/keyword", tags=["keyword"])
api_router.include_router(
    project_keyword_router, prefix="/project-keyword", tags=["project-keyword"]
)
api_router.include_router(
    product_wpid_router, prefix="/product-wpid", tags=["product-wpid"]
)
