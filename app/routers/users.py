from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas import UserResponse, UserCreate
from ..database import get_db
from ..services import user_service
from ..core.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db, user.email, user.password)


@router.get("/profile", response_model=UserResponse)
def profile(current_user=Depends(get_current_user)):
    return current_user


@router.get("/admin")
def admin_panel(current_user=Depends(require_admin)):
    return {"message": "Welcome admin"}