"""add foreign key to posts table

Revision ID: 6c9004fd08e4
Revises: 8b208663c614
Create Date: 2022-08-22 19:12:36.919779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c9004fd08e4'
down_revision = '8b208663c614'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users",
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column("posts", 'owner_id')
    pass
