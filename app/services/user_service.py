from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.wallet import Wallet
import app.repositories.user_repository as user_repository
from app.security import get_password_hash


def register_user(db: Session, email: str, password: str):
    existing_user = user_repository.get_user_by_email(db, email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = get_password_hash(password)

    user = user_repository.create_user(db, email, hashed)

    wallet = Wallet(user_id=user.id)
    db.add(wallet)

    db.commit()
    db.refresh(user)

    return user


def get_users(db: Session):
    return user_repository.get_all_users(db)