"""add event curator reference

Revision ID: a0d4b6ca0a6d
Revises: be31202421d8
Create Date: 2025-11-09 12:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a0d4b6ca0a6d"
down_revision: Union[str, Sequence[str], None] = "be31202421d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("events", sa.Column("curator_id", sa.Uuid(), nullable=True))
    op.create_index("ix_events_curator_id", "events", ["curator_id"], unique=False)
    op.create_foreign_key(
        "fk_events_curator_id_users",
        "events",
        "users",
        ["curator_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.execute("UPDATE events SET curator_id = creator_id")
    op.alter_column("events", "curator_id", existing_type=sa.Uuid(), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_events_curator_id_users", "events", type_="foreignkey")
    op.drop_index("ix_events_curator_id", table_name="events")
    op.drop_column("events", "curator_id")

