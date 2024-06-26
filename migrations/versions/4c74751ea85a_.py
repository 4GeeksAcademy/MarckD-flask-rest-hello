"""empty message

Revision ID: 4c74751ea85a
Revises: 4c18f054969b
Create Date: 2024-04-24 05:28:21.113324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c74751ea85a'
down_revision = '4c18f054969b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite__planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('planets_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('favorite__planet_User_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorite__planet_Planets_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'planets', ['planets_id'], ['id'])
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])
        batch_op.drop_column('User_id')
        batch_op.drop_column('Planets_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite__planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Planets_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('User_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favorite__planet_Planets_id_fkey', 'planets', ['Planets_id'], ['id'])
        batch_op.create_foreign_key('favorite__planet_User_id_fkey', 'user', ['User_id'], ['id'])
        batch_op.drop_column('planets_id')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
