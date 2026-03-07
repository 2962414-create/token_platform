from fastapi import APIRouter, Depends, Query, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import wallet_service
from app.core.dependencies import get_current_user
from app.schemas import (
    BalanceResponse,
    TransactionResponse,
    DepositRequest,
    TransferRequest,
    TransferResponse,
)

router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.post("/deposit", response_model=BalanceResponse)
def deposit_money(
    request: DepositRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return wallet_service.deposit(db, current_user.id, request.amount)


@router.get("/balance", response_model=BalanceResponse)
def get_balance(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return wallet_service.get_balance(db, current_user.id)


@router.get("/history", response_model=list[TransactionResponse])
def history(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return wallet_service.get_history(db, current_user.id, limit, offset)


@router.post("/transfer", response_model=TransferResponse)
def transfer_money(
    request: TransferRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
):
    return wallet_service.transfer(
        db=db,
        from_user_id=current_user.id,
        to_user_id=request.to_user_id,
        amount=request.amount,
        idempotency_key=idempotency_key,
    )