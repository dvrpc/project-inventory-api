from fastapi import APIRouter, Depends
from geography.router import router as geography_router
from agency.router import router as agency_router

api_router = APIRouter()

api_router.include_router(geography_router, prefix="/geography", tags=["geography"])
api_router.include_router(agency_router, prefix="/agency", tags=["agency"])