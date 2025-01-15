from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .connection import db

class Producer(db.Base):
    __tablename__ = 'producers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)
    contact = Column(String)
    metadata = Column(JSON)
    products = relationship('Product', back_populates='producer')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Product(db.Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    producer_id = Column(Integer, ForeignKey('producers.id'))
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    subcategory = Column(String)
    unit = Column(String, nullable=False)
    metadata = Column(JSON)
    producer = relationship('Producer', back_populates='products')
    inventory = relationship('Inventory', back_populates='product', uselist=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Inventory(db.Base):
    __tablename__ = 'inventory'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), unique=True)
    quantity = Column(Float, default=0)
    product = relationship('Product', back_populates='inventory')
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)