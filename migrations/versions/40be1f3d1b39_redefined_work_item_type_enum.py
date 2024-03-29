"""Redefined work_item_type enum

Revision ID: 40be1f3d1b39
Revises: 425dfefede88
Create Date: 2024-03-24 15:11:28.941260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40be1f3d1b39'
down_revision: Union[str, None] = '425dfefede88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('work_items', sa.Column('work_item_type', sa.Enum('PROJECT', 'COMPLEX_TASK', 'TASK', name='workitemtype'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('work_items', 'work_item_type')
    # ### end Alembic commands ###
