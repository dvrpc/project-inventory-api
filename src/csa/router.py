from fastapi import APIRouter
from src.csa.service import get_csa_polygon


router = APIRouter()

@router.get("/{pub_id}")
def find_csa_polygon(pub_id: str):
    return get_csa_polygon(pub_id)
