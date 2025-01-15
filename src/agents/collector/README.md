# Collector Agent

The Collector Agent is responsible for managing product intake and inventory organization in the RuralFlow AI system.

## Components

### 1. CollectorAgent (CollectorAgent.py)
- Main agent implementation
- Handles product intake processing
- Manages inventory organization
- Validates data
- Generates product labels
- Interacts with other agents

### 2. Database Manager (database_manager.py)
- Manages database operations
- Handles producer and product records
- Tracks inventory levels
- Provides inventory queries and updates

## Database Schema

### Producers
- id: Primary key
- name: Producer name
- location: Geographic location
- contact: Contact information
- metadata: Additional producer data

### Products
- id: Primary key
- producer_id: Foreign key to producers
- name: Product name
- category: Product category
- subcategory: Product subcategory
- unit: Unit of measurement
- metadata: Additional product data

### Inventory
- id: Primary key
- product_id: Foreign key to products
- quantity: Current quantity
- last_updated: Last update timestamp

## Usage Example

```python
from collector.CollectorAgent import CollectorAgent

# Initialize the agent
agent = CollectorAgent()

# Add a new producer
producer_data = {
    'name': 'María García',
    'location': 'Lugo, Galicia',
    'contact': '+34 600 000 000'
}
producer = agent.add_producer(producer_data)

# Add a new product
product_data = {
    'name': 'Mountain Wildflower Honey',
    'category': 'Honey',
    'subcategory': 'Wildflower',
    'unit': 'kg',
    'metadata': {
        'origin': 'Mountain range',
        'harvest_season': 'Summer 2024'
    }
}
product = agent.add_product(product_data, producer.id)

# Update inventory
agent.update_inventory(product.id, quantity=50.0)

# Get inventory status
inventory = agent.get_producer_inventory(producer.id)
```

## Error Handling

The agent provides detailed error messages for:
- Missing required fields
- Invalid data types
- Database operation failures
- Invalid inventory operations

## Security

- All database operations use connection pooling
- Transactions are automatically managed with rollback support
- Input validation before database operations
- Audit trail through timestamps