"""Add EquipmentHistory model

Revision ID: 5b7bc578c8b6
Revises: 2c7853298430
Create Date: 2025-04-16 14:36:05.840886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b7bc578c8b6'
down_revision = '2c7853298430'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('equipment_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('event', sa.String(length=255), nullable=False),
    sa.Column('equipment_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['equipment_id'], ['equipment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('equipment_history')
    # ### end Alembic commands ###
