"""Added managed teams to the class User

Revision ID: 96079bd0abb5
Revises: 28d14cc36be8
Create Date: 2024-02-21 21:18:21.199778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96079bd0abb5'
down_revision: Union[str, None] = '28d14cc36be8'
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
