"""Column is_deleted added to User

Revision ID: 3a17721b2b92
Revises: e429df3dc3a0
Create Date: 2024-03-29 22:59:30.298269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a17721b2b92'
down_revision: Union[str, None] = 'e429df3dc3a0'
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
