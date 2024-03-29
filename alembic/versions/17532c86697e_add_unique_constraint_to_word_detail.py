"""Add unique constraint to word_detail

Revision ID: 17532c86697e
Revises: 9d3a14be03e9
Create Date: 2024-02-15 21:20:41.111016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17532c86697e'
down_revision: Union[str, None] = '9d3a14be03e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_word_detail_uniqueness', 'words_details', ['word_id', 'part_of_speech_id', 'origin_id', 'meaning'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_word_detail_uniqueness', 'words_details', type_='unique')
    # ### end Alembic commands ###
