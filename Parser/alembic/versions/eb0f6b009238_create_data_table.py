"""create data table

Revision ID: eb0f6b009238
Revises: 
Create Date: 2019-10-05 18:51:28.334680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb0f6b009238'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'info',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(50), nullable=False),
        sa.Column('address', sa.String(100), nullable=True),
        sa.Column('phone', sa.String(25), nullable=True),
        sa.Column('email', sa.String(50), nullable=True),
        sa.Column('link', sa.String(50), nullable=True),
        sa.Column('timetable', sa.String(255), nullable=True),
        sa.Column('review', sa.String(25), nullable=False),
        sa.Column('about', sa.Text, nullable=True),
        sa.Column('imgLink', sa.String(50), nullable=False),
    )


def downgrade():
    op.drop_table('info')
