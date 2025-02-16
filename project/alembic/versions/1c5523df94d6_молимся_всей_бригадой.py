"""молимся всей бригадой

Revision ID: 1c5523df94d6
Revises: 9fc42594a97e
Create Date: 2025-01-25 00:50:07.418623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c5523df94d6'
down_revision: Union[str, None] = '9fc42594a97e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lesson_student')
    op.add_column('student', sa.Column('id_group', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'student', 's_group', ['id_group'], ['id'])
    op.add_column('student_group', sa.Column('student_id', sa.Integer(), nullable=False))
    op.add_column('student_group', sa.Column('group_id', sa.Integer(), nullable=False))
    op.drop_constraint('student_group_id_student_fkey', 'student_group', type_='foreignkey')
    op.drop_constraint('student_group_id_group_fkey', 'student_group', type_='foreignkey')
    op.create_foreign_key(None, 'student_group', 's_group', ['group_id'], ['id'])
    op.create_foreign_key(None, 'student_group', 'student', ['student_id'], ['id'])
    op.drop_column('student_group', 'id_student')
    op.drop_column('student_group', 'id_group')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student_group', sa.Column('id_group', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('student_group', sa.Column('id_student', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'student_group', type_='foreignkey')
    op.drop_constraint(None, 'student_group', type_='foreignkey')
    op.create_foreign_key('student_group_id_group_fkey', 'student_group', 's_group', ['id_group'], ['id'])
    op.create_foreign_key('student_group_id_student_fkey', 'student_group', 'student', ['id_student'], ['id'])
    op.drop_column('student_group', 'group_id')
    op.drop_column('student_group', 'student_id')
    op.drop_constraint(None, 'student', type_='foreignkey')
    op.drop_column('student', 'id_group')
    op.create_table('lesson_student',
    sa.Column('lesson_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], name='lesson_student_lesson_id_fkey'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name='lesson_student_student_id_fkey'),
    sa.PrimaryKeyConstraint('lesson_id', 'student_id', name='lesson_student_pkey')
    )
    # ### end Alembic commands ###
