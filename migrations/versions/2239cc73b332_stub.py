"""Stub migration to restore missing revision 2239cc73b332

This file is intentionally empty (no schema changes). It restores a missing node in
Alembic's revision graph so autogenerate/upgrade can run. If you later replace this
with the real migration, remove this stub.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2239cc73b332'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # stub: no schema changes
    pass


def downgrade():
    pass
