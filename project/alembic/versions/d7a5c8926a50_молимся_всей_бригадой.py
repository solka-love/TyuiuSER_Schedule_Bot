"""молимся всей бригадой

Revision ID: d7a5c8926a50
Revises: 3461c46f2772
Create Date: 2025-01-25 00:43:56.038628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7a5c8926a50'
down_revision: Union[str, None] = '3461c46f2772'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lesson_student',
    sa.Column('lesson_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('lesson_id', 'student_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lesson_student')
    # ### end Alembic commands ###
