from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import auth_service
from ..schemas import RefreshRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return auth_service.login_user(
        db,
        form_data.username,
        form_data.password
    )


@router.post("/refresh")
def refresh_token(
    request: RefreshRequest,
    db: Session = Depends(get_db)
):
    return auth_service.refresh_access_token(db, request.refresh_token)

@router.post("/logout")
def logout(
    request: RefreshRequest,
    db: Session = Depends(get_db)
):
    return auth_service.logout_user(db, request.refresh_token)