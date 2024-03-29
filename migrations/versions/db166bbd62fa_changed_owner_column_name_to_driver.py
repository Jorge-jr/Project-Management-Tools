"""Changed owner column name to driver

Revision ID: db166bbd62fa
Revises: 694d6dc8a6e1
Create Date: 2024-03-20 22:48:58.093555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db166bbd62fa'
down_revision: Union[str, None] = '694d6dc8a6e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('work_items', sa.Column('driver_id', sa.Integer(), nullable=True))
    op.drop_constraint('work_items_owner_id_fkey', 'work_items', type_='foreignkey')
    op.create_foreign_key(None, 'work_items', 'users', ['driver_id'], ['id'])
    op.drop_column('work_items', 'owner_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('work_items', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'work_items', type_='foreignkey')
    op.create_foreign_key('work_items_owner_id_fkey', 'work_items', 'users', ['owner_id'], ['id'])
    op.drop_column('work_items', 'driver_id')
    # ### end Alembic commands ###
