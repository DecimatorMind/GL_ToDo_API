"""create tables

Revision ID: 5e04e75e1f08
Revises: ba751f30a4ed
Create Date: 2022-04-22 12:44:38.747884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e04e75e1f08'
down_revision = ''
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id',sa.Integer,primary_key = True),
        sa.Column('name',sa.String),
        sa.Column('email',sa.String,unique = True),
        sa.Column('password',sa.String)
    )


def downgrade():
    op.drop_table('users')
