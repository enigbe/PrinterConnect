"""empty message

Revision ID: 737b85598330
Revises: 
Create Date: 2021-05-26 10:34:29.566698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '737b85598330'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clients', 'avatar_uploaded')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clients', sa.Column('avatar_uploaded', sa.BOOLEAN(), nullable=False))
    # ### end Alembic commands ###