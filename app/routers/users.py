from fastapi import APIRouter, Depends
from app.models import User
from app.schemas import UserResponse
from app.core.dependencies import get_current_user, require_admin

router = APIRouter()


@router.get("/profile", response_model=UserResponse)
def profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/admin")
def admin_panel(current_user: User = Depends(require_admin)):
    return {"message": "Welcome admin"}