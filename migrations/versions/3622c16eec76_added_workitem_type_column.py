"""Added WorkItem.TYPE column

Revision ID: 3622c16eec76
Revises: f84349dd245d
Create Date: 2024-03-09 00:27:50.915086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3622c16eec76'
down_revision: Union[str, None] = 'f84349dd245d'
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
