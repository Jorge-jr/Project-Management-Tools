"""Check for class name changes

Revision ID: 851964f0d3d3
Revises: b0f4793b1767
Create Date: 2024-03-24 01:55:36.797756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '851964f0d3d3'
down_revision: Union[str, None] = 'b0f4793b1767'
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