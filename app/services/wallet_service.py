from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from decimal import Decimal

from app.models.wallet import Wallet
from app.models.transaction import Transaction


def get_balance(db: Session, user_id: int):
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()

    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return {"balance": wallet.balance}


def deposit(db: Session, user_id: int, amount: Decimal):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    wallet = (
        db.query(Wallet)
        .filter(Wallet.user_id == user_id)
        .with_for_update()
        .first()
    )

    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet.balance is None:
        wallet.balance = Decimal("0")

    wallet.balance += amount

    transaction = Transaction(
        from_user_id=None,
        to_user_id=user_id,
        amount=amount,
        type="deposit",
        idempotency_key=None,
    )

    db.add(transaction)
    db.commit()
    db.refresh(wallet)

    return {"balance": wallet.balance}


def get_history(
    db: Session,
    user_id: int,
    limit: int = 50,
    offset: int = 0,
):
    return (
        db.query(Transaction)
        .filter(
            (Transaction.from_user_id == user_id) |
            (Transaction.to_user_id == user_id)
        )
        .order_by(
            Transaction.created_at.desc(),
            Transaction.id.desc()
        )
        .offset(offset)
        .limit(limit)
        .all()
    )


def transfer(
    db: Session,
    from_user_id: int,
    to_user_id: int,
    amount: Decimal,
    idempotency_key: str,
):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    if from_user_id == to_user_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to yourself")

    # Idempotency replay
    existing = (
        db.query(Transaction)
        .filter(Transaction.idempotency_key == idempotency_key)
        .first()
    )
    if existing:
        sender_wallet = db.query(Wallet).filter(Wallet.user_id == existing.from_user_id).first()
        receiver_wallet = db.query(Wallet).filter(Wallet.user_id == existing.to_user_id).first()

        return {
            "replayed": True,
            "id": existing.id,
            "from_user_id": existing.from_user_id,
            "to_user_id": existing.to_user_id,
            "amount": existing.amount,
            "type": existing.type,
            "created_at": existing.created_at,
            "idempotency_key": existing.idempotency_key,
            "balance_from": sender_wallet.balance if sender_wallet else Decimal("0"),
            "balance_to": receiver_wallet.balance if receiver_wallet else Decimal("0"),
        }

    # Стабильный порядок блокировки
    first_id, second_id = sorted([from_user_id, to_user_id])

    try:
        wallets = (
            db.query(Wallet)
            .filter(Wallet.user_id.in_([first_id, second_id]))
            .with_for_update()
            .all()
        )

        if len(wallets) != 2:
            raise HTTPException(status_code=404, detail="Wallet not found")

        by_user = {w.user_id: w for w in wallets}
        sender_wallet = by_user[from_user_id]
        receiver_wallet = by_user[to_user_id]

        if sender_wallet.balance is None:
            sender_wallet.balance = Decimal("0")
        if receiver_wallet.balance is None:
            receiver_wallet.balance = Decimal("0")

        if sender_wallet.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        sender_wallet.balance -= amount
        receiver_wallet.balance += amount

        transaction = Transaction(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            amount=amount,
            type="transfer",
            idempotency_key=idempotency_key,
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return {
            "replayed": False,
            "id": transaction.id,
            "from_user_id": transaction.from_user_id,
            "to_user_id": transaction.to_user_id,
            "amount": transaction.amount,
            "type": transaction.type,
            "created_at": transaction.created_at,
            "idempotency_key": transaction.idempotency_key,
            "balance_from": sender_wallet.balance,
            "balance_to": receiver_wallet.balance,
        }

    except IntegrityError:
        db.rollback()

        existing = (
            db.query(Transaction)
            .filter(Transaction.idempotency_key == idempotency_key)
            .first()
        )
        if existing:
            sender_wallet = db.query(Wallet).filter(Wallet.user_id == existing.from_user_id).first()
            receiver_wallet = db.query(Wallet).filter(Wallet.user_id == existing.to_user_id).first()

            return {
                "replayed": True,
                "id": existing.id,
                "from_user_id": existing.from_user_id,
                "to_user_id": existing.to_user_id,
                "amount": existing.amount,
                "type": existing.type,
                "created_at": existing.created_at,
                "idempotency_key": existing.idempotency_key,
                "balance_from": sender_wallet.balance if sender_wallet else Decimal("0"),
                "balance_to": receiver_wallet.balance if receiver_wallet else Decimal("0"),
            }

        raise HTTPException(status_code=409, detail="Idempotency conflict")

    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise