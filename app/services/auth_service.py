from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from jose import JWTError, jwt

from app.models import User
from app.models.refresh_token import RefreshToken
from app.core.security import verify_password, create_access_token
from app.core.config import settings


# 🔐 LOGIN
def login_user(db: Session, email: str, password: str):

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 🔹 ACCESS TOKEN
    access_token = create_access_token(
        data={"sub": user.email, "type": "access"},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # 🔹 REFRESH TOKEN
    refresh_expires = timedelta(days=7)

    refresh_token = create_access_token(
        data={"sub": user.email, "type": "refresh"},
        expires_delta=refresh_expires
    )

    # 🔹 Сохраняем refresh в БД
    db_refresh = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=datetime.utcnow() + refresh_expires
    )

    db.add(db_refresh)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# 🔄 REFRESH (с rotation)
def refresh_access_token(db: Session, refresh_token: str):

    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email: str = payload.get("sub")
        token_type: str = payload.get("type")

        if email is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # 🔎 Проверяем токен в БД
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if not db_token:
        raise HTTPException(status_code=401, detail="Token not found")

    # ⏳ Проверяем срок
    if db_token.expires_at < datetime.utcnow():
        db.delete(db_token)
        db.commit()
        raise HTTPException(status_code=401, detail="Token expired")

    # 👤 Получаем пользователя
    user = db.query(User).filter(User.id == db_token.user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # 🗑 ROTATION: удаляем старый refresh
    db.delete(db_token)

    # 🔹 Новый access
    access_token = create_access_token(
        data={"sub": user.email, "type": "access"},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # 🔹 Новый refresh
    refresh_expires = timedelta(days=7)

    new_refresh_token = create_access_token(
        data={"sub": user.email, "type": "refresh"},
        expires_delta=refresh_expires
    )

    db_refresh = RefreshToken(
        token=new_refresh_token,
        user_id=user.id,
        expires_at=datetime.utcnow() + refresh_expires
    )

    db.add(db_refresh)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


# 🚪 LOGOUT
def logout_user(db: Session, refresh_token: str):

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if not db_token:
        raise HTTPException(status_code=404, detail="Token not found")

    db.delete(db_token)
    db.commit()

    return {"message": "Successfully logged out"}