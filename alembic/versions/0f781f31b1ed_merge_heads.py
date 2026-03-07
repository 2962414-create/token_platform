"""merge heads

Revision ID: 0f781f31b1ed
Revises: 45efac4384a5, eb6639ca6709
Create Date: 2026-03-05 15:06:40.751898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f781f31b1ed'
down_revision: Union[str, Sequence[str], None] = ('45efac4384a5', 'eb6639ca6709')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
