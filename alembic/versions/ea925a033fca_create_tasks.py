"""create tasks

Revision ID: ea925a033fca
Revises: 5e04e75e1f08
Create Date: 2022-04-22 12:55:54.039424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea925a033fca'
down_revision = '5e04e75e1f08'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tasks',
        sa.Column("id",sa.Integer,primary_key = True),
        sa.Column("title",sa.String,nullable = False),
        sa.Column('description',sa.String,nullable = False),
        sa.Column('user_id',sa.Integer,nullable = False),
        sa.Column('completed',sa.Boolean),
        sa.Column('initial_date',sa.Date,nullable = False),
        sa.Column('last_date',sa.Date),
        sa.Column('user_order',sa.Integer,nullable = False),
        sa.Column('last_update',sa.Date,nullable = False),
        sa.Column('deleted',sa.Date,nullable = True),
    )


def downgrade():
    op.drop_table('tasks')
