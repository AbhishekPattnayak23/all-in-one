"""Add password reset fields to users table

Revision ID: add_reset_fields_20240101
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_reset_fields_20240101'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add password reset fields
    op.add_column('users', sa.Column('reset_token', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('reset_token_expires_at', sa.DateTime(), nullable=True))
    
    # Create indexes
    op.create_index('ix_users_reset_token', 'users', ['reset_token'], unique=True)

def downgrade():
    # Remove indexes
    op.drop_index('ix_users_reset_token', table_name='users')
    
    # Remove password reset fields
    op.drop_column('users', 'reset_token_expires_at')
    op.drop_column('users', 'reset_token')
