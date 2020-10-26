"""empty message

Revision ID: 4e5f75685df6
Revises: 
Create Date: 2020-10-16 10:00:55.611032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e5f75685df6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categorys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('summ', sa.DECIMAL(precision=20, scale=2), nullable=False),
    sa.Column('status', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=32), nullable=True),
    sa.Column('tel', sa.Integer(), nullable=True),
    sa.Column('addres', sa.String(length=128), nullable=True),
    sa.Column('meails_list', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('price', sa.DECIMAL(precision=20, scale=2), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('picture', sa.String(length=128), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categorys.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mail', sa.String(length=32), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('role', sa.String(length=32), nullable=False),
    sa.Column('orders_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['orders_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mail')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('meals')
    op.drop_table('orders')
    op.drop_table('categorys')
    # ### end Alembic commands ###