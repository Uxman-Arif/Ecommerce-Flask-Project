"""usercreation

Revision ID: 6973bf68e42c
Revises: 5371a12a7e92
Create Date: 2025-01-13 09:10:42.170447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6973bf68e42c'
down_revision = '5371a12a7e92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=40), nullable=False),
    sa.Column('password', sa.String(length=400), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###