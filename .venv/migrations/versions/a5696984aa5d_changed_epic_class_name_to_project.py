"""Changed 'epic' class name  to 'project'

Revision ID: a5696984aa5d
Revises: 151c01c7ed6f
Create Date: 2024-03-23 20:39:24.847103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5696984aa5d'
down_revision: Union[str, None] = '151c01c7ed6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('projects')
    op.rename_table('epics', 'projects')

    # Add project_id columns to complex_tasks and tasks
    op.add_column('complex_tasks', sa.Column('project_id', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('project_id', sa.Integer(), nullable=True))

    # Drop the old foreign key constraints
    op.drop_constraint('complex_tasks_epic_id_fkey', 'complex_tasks', type_='foreignkey')
    op.drop_constraint('tasks_epic_id_fkey', 'tasks', type_='foreignkey')

    # Create new foreign key constraints to the projects table
    op.create_foreign_key(None, 'complex_tasks', 'projects', ['project_id'], ['id'])
    op.create_foreign_key(None, 'tasks', 'projects', ['project_id'], ['id'])

    # Drop the epic_id columns
    op.drop_column('complex_tasks', 'epic_id')
    op.drop_column('tasks', 'epic_id')


def downgrade() -> None:
    # Reverse the operations performed in the upgrade function
    op.add_column('tasks', sa.Column('epic_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('complex_tasks', sa.Column('epic_id', sa.INTEGER(), autoincrement=False, nullable=True))

    # Drop the new foreign key constraints
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_constraint(None, 'complex_tasks', type_='foreignkey')

    # Recreate the old foreign key constraints to the epics table
    op.create_foreign_key('tasks_epic_id_fkey', 'tasks', 'epics', ['epic_id'], ['id'])
    op.create_foreign_key('complex_tasks_epic_id_fkey', 'complex_tasks', 'epics', ['epic_id'], ['id'])

    # Drop the project_id columns
    op.drop_column('tasks', 'project_id')
    op.drop_column('complex_tasks', 'project_id')

    # Rename the projects table back to epics
    op.rename_table('projects', 'epics')
