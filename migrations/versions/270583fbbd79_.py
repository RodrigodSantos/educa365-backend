"""empty message

Revision ID: 270583fbbd79
Revises: c3868695d7bf
Create Date: 2023-11-21 11:50:27.353896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '270583fbbd79'
down_revision = 'c3868695d7bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_blacklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('exp', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_blacklist')
    # ### end Alembic commands ###
