"""Init

Revision ID: 66e66722fcb1
Revises: 92b591854e45
Create Date: 2023-12-14 20:06:26.610496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66e66722fcb1'
down_revision: Union[str, None] = '92b591854e45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass
   


def downgrade() -> None:
    pass
