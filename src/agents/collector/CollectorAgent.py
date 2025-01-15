from typing import Dict, Any, List, Optional
from datetime import datetime
from .database_manager import CollectorDatabaseManager
from ...database.models import Producer, Product, Inventory

class CollectorAgent:
    def __init__(self):
        self.db_manager = CollectorDatabaseManager()
        
    def validate_producer_data(self, data: Dict[str, Any]) -> None:
        """Validate producer data before database insertion"""
        required_fields = ['name', 'location']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'Missing required field: {field}')
        
        if not isinstance(data['name'], str) or not data['name'].strip():
            raise ValueError('Producer name must be a non-empty string')
            
    def validate_product_data(self, data: Dict[str, Any]) -> None:
        """Validate product data before database insertion"""
        required_fields = ['name', 'category', 'unit']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'Missing required field: {field}')
        
        if not isinstance(data['name'], str) or not data['name'].strip():
            raise ValueError('Product name must be a non-empty string')
            
    def add_producer(self, data: Dict[str, Any]) -> Producer:
        """Add a new producer to the system
        
        Args:
            data: Dictionary containing producer information
                - name: Producer's name (required)
                - location: Geographic location (required)
                - contact: Contact information (optional)
                - metadata: Additional data (optional)
        
        Returns:
            Producer object
        
        Raises:
            ValueError: If required fields are missing or invalid
        """
        self.validate_producer_data(data)
        return self.db_manager.add_producer(data)
    
    def add_product(self, data: Dict[str, Any], producer_id: int) -> Product:
        """Add a new product to the system
        
        Args:
            data: Dictionary containing product information
                - name: Product name (required)
                - category: Product category (required)
                - subcategory: Product subcategory (optional)
                - unit: Unit of measurement (required)
                - metadata: Additional data (optional)
            producer_id: ID of the producer
        
        Returns:
            Product object
        
        Raises:
            ValueError: If required fields are missing or invalid
        """
        self.validate_product_data(data)
        return self.db_manager.add_product(data, producer_id)
    
    def update_inventory(self, product_id: int, quantity: float, operation: str = 'add') -> Inventory:
        """Update product inventory
        
        Args:
            product_id: ID of the product
            quantity: Quantity to add/subtract/set
            operation: Type of operation ('add', 'subtract', or 'set')
        
        Returns:
            Updated Inventory object
        
        Raises:
            ValueError: If quantity is invalid or operation not supported
        """
        if quantity < 0 and operation != 'subtract':
            raise ValueError('Quantity must be non-negative')
            
        if operation not in ['add', 'subtract', 'set']:
            raise ValueError('Invalid operation. Must be add, subtract, or set')
            
        return self.db_manager.update_inventory(product_id, quantity, operation)
    
    def get_producer_inventory(self, producer_id: int) -> List[Dict[str, Any]]:
        """Get inventory status for all products of a producer
        
        Args:
            producer_id: ID of the producer
        
        Returns:
            List of dictionaries containing inventory information
        """
        return self.db_manager.get_producer_inventory(producer_id)
    
    def get_product_inventory(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Get inventory status for a specific product
        
        Args:
            product_id: ID of the product
        
        Returns:
            Dictionary containing inventory information or None if not found
        """
        return self.db_manager.get_product_inventory(product_id)
    
    def process_manager_instruction(self, instruction: Dict[str, Any]) -> Dict[str, Any]:
        """Process instructions from the Manager Agent
        
        Args:
            instruction: Dictionary containing manager instructions
                - action: Type of action ('add_producer', 'add_product', 'update_inventory')
                - data: Data for the action
        
        Returns:
            Dictionary containing the result of the operation
        
        Raises:
            ValueError: If instruction format is invalid
        """
        if 'action' not in instruction:
            raise ValueError('Missing action in manager instruction')
            
        action = instruction['action']
        data = instruction.get('data', {})
        
        if action == 'add_producer':
            producer = self.add_producer(data)
            return {'status': 'success', 'producer_id': producer.id}
            
        elif action == 'add_product':
            if 'producer_id' not in data:
                raise ValueError('Missing producer_id in product data')
            product = self.add_product(data, data['producer_id'])
            return {'status': 'success', 'product_id': product.id}
            
        elif action == 'update_inventory':
            if not all(k in data for k in ['product_id', 'quantity']):
                raise ValueError('Missing required fields in inventory update')
            inventory = self.update_inventory(
                data['product_id'],
                data['quantity'],
                data.get('operation', 'add')
            )
            return {
                'status': 'success',
                'product_id': inventory.product_id,
                'new_quantity': inventory.quantity
            }
            
        else:
            raise ValueError(f'Unknown action: {action}')
