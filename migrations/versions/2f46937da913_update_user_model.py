"""Drop and recreate users table with new structure

Revision ID: abcdef123456
Revises: previous_revision_id
Create Date: 2024-11-28
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# Define the Enum for roles
class UserRoleEnum(str, sa.Enum):
    SUPER_ADMIN = "super_admin"
    CLIENT_ADMIN = "client_admin"
    REFERRER = "referrer"
    REFERRED = "referred"


# revision identifiers, used by Alembic
revision = '2f46937da913'
down_revision = '5b29c8df3122'
branch_labels = None
depends_on = None

def upgrade():
    # Define the ENUM type for roles
    roles_enum = sa.Enum('super_admin', 'client_admin', 'referrer', 'referred', name="user_role_enum")

    # Create the `users` table
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), unique=True, nullable=False, index=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', roles_enum, nullable=False),
        sa.Column('client_id', UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, onupdate=sa.text('NOW()'), nullable=True),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('true'), nullable=False),
    )


def downgrade():
    # Drop the `users` table
    op.drop_table('users')

    # Drop the `user_role_enum` ENUM type
    op.execute("DROP TYPE IF EXISTS user_role_enum;")