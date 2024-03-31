"""Column is_deleted added to User

Revision ID: e63fd28ad63a
Revises: 1099755ca522
Create Date: 2024-03-29 22:55:00.809366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e63fd28ad63a'
down_revision: Union[str, None] = '1099755ca522'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_deleted')
    # ### end Alembic commands ###