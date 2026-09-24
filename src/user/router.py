from fastapi import APIRouter, Depends

from src.auth.validate import require_admin

router = APIRouter()

@router.get("/")
async def get_current_user(admin=Depends(require_admin)):
    return {"is_admin": True}