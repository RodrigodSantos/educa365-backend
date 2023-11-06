"""empty message

Revision ID: 6232bd1662c2
Revises: b0cf63b17a39
Create Date: 2023-11-06 10:03:04.344704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6232bd1662c2'
down_revision = 'b0cf63b17a39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_turma', schema=None) as batch_op:
        batch_op.add_column(sa.Column('instituicao_id', sa.UUID(), nullable=False))
        batch_op.create_foreign_key(None, 'tb_instituicao_ensino', ['instituicao_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_turma', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('instituicao_id')

    # ### end Alembic commands ###
