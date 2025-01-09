from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from datetime import datetime
import json

from ..models.inventory import Product, InventoryRecord, ProductLabel, ProductCategory

class CollectorCRUD:
    @staticmethod
    def create_product(db: Session, product_data: Dict) -> Product:
        """Create a new product entry"""
        product = Product(
            id=product_data['product_id'],
            name=product_data['product_name'],
            category=ProductCategory[product_data['category'].upper()],
            subcategory=product_data['subcategory'],
            user_id=product_data['user_id'],
            quantity=product_data['quantity'],
            unit=product_data['unit']
        )
        db.add(product)
        
        # Create initial inventory record
        inventory_record = InventoryRecord(
            product_id=product.id,
            action='new_entry',
            quantity=product_data['quantity'],
            notes='Initial product entry'
        )
        db.add(inventory_record)
        
        # Create product label
        label = ProductLabel(
            product_id=product.id,
            label_data=json.dumps({
                'product_id': product.id,
                'product_name': product.name,
                'category': product.category.value,
                'subcategory': product.subcategory,
                'user_id': product.user_id,
                'quantity': product.quantity,
                'unit': product.unit,
                'timestamp': datetime.utcnow().isoformat()
            })
        )
        db.add(label)
        
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_product(db: Session, product_id: str) -> Optional[Product]:
        """Retrieve a product by its ID"""
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def get_products_by_category(db: Session, category: ProductCategory) -> List[Product]:
        """Get all products in a specific category"""
        return db.query(Product).filter(Product.category == category).all()

    @staticmethod
    def update_product_quantity(db: Session, product_id: str, quantity: float, action: str) -> Product:
        """Update product quantity and create inventory record"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.quantity = quantity
            product.updated_at = datetime.utcnow()
            
            inventory_record = InventoryRecord(
                product_id=product_id,
                action=action,
                quantity=quantity,
                notes=f'Quantity updated to {quantity} {product.unit}'
            )
            db.add(inventory_record)
            
            db.commit()
            db.refresh(product)
        return product

    @staticmethod
    def get_inventory_summary(db: Session) -> Dict:
        """Generate inventory summary"""
        products = db.query(Product).all()
        
        summary = {
            'total_products': len(products),
            'categories': {}
        }
        
        for product in products:
            category = product.category.value
            if category not in summary['categories']:
                summary['categories'][category] = {}
            
            if product.subcategory not in summary['categories'][category]:
                summary['categories'][category][product.subcategory] = {
                    'product_count': 0,
                    'total_quantity': 0
                }
            
            cat_summary = summary['categories'][category][product.subcategory]
            cat_summary['product_count'] += 1
            cat_summary['total_quantity'] += product.quantity
        
        return summary

    @staticmethod
    def get_product_history(db: Session, product_id: str) -> List[InventoryRecord]:
        """Get the complete history of a product"""
        return db.query(InventoryRecord)\
            .filter(InventoryRecord.product_id == product_id)\
            .order_by(InventoryRecord.timestamp.desc())\
            .all()