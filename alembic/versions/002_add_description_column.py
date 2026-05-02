"""add description column

Revision ID: 002
Revises: 001
Create Date: 2026-04-28 10:30:00
"""
from alembic import op
import sqlalchemy as sa

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('product', sa.Column('description', sa.String(), nullable=False, server_default=''))

def downgrade() -> None:
    op.drop_column('product', 'description')
