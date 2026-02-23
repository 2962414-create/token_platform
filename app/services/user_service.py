from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..repositories import user_repository
from ..security import get_password_hash


def register_user(db: Session, email: str, password: str):
    existing_user = user_repository.get_user_by_email(db, email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = get_password_hash(password)

    return user_repository.create_user(db, email, hashed)


def get_users(db: Session):
    return user_repository.get_all_users(db)