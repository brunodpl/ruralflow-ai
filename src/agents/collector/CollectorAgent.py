from datetime import datetime
from typing import Dict, Optional
import uuid
from sqlalchemy.orm import Session

from ...database.crud.collector_crud import CollectorCRUD
from ...database.config import get_db

class CollectorAgent:
    def __init__(self):
        self.crud = CollectorCRUD()
    
    def generate_product_id(self, category: str) -> str:
        """Generate a unique product ID based on category and UUID"""
        return f"{category[:3].upper()}-{str(uuid.uuid4())[:8]}"
    
    def validate_data(self, data: Dict) -> tuple[bool, Optional[str]]:
        """Validate incoming data for completeness"""
        required_fields = [
            'user_id', 'product_name', 'category', 
            'subcategory', 'quantity', 'unit'
        ]
        
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
                
        if not isinstance(data['quantity'], (int, float)) or data['quantity'] <= 0:
            return False, "Invalid quantity value"
            
        return True, None
    
    def process_new_entry(self, data: Dict) -> Dict:
        """Process a new product entry"""
        # Validate data
        is_valid, error = self.validate_data(data)
        if not is_valid:
            return {
                'status': 'error',
                'message': error
            }
        
        # Generate product ID
        product_id = self.generate_product_id(data['category'])
        data['product_id'] = product_id
        
        try:
            # Get database session
            db = next(get_db())
            
            # Create product in database
            product = self.crud.create_product(db, data)
            
            return {
                'status': 'success',
                'product_id': product.id,
                'message': 'Product successfully processed and labeled'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Database error: {str(e)}'
            }
    
    def get_inventory_summary(self) -> Dict:
        """Generate a summary of current inventory"""
        try:
            db = next(get_db())
            return self.crud.get_inventory_summary(db)
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error getting inventory summary: {str(e)}'
            }
    
    def get_product_details(self, product_id: str) -> Optional[Dict]:
        """Retrieve detailed information about a specific product"""
        try:
            db = next(get_db())
            product = self.crud.get_product(db, product_id)
            if product:
                history = self.crud.get_product_history(db, product_id)
                return {
                    'product': product,
                    'history': history
                }
            return None
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error getting product details: {str(e)}'
            }