# Collector Agent

The Collector Agent is responsible for managing product intake and inventory organization in the RuralFlow AI system.

## Features

1. Data Validation
   - Ensures completeness of user and product information
   - Validates data types and values

2. Product Labeling
   - Generates unique product IDs
   - Creates detailed labels with all necessary metadata
   - Maintains a searchable label database

3. Inventory Management
   - Organizes products by category and subcategory
   - Tracks quantities and units
   - Maintains user associations

4. Logging and Tracking
   - Records all processed items
   - Maintains audit trail
   - Generates inventory summaries

## Usage Example

```python
# Initialize the Collector Agent
collector = CollectorAgent()

# Process a new product
result = collector.process_new_entry({
    'user_name': 'María García',
    'product_name': 'Mountain Wildflower Honey',
    'category': 'Honey',
    'subcategory': 'Wildflower',
    'quantity': 50.0,
    'unit': 'kg',
    'region': 'Galicia'
})

# Get inventory summary
summary = collector.get_inventory_summary()
```

## Data Structures

### Product Label
```python
@dataclass
class ProductLabel:
    product_id: str        # Unique identifier
    product_name: str      # Name of the product
    category: str         # Main category
    subcategory: str      # Subcategory
    user_name: str        # Producer name
    timestamp: datetime   # Entry timestamp
    quantity: float       # Product quantity
    unit: str            # Unit of measurement
    region: str          # Geographic region
```

## Error Handling

The agent provides detailed error messages for:
- Missing required fields
- Invalid data types
- Invalid quantities
- Unknown product IDs

## Integration

The Collector Agent is designed to work seamlessly with other RuralFlow AI agents, particularly the Manager Agent.