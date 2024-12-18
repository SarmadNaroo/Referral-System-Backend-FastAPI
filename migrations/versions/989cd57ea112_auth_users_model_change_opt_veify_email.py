"""auth users model change opt veify email

Revision ID: 989cd57ea112
Revises: 04c8989ea6e4
Create Date: 2024-11-29 17:29:25.858212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '989cd57ea112'
down_revision: Union[str, None] = '04c8989ea6e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(), nullable=False))
    op.add_column('users', sa.Column('is_email_verified', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('otp', sa.String(), nullable=True))
    op.add_column('users', sa.Column('otp_expires_at', sa.DateTime(), nullable=True))
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_column('users', 'otp_expires_at')
    op.drop_column('users', 'otp')
    op.drop_column('users', 'is_email_verified')
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
