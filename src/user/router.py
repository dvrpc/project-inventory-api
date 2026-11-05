from fastapi import APIRouter, Depends

from src.auth.validate import get_optional_dvrpc_user, require_admin

router = APIRouter()

@router.get("")
async def get_current_user(is_dvrpc_user: bool = Depends(get_optional_dvrpc_user)):
    return is_dvrpc_user