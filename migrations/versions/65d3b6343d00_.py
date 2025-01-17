"""empty message

Revision ID: 65d3b6343d00
Revises: 1cd4c4177403
Create Date: 2023-08-14 15:57:45.578551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65d3b6343d00'
down_revision = '1cd4c4177403'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_people', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('id_planets', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'people', ['id_people'], ['id'])
        batch_op.create_foreign_key(None, 'planets', ['id_planets'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('id_planets')
        batch_op.drop_column('id_people')

    # ### end Alembic commands ###
