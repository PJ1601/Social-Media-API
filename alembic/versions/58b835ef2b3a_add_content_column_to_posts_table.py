"""add content column to posts table

Revision ID: 58b835ef2b3a
Revises: 88b9b07adb53
Create Date: 2022-08-22 18:24:52.734030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58b835ef2b3a'
down_revision = '88b9b07adb53'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
