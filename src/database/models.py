from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .connection import db

class Producer(db.Base):
    __tablename__ = 'producers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)
    contact = Column(String)
    products = relationship('Product', back_populates='producer')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Product(db.Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    producer_id = Column(Integer, ForeignKey('producers.id'))
    name = Column(String, nullable=False)
    category = Column(String)
    quantity = Column(Float)
    unit = Column(String)
    price = Column(Float)
    availability = Column(Boolean, default=True)
    metadata = Column(JSON)
    producer = relationship('Producer', back_populates='products')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MarketData(db.Base):
    __tablename__ = 'market_data'
    
    id = Column(Integer, primary_key=True)
    product_category = Column(String)
    price = Column(Float)
    market_location = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String)
    metadata = Column(JSON)