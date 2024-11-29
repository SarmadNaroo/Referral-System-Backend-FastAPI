"""relation one-one created clients users

Revision ID: 04c8989ea6e4
Revises: 5faa6fa1df70
Create Date: 2024-11-29 12:16:34.267395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04c8989ea6e4'
down_revision: Union[str, None] = '5faa6fa1df70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clients', sa.Column('user_id', sa.UUID(), nullable=False))
    op.create_unique_constraint(None, 'clients', ['user_id'])
    op.create_foreign_key(None, 'clients', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'clients', type_='foreignkey')
    op.drop_constraint(None, 'clients', type_='unique')
    op.drop_column('clients', 'user_id')
    # ### end Alembic commands ###
