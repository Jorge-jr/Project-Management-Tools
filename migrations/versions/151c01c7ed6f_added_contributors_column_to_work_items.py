"""Added 'contributors' column to work_items

Revision ID: 151c01c7ed6f
Revises: db166bbd62fa
Create Date: 2024-03-20 23:09:46.347845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '151c01c7ed6f'
down_revision: Union[str, None] = 'db166bbd62fa'
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