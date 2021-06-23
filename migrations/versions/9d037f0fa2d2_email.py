"""email

Revision ID: 9d037f0fa2d2
Revises: ca51fa6fade9
Create Date: 2021-06-23 11:58:05.946130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d037f0fa2d2'
down_revision = 'ca51fa6fade9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(length=120), nullable=True))
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###
