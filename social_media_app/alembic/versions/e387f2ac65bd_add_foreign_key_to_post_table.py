"""add foreign key to post table

Revision ID: e387f2ac65bd
Revises: 560e3434cc14
Create Date: 2026-06-12 17:53:04.862614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e387f2ac65bd'
down_revision: Union[str, Sequence[str], None] = '560e3434cc14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post_new', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key('posts_users_fkey',
                          source_table='post_new',
                          referent_table='users',
                          local_cols=['user_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE'
                        )
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', 'post_new', type_='foreignkey')
    op.drop_column('post_new', 'user_id')
    pass


#alembic revision --autogenerate -m "add vote table"