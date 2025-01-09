"""initial schema

Revision ID: 001
Revises: 
Create Date: 2024-01-09
"""
from alembic import op
import sqlalchemy as sa


def upgrade():
    # Create products table
    op.create_table(
        'products',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('category', sa.Enum('honey', 'cheese', 'wine', 'other', name='productcategory'), nullable=False),
        sa.Column('subcategory', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )

    # Create inventory_records table
    op.create_table(
        'inventory_records',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('product_id', sa.String(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('notes', sa.String()),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'])
    )

    # Create product_labels table
    op.create_table(
        'product_labels',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('product_id', sa.String(), nullable=False, unique=True),
        sa.Column('label_data', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'])
    )


def downgrade():
    op.drop_table('product_labels')
    op.drop_table('inventory_records')
    op.drop_table('products')
    op.execute('DROP TYPE productcategory')