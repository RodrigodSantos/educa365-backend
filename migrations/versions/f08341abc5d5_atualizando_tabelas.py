"""atualizando tabelas

Revision ID: f08341abc5d5
Revises: c2f9b95c5159
Create Date: 2023-09-17 22:21:29.225852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f08341abc5d5'
down_revision = 'c2f9b95c5159'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tbFuncionario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pessoaId', sa.Integer(), nullable=False))
        batch_op.create_unique_constraint(None, ['email'])
        batch_op.create_foreign_key(None, 'tbPessoa', ['pessoaId'], ['id'])
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tbFuncionario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"tbFuncionario_id_seq"\'::regclass)'), autoincrement=True, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('pessoaId')

    # ### end Alembic commands ###
