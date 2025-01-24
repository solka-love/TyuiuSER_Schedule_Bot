"""Add user_id column to student table

Revision ID: 85f4707639f2
Revises: 4104d90d67d2
Create Date: 2025-01-24 22:45:54.999451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85f4707639f2'
down_revision: Union[str, None] = '4104d90d67d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('user_id', sa.Integer(), nullable=False))
    op.add_column('student', sa.Column('username', sa.String(length=100), nullable=False))
    op.add_column('student', sa.Column('full_name', sa.String(length=200), nullable=False))
    op.alter_column('student', 'student_tag',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.alter_column('student', 'coins',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_unique_constraint(None, 'student', ['user_id'])
    op.drop_column('student', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('name', sa.VARCHAR(length=60), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'student', type_='unique')
    op.alter_column('student', 'coins',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('student', 'student_tag',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    op.drop_column('student', 'full_name')
    op.drop_column('student', 'username')
    op.drop_column('student', 'user_id')
    # ### end Alembic commands ###
