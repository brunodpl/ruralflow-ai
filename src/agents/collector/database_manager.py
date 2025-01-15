from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from ...database.connection import db
from ...database.models import Product, Producer, Inventory

class CollectorDatabaseManager:
    def __init__(self):
        self.db = db
    
    def add_producer(self, producer_data: Dict[str, Any]) -> Producer:
        """Add a new producer to the database"""
        with self.db.get_session() as session:
            producer = Producer(
                name=producer_data['name'],
                location=producer_data['location'],
                contact=producer_data.get('contact'),
                metadata=producer_data.get('metadata', {})
            )
            session.add(producer)
            session.commit()
            return producer
    
    def add_product(self, product_data: Dict[str, Any], producer_id: int) -> Product:
        """Add a new product to the database"""
        with self.db.get_session() as session:
            product = Product(
                producer_id=producer_id,
                name=product_data['name'],
                category=product_data['category'],
                subcategory=product_data.get('subcategory'),
                unit=product_data['unit'],
                metadata=product_data.get('metadata', {})
            )
            session.add(product)
            session.commit()
            return product
    
    def update_inventory(self, product_id: int, quantity: float, operation: str = 'add') -> Inventory:
        """Update inventory for a product"""
        with self.db.get_session() as session:
            inventory = session.query(Inventory).filter(Inventory.product_id == product_id).first()
            
            if not inventory:
                inventory = Inventory(product_id=product_id, quantity=0)
                session.add(inventory)
            
            if operation == 'add':
                inventory.quantity += quantity
            elif operation == 'subtract':
                inventory.quantity -= quantity
            elif operation == 'set':
                inventory.quantity = quantity
            
            inventory.last_updated = datetime.utcnow()
            session.commit()
            return inventory
    
    def get_product_inventory(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Get current inventory for a product"""
        with self.db.get_session() as session:
            inventory = session.query(Inventory).filter(Inventory.product_id == product_id).first()
            if inventory:
                return {
                    'product_id': inventory.product_id,
                    'quantity': inventory.quantity,
                    'last_updated': inventory.last_updated
                }
            return None
    
    def get_producer_inventory(self, producer_id: int) -> List[Dict[str, Any]]:
        """Get inventory for all products of a producer"""
        with self.db.get_session() as session:
            products = session.query(Product).filter(Product.producer_id == producer_id).all()
            inventory_list = []
            
            for product in products:
                inventory = session.query(Inventory).filter(Inventory.product_id == product.id).first()
                if inventory:
                    inventory_list.append({
                        'product_id': product.id,
                        'product_name': product.name,
                        'category': product.category,
                        'quantity': inventory.quantity,
                        'unit': product.unit,
                        'last_updated': inventory.last_updated
                    })
            
            return inventory_list