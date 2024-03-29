"""Created user_team_association table

Revision ID: 28d14cc36be8
Revises: 39c72e21a656
Create Date: 2024-02-21 21:13:48.590343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28d14cc36be8'
down_revision: Union[str, None] = '39c72e21a656'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_team_id_fkey', 'users', type_='foreignkey')
    op.drop_constraint('users_managed_team_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'team_id')
    op.drop_column('users', 'managed_team_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('managed_team_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('team_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_managed_team_id_fkey', 'users', 'teams', ['managed_team_id'], ['id'])
    op.create_foreign_key('users_team_id_fkey', 'users', 'teams', ['team_id'], ['id'])
    # ### end Alembic commands ###
