from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..repositories import user_repository
from ..security import verify_password, create_access_token
from ..models import User


def authenticate_user(db: Session, email: str, password: str):
    user = user_repository.get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    return user


def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    token = create_access_token(data={"sub": user.email})
    return token