"""empty message

Revision ID: a5ef50182a07
Revises: 2fe28795daf0
Create Date: 2023-11-12 21:05:32.983348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5ef50182a07'
down_revision = '2fe28795daf0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_turma', schema=None) as batch_op:
        batch_op.add_column(sa.Column('professor_id', sa.UUID(), nullable=True))
        batch_op.create_foreign_key(None, 'tb_funcionario', ['professor_id'], ['pessoa_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_turma', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('professor_id')

    # ### end Alembic commands ###
