"""Adjusted child-parent relations for WorkItem subclasses

Revision ID: 88029eb7a1e2
Revises: 712c301f61c1
Create Date: 2024-03-09 12:15:51.861447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88029eb7a1e2'
down_revision: Union[str, None] = '712c301f61c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###