from pydantic import BaseModel, EmailStr


# 🔹 Схема для создания пользователя (при регистрации)
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# 🔹 Схема для ответа (не содержит пароль!)
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True  # для SQLAlchemy (Pydantic v2)

class Token(BaseModel):
    access_token: str
    token_type: str