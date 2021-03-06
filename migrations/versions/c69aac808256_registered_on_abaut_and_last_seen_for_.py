"""registered on, abaut and last_seen for User

Revision ID: c69aac808256
Revises: 9d037f0fa2d2
Create Date: 2021-06-26 11:58:07.092344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c69aac808256'
down_revision = '9d037f0fa2d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('registered_on', sa.Date(), nullable=True))
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    op.drop_column('user', 'registered_on')
    # ### end Alembic commands ###
