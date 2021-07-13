"""Initial migration

Revision ID: e421475dba3c
Revises: 
Create Date: 2021-06-22 18:26:28.255632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e421475dba3c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('username', sa.String(length=120), nullable=True),
    sa.Column('first_name', sa.String(length=120), nullable=True),
    sa.Column('last_name', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('oauth_token', sa.String(length=200), nullable=True),
    sa.Column('oauth_token_secret', sa.String(length=200), nullable=True),
    sa.Column('bio', sa.String(length=250), nullable=True),
    sa.Column('avatar_filename', sa.String(length=100), nullable=True),
    sa.Column('avatar_uploaded', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_clients'))
    )
    op.create_index(op.f('ix_clients_email'), 'clients', ['email'], unique=True)
    op.create_index(op.f('ix_clients_username'), 'clients', ['username'], unique=True)
    op.create_table('blocked_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=50), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], name=op.f('fk_blocked_tokens_client_id_clients')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_blocked_tokens'))
    )
    op.create_table('cad_models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cad_model_id', sa.String(length=100), nullable=False),
    sa.Column('cad_model_name', sa.String(length=100), nullable=False),
    sa.Column('cad_model_height', sa.Float(precision=2), nullable=False),
    sa.Column('cad_model_width', sa.Float(precision=2), nullable=False),
    sa.Column('cad_model_length', sa.Float(precision=2), nullable=False),
    sa.Column('cad_model_material', sa.String(length=100), nullable=False),
    sa.Column('cad_model_mesh_percent', sa.Integer(), nullable=False),
    sa.Column('cad_model_visibility', sa.Boolean(), nullable=True),
    sa.Column('cad_model_creation_time', sa.DateTime(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], name=op.f('fk_cad_models_client_id_clients')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_cad_models'))
    )
    op.create_table('confirmations',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('expire_at', sa.Integer(), nullable=False),
    sa.Column('confirmed', sa.Boolean(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], name=op.f('fk_confirmations_client_id_clients')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_confirmations'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('confirmations')
    op.drop_table('cad_models')
    op.drop_table('blocked_tokens')
    op.drop_index(op.f('ix_clients_username'), table_name='clients')
    op.drop_index(op.f('ix_clients_email'), table_name='clients')
    op.drop_table('clients')
    # ### end Alembic commands ###