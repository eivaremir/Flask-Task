"""empty message

Revision ID: 7834db2e3d14
Revises: 
Create Date: 2020-07-27 07:38:29.992205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7834db2e3d14'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'updated_at')
    # ### end Alembic commands ###
