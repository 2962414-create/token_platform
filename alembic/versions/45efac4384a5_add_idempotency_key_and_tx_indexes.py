"""add idempotency key and tx indexes

Revision ID: 45efac4384a5
Revises: 39464aeeafdb
Create Date: 2026-03-01 16:48:43.715116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45efac4384a5'
down_revision: Union[str, Sequence[str], None] = '39464aeeafdb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1) колонка idempotency_key
    op.add_column("transactions", sa.Column("idempotency_key", sa.String(), nullable=True))

    # 2) уникальность на idempotency_key
    op.create_unique_constraint(
        "uq_transactions_idempotency_key",
        "transactions",
        ["idempotency_key"]
    )

    # 3) индексы для ускорения выборок истории
    op.create_index(
        "ix_transactions_from_user_id",
        "transactions",
        ["from_user_id"],
        unique=False
    )
    op.create_index(
        "ix_transactions_to_user_id",
        "transactions",
        ["to_user_id"],
        unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_transactions_to_user_id", table_name="transactions")
    op.drop_index("ix_transactions_from_user_id", table_name="transactions")

    op.drop_constraint(
        "uq_transactions_idempotency_key",
        "transactions",
        type_="unique"
    )

    op.drop_column("transactions", "idempotency_key")