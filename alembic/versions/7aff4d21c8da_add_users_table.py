"""add users table

Revision ID: 7aff4d21c8da
Revises: 1b8c8218fbbc
Create Date: 2023-04-26 10:09:09.109093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7aff4d21c8da"
down_revision = "1b8c8218fbbc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
