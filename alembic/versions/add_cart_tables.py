# alembic/versions/add_cart_tables.py
# Migración para crear tablas de productos, carritos y items

"""
Migración Alembic para crear las tablas de productos, carritos y items.
Define los cambios en la base de datos para KickShopping.
"""

"""add cart tables

Revision ID: 0001
Revises: 
Create Date: 2025-09-15

"""
from alembic import op  # Operaciones de migración
import sqlalchemy as sa  # Tipos y utilidades de SQLAlchemy

# Identificadores de la migración
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """
    Crea las tablas 'products', 'carts' y 'cart_items' en la base de datos.
    """
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nombre', sa.String, nullable=False, unique=True),
        sa.Column('descripcion', sa.String),
        sa.Column('precio', sa.Float, nullable=False)
    )
    op.create_table(
        'carts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.String, nullable=False, unique=True)
    )
    op.create_table(
        'cart_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('cart_id', sa.Integer, sa.ForeignKey('carts.id')),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id')),
        sa.Column('cantidad', sa.Integer, default=1)
    )

def downgrade():
    """
    Elimina las tablas creadas por esta migración.
    """
    op.drop_table('cart_items')
    op.drop_table('carts')
    op.drop_table('products')
