"""empty message

Revision ID: 66329b17192a
Revises: 33d45a6d8651
Create Date: 2021-05-29 10:17:47.161706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66329b17192a'
down_revision = '33d45a6d8651'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blocked_tokens', sa.Column('client_id', sa.Integer(), nullable=False))
    op.create_foreign_key(op.f('fk_blocked_tokens_client_id_clients'), 'blocked_tokens', 'clients', ['client_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_blocked_tokens_client_id_clients'), 'blocked_tokens', type_='foreignkey')
    op.drop_column('blocked_tokens', 'client_id')
    # ### end Alembic commands ###