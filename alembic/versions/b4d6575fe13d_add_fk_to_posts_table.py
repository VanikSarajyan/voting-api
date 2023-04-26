"""add FK to posts table

Revision ID: b4d6575fe13d
Revises: 7aff4d21c8da
Create Date: 2023-04-26 10:13:41.927318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b4d6575fe13d"
down_revision = "7aff4d21c8da"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer, nullable=False))
    op.create_foreign_key(
        "posts_users_pk",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_pk", table_name="posts")
    op.drop_column("posts", "user_id")
