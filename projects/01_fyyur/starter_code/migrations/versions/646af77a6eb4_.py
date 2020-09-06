"""empty message

Revision ID: 646af77a6eb4
Revises: da2b2b082289
Create Date: 2020-09-06 17:03:19.063157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '646af77a6eb4'
down_revision = 'da2b2b082289'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('start_time', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'start_time')
    # ### end Alembic commands ###