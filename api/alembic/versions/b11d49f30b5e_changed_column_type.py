"""Changed column type

Revision ID: b11d49f30b5e
Revises: 6c4b60de12d5
Create Date: 2024-03-05 11:36:17.592927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b11d49f30b5e'
down_revision: Union[str, None] = '6c4b60de12d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'links', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'links', type_='foreignkey')
    # ### end Alembic commands ###