"""empty message

Revision ID: 0b570f598d1a
Revises: 45dad174ab95
Create Date: 2017-02-28 15:15:11.815291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b570f598d1a'
down_revision = '45dad174ab95'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column(
        'category_id', sa.Integer(), nullable=True))
    op.add_column('posts', sa.Column(
        'photo', sa.String(length=100), nullable=True))
    op.create_foreign_key(None, 'posts', 'categories', ['category_id'], ['id'])
    with op.batch_alter_table('posts') as batch_op:
        # batch_op.create_foreign_key(None, 'posts', 'categories', ['category_id'], ['id'])
        batch_op.drop_column('body')
    # op.create_foreign_key(None, 'posts', 'categories', ['category_id'], ['id'])
    # op.drop_column('posts', 'body')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body', sa.TEXT(), nullable=True))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'photo')
    op.drop_column('posts', 'category_id')
    # ### end Alembic commands ###
