"""add last few column to posts table

Revision ID: e7efd4cf6e38
Revises: 6c9004fd08e4
Create Date: 2022-08-22 19:24:53.061439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7efd4cf6e38'
down_revision = '6c9004fd08e4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column("published", sa.Boolean, server_default="TRUE", nullable=False))
    op.add_column('posts', sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, 
    server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
