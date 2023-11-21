"""empty message

Revision ID: 04d23503ddc8
Revises: 38b422b69de7
Create Date: 2023-11-17 08:52:14.787125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04d23503ddc8'
down_revision = '38b422b69de7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_relatorio', schema=None) as batch_op:
        batch_op.alter_column('educando_id',
               existing_type=sa.UUID(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_relatorio', schema=None) as batch_op:
        batch_op.alter_column('educando_id',
               existing_type=sa.UUID(),
               nullable=False)

    # ### end Alembic commands ###