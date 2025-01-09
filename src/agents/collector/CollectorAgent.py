from datetime import datetime
from typing import Dict, List, Optional
import uuid
from dataclasses import dataclass

@dataclass
class ProductLabel:
    product_id: str
    product_name: str
    category: str
    subcategory: str
    user_name: str
    timestamp: datetime
    quantity: float
    unit: str
    region: str

class CollectorAgent:
    def __init__(self):
        self.inventory = {}
        self.labels = {}
        self.processed_items_log = []
        
    def generate_product_id(self, category: str) -> str:
        """Generate a unique product ID based on category and UUID"""
        return f"{category[:3].upper()}-{str(uuid.uuid4())[:8]}"
    
    def validate_data(self, data: Dict) -> tuple[bool, Optional[str]]:
        """Validate incoming data for completeness"""
        required_fields = [
            'user_name', 'product_name', 'category', 
            'subcategory', 'quantity', 'unit', 'region'
        ]
        
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
                
        if not isinstance(data['quantity'], (int, float)) or data['quantity'] <= 0:
            return False, "Invalid quantity value"
            
        return True, None
    
    def create_label(self, data: Dict, product_id: str) -> ProductLabel:
        """Create a product label with all necessary information"""
        return ProductLabel(
            product_id=product_id,
            product_name=data['product_name'],
            category=data['category'],
            subcategory=data['subcategory'],
            user_name=data['user_name'],
            timestamp=datetime.now(),
            quantity=data['quantity'],
            unit=data['unit'],
            region=data['region']
        )
    
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
        
        # Create label
        label = self.create_label(data, product_id)
        
        # Update inventory
        category_key = f"{data['category']}/{data['subcategory']}"
        if category_key not in self.inventory:
            self.inventory[category_key] = []
        
        self.inventory[category_key].append({
            'product_id': product_id,
            'user_name': data['user_name'],
            'quantity': data['quantity'],
            'unit': data['unit'],
            'timestamp': datetime.now()
        })
        
        # Store label
        self.labels[product_id] = label
        
        # Log the processed item
        self.processed_items_log.append({
            'product_id': product_id,
            'action': 'new_entry',
            'timestamp': datetime.now(),
            'details': data
        })
        
        return {
            'status': 'success',
            'product_id': product_id,
            'message': 'Product successfully processed and labeled',
            'label': label
        }
    
    def get_inventory_summary(self) -> Dict:
        """Generate a summary of current inventory"""
        summary = {
            'total_products': sum(len(products) for products in self.inventory.values()),
            'categories': {}
        }
        
        for category_key, products in self.inventory.items():
            category, subcategory = category_key.split('/')
            if category not in summary['categories']:
                summary['categories'][category] = {}
            
            summary['categories'][category][subcategory] = {
                'product_count': len(products),
                'total_quantity': sum(p['quantity'] for p in products)
            }
        
        return summary
    
    def get_product_details(self, product_id: str) -> Optional[Dict]:
        """Retrieve detailed information about a specific product"""
        if product_id in self.labels:
            label = self.labels[product_id]
            return {
                'label': label,
                'history': [log for log in self.processed_items_log 
                           if log['product_id'] == product_id]
            }
        return None