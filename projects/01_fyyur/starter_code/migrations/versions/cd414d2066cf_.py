"""empty message

Revision ID: cd414d2066cf
Revises: 50fe23b1080a
Create Date: 2020-09-06 15:45:06.203125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd414d2066cf'
down_revision = '50fe23b1080a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('artist_id', sa.Integer(), nullable=False))
    op.add_column('Show', sa.Column('start_time', sa.DateTime(), nullable=False))
    op.add_column('Show', sa.Column('venue_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Show', 'Artist', ['artist_id'], ['id'])
    op.create_foreign_key(None, 'Show', 'Venue', ['venue_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Show', type_='foreignkey')
    op.drop_constraint(None, 'Show', type_='foreignkey')
    op.drop_column('Show', 'venue_id')
    op.drop_column('Show', 'start_time')
    op.drop_column('Show', 'artist_id')
    # ### end Alembic commands ###
