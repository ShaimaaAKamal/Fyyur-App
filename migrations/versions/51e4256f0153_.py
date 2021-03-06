"""empty message

Revision ID: 51e4256f0153
Revises: 394a38c7b6fd
Create Date: 2021-01-14 17:14:41.354753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51e4256f0153'
down_revision = '394a38c7b6fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shows', 'venue_name')
    op.drop_column('shows', 'artist_image_link')
    op.drop_column('shows', 'venue_image_link')
    op.drop_column('shows', 'artist_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('artist_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('shows', sa.Column('venue_image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=False))
    op.add_column('shows', sa.Column('artist_image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=False))
    op.add_column('shows', sa.Column('venue_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
