# Collector Agent Database Integration

This module handles the integration between the Collector Agent and the database. It provides functionality for:

- Storing collected market data
- Retrieving historical market data
- Updating product prices based on market trends
- Generating statistical reports

## Usage

```python
from collector.database_manager import CollectorDatabaseManager

# Initialize the database manager
db_manager = CollectorDatabaseManager()

# Save new market data
market_data = {
    'product_category': 'dairy',
    'price': 2.50,
    'market_location': 'Galicia Central Market',
    'source': 'market_api',
    'metadata': {
        'currency': 'EUR',
        'unit': 'liter'
    }
}
db_manager.save_market_data(market_data)

# Get latest market data for a category
latest_data = db_manager.get_latest_market_data('dairy')

# Get statistical information
stats = db_manager.get_product_stats('dairy')
```

## Configuration

Make sure to set the following environment variables:
- DATABASE_URL: Connection string for the PostgreSQL database

## Security Notes

- All database operations use connection pooling for efficiency
- Transactions are automatically managed with rollback support
- Sensitive data should be stored in encrypted format