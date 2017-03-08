"""empty message

Revision ID: 4f806ed85ef6
Revises: e9378af5bb49
Create Date: 2017-03-07 20:23:13.623734

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4f806ed85ef6'
down_revision = 'e9378af5bb49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('follows', sa.Column('create_time', sa.DateTime(), nullable=True))
    op.drop_column('follows', 'timestamp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('follows', sa.Column('timestamp', mysql.DATETIME(), nullable=True))
    op.drop_column('follows', 'create_time')
    # ### end Alembic commands ###