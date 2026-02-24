from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import auth_service
from ..schemas import Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    token = auth_service.login_user(
        db,
        form_data.username,
        form_data.password
    )

    return Token(
        access_token=token,
        token_type="bearer"
    )