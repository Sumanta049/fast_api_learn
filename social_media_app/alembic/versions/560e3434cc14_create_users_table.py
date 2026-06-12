"""create users table

Revision ID: 560e3434cc14
Revises: 4873de1673ba
Create Date: 2026-06-12 17:50:07.939981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '560e3434cc14'
down_revision: Union[str, Sequence[str], None] = '4873de1673ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users_alembic',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    pass


def downgrade() -> None:
    op.drop_table('users_alembic')
    pass


#alembic current 
#alembic history