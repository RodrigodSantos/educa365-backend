"""empty message

Revision ID: 72c2ca55f92b
Revises: 8d078d0790a5
Create Date: 2023-11-01 09:12:38.370628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72c2ca55f92b'
down_revision = '8d078d0790a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_relatorio', schema=None) as batch_op:
        batch_op.alter_column('funcionario_id',
               existing_type=sa.UUID(),
               nullable=False)
        batch_op.alter_column('tipo',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('titulo',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_relatorio', schema=None) as batch_op:
        batch_op.alter_column('titulo',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('tipo',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('funcionario_id',
               existing_type=sa.UUID(),
               nullable=True)

    # ### end Alembic commands ###