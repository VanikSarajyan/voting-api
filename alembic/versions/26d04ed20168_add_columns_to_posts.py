"""add columns to posts

Revision ID: 26d04ed20168
Revises: b4d6575fe13d
Create Date: 2023-04-26 10:18:31.987992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "26d04ed20168"
down_revision = "b4d6575fe13d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean, nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
