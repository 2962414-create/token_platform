"""add idempotency key and tx indexes (noop - merged elsewhere)

Revision ID: eb6639ca6709
Revises: 0439b202d468
Create Date: 2026-03-03 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "eb6639ca6709"
down_revision: Union[str, Sequence[str], None] = "0439b202d468"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # This revision is intentionally a no-op.
    # The actual changes were applied in another revision (45efac4384a5).
    pass


def downgrade() -> None:
    pass