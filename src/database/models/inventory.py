from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..config import Base

class ProductCategory(enum.Enum):
    HONEY = "honey"
    CHEESE = "cheese"
    WINE = "wine"
    OTHER = "other"

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)  # Custom product ID (e.g., HON-12345678)
    name = Column(String, nullable=False)
    category = Column(Enum(ProductCategory), nullable=False)
    subcategory = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="products")
    inventory_records = relationship("InventoryRecord", back_populates="product")

class InventoryRecord(Base):
    __tablename__ = "inventory_records"

    id = Column(Integer, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    action = Column(String, nullable=False)  # e.g., "new_entry", "update", "remove"
    quantity = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)

    # Relationships
    product = relationship("Product", back_populates="inventory_records")

class ProductLabel(Base):
    __tablename__ = "product_labels"

    id = Column(Integer, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"), unique=True, nullable=False)
    label_data = Column(String, nullable=False)  # JSON string containing label information
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)