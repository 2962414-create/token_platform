from pydantic import BaseModel, EmailStr
from decimal import Decimal
from typing import Optional
from datetime import datetime


# =========================
# USER
# =========================

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# =========================
# AUTH
# =========================

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshRequest(BaseModel):
    refresh_token: str


# =========================
# WALLET
# =========================

class DepositRequest(BaseModel):
    amount: Decimal

    class Config:
        json_encoders = {
            Decimal: lambda v: str(v)
        }


class BalanceResponse(BaseModel):
    balance: Decimal

    class Config:
        json_encoders = {
            Decimal: lambda v: str(v)
        }


class TransactionResponse(BaseModel):
    id: int
    from_user_id: Optional[int]
    to_user_id: Optional[int]
    amount: Decimal
    type: str
    created_at: Optional[datetime]
    idempotency_key: Optional[str]

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: str(v)
        }


class TransferRequest(BaseModel):
    to_user_id: int
    amount: Decimal


class TransferResponse(BaseModel):
    replayed: bool
    id: int
    from_user_id: int
    to_user_id: int
    amount: Decimal
    type: str
    created_at: Optional[datetime]
    idempotency_key: Optional[str]
    balance_from: Decimal
    balance_to: Decimal

    class Config:
        json_encoders = {
            Decimal: lambda v: str(v)
        }