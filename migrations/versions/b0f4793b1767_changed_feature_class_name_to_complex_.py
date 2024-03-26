"""Changed 'feature' class name  to 'complex_task'

Revision ID: b0f4793b1767
Revises: a5696984aa5d
Create Date: 2024-03-24 01:18:23.982747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0f4793b1767'
down_revision: Union[str, None] = 'a5696984aa5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('complex_tasks')
    op.rename_table('features', 'complex_tasks')

    # Add complex_task_id column to tasks
    op.add_column('tasks', sa.Column('complex_task_id', sa.Integer(), nullable=True))

    # Drop the old foreign key constraint
    op.drop_constraint('tasks_feature_id_fkey', 'tasks', type_='foreignkey')

    # Create a new foreign key constraint to the complex_tasks table
    op.create_foreign_key(None, 'tasks', 'complex_tasks', ['complex_task_id'], ['id'])

    # Drop the feature_id column from tasks
    op.drop_column('tasks', 'feature_id')


def downgrade() -> None:
    # Reverse the operations performed in the upgrade function
    op.add_column('tasks', sa.Column('feature_id', sa.INTEGER(), autoincrement=False, nullable=True))

    # Drop the new foreign key constraint
    op.drop_constraint(None, 'tasks', type_='foreignkey')

    # Recreate the old foreign key constraint to the features table
    op.create_foreign_key('tasks_feature_id_fkey', 'tasks', 'features', ['feature_id'], ['id'])

    # Drop the complex_task_id column from tasks
    op.drop_column('tasks', 'complex_task_id')

    # Rename the complex_tasks table back to features
    op.rename_table('complex_tasks', 'features')
