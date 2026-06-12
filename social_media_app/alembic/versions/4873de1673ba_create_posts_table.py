"""create posts table

Revision ID: 4873de1673ba
Revises: 
Create Date: 2026-06-12 17:37:33.348878

"""


#docs at
# https://alembic.sqlalchemy.org/en/latest/tutorial.html
#or 
# documentations, and at bottom ddl internals

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4873de1673ba'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts_alembic',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('published', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        #sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table('posts_alembic')
    pass



#alembic revision -m "create posts table"
#alembic upgrade 4873de1673ba

#for modifying the table, we can use
#alembic revision -m "add new column to posts table"
#and another similar file will be created, and we can add the new column in that file, and then run
#cmd:
#op.add_column('posts_alembic', sa.Column('new_column_name', sa.String(), nullable=True))
#alembic upgrade head (for upgrading to the latest version)

#for downgrading to the previous version, we can use
#alembic downgrade -1 (for downgrading to the previous version)