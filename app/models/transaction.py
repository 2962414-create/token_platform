from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    amount = Column(Numeric(18, 2), nullable=False)
    type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    idempotency_key = Column(String, nullable=True, unique=True)

    from_user = relationship("User", foreign_keys=[from_user_id])
    to_user = relationship("User", foreign_keys=[to_user_id])


Index("ix_transactions_from_user_id", Transaction.from_user_id)
Index("ix_transactions_to_user_id", Transaction.to_user_id)