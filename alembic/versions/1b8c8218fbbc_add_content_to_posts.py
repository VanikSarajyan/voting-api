"""add content to posts

Revision ID: 1b8c8218fbbc
Revises: b8e67aa40fbd
Create Date: 2023-04-25 20:53:54.044790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1b8c8218fbbc"
down_revision = "b8e67aa40fbd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
