"""empty message

Revision ID: f41736a39872
Revises: c2c303810003
Create Date: 2020-09-06 17:43:01.303893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f41736a39872'
down_revision = 'c2c303810003'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('artist_image_link', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'artist_image_link')
    # ### end Alembic commands ###