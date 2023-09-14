"""empty message

Revision ID: 0ca88ac43663
Revises: 8ff277d0f361
Create Date: 2023-08-13 18:50:18.670646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ca88ac43663'
down_revision = '8ff277d0f361'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('description'),
    sa.UniqueConstraint('name')
    )
    op.drop_table('characters')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='characters_pkey'),
    sa.UniqueConstraint('description', name='characters_description_key'),
    sa.UniqueConstraint('name', name='characters_name_key')
    )
    op.drop_table('people')
    # ### end Alembic commands ###
