"""Adjusted child-parent relations for WorkItem subclasses #2

Revision ID: 15b8951057ce
Revises: 88029eb7a1e2
Create Date: 2024-03-09 12:30:06.772021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15b8951057ce'
down_revision: Union[str, None] = '88029eb7a1e2'
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
