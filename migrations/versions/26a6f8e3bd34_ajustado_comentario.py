"""ajustado comentario

Revision ID: 26a6f8e3bd34
Revises: e40cb6999b0a
Create Date: 2023-12-10 01:38:40.687467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26a6f8e3bd34'
down_revision = 'e40cb6999b0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_comentario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('relatorio_id', sa.UUID(), nullable=False))
        batch_op.create_foreign_key(None, 'tb_relatorio', ['relatorio_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_comentario', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('relatorio_id')

    # ### end Alembic commands ###
