"""empty message

Revision ID: b1d9a99d36b9
Revises: 270583fbbd79
Create Date: 2023-12-07 10:45:25.050383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1d9a99d36b9'
down_revision = '270583fbbd79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_turma', schema=None) as batch_op:
        batch_op.add_column(sa.Column('idade', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_turma', schema=None) as batch_op:
        batch_op.drop_column('idade')

    # ### end Alembic commands ###
