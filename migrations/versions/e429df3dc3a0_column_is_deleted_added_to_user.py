"""Column is_deleted added to User

Revision ID: e429df3dc3a0
Revises: e63fd28ad63a
Create Date: 2024-03-29 22:55:48.581569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e429df3dc3a0'
down_revision: Union[str, None] = 'e63fd28ad63a'
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
