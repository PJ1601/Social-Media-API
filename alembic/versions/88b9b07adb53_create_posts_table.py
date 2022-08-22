"""create posts table

Revision ID: 88b9b07adb53
Revises: 
Create Date: 2022-08-21 18:59:36.573189

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88b9b07adb53'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    sa.drop_table('posts') 
    pass
