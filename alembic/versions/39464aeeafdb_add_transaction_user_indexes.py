"""add transaction user indexes

Revision ID: 39464aeeafdb
Revises: 68206559d808
Create Date: 2026-02-28 17:23:27.680860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39464aeeafdb'
down_revision: Union[str, Sequence[str], None] = '68206559d808'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_index(
        "ix_transactions_user_from",
        "transactions",
        ["from_user_id"],
        unique=False,
    )
    op.create_index(
        "ix_transactions_user_to",
        "transactions",
        ["to_user_id"],
        unique=False,
    )


def downgrade():
    op.drop_index("ix_transactions_user_from", table_name="transactions")
    op.drop_index("ix_transactions_user_to", table_name="transactions")