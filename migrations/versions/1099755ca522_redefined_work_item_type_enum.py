"""Redefined work_item_type enum

Revision ID: 1099755ca522
Revises: 3184c6990dc2
Create Date: 2024-03-24 15:13:56.137366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1099755ca522'
down_revision: Union[str, None] = '3184c6990dc2'
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