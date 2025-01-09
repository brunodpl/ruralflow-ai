import pytest
from datetime import datetime
from src.agents.collector.CollectorAgent import CollectorAgent

@pytest.fixture
def collector():
    return CollectorAgent()

@pytest.fixture
def sample_product_data():
    return {
        'user_name': 'María García',
        'product_name': 'Mountain Wildflower Honey',
        'category': 'Honey',
        'subcategory': 'Wildflower',
        'quantity': 50.0,
        'unit': 'kg',
        'region': 'Galicia'
    }

def test_data_validation(collector, sample_product_data):
    # Test valid data
    is_valid, error = collector.validate_data(sample_product_data)
    assert is_valid
    assert error is None
    
    # Test missing field
    invalid_data = sample_product_data.copy()
    del invalid_data['user_name']
    is_valid, error = collector.validate_data(invalid_data)
    assert not is_valid
    assert 'Missing required field' in error
    
    # Test invalid quantity
    invalid_data = sample_product_data.copy()
    invalid_data['quantity'] = -1
    is_valid, error = collector.validate_data(invalid_data)
    assert not is_valid
    assert 'Invalid quantity' in error

def test_product_processing(collector, sample_product_data):
    # Process new product
    result = collector.process_new_entry(sample_product_data)
    
    assert result['status'] == 'success'
    assert 'product_id' in result
    assert 'HON-' in result['product_id']  # Check ID format
    
    # Verify inventory update
    summary = collector.get_inventory_summary()
    assert summary['total_products'] == 1
    assert 'Honey' in summary['categories']
    assert 'Wildflower' in summary['categories']['Honey']
    
    # Check label creation
    product_details = collector.get_product_details(result['product_id'])
    assert product_details is not None
    assert product_details['label'].product_name == 'Mountain Wildflower Honey'
    assert product_details['label'].quantity == 50.0

def test_inventory_summary(collector, sample_product_data):
    # Add multiple products
    collector.process_new_entry(sample_product_data)
    
    modified_data = sample_product_data.copy()
    modified_data['quantity'] = 30.0
    collector.process_new_entry(modified_data)
    
    summary = collector.get_inventory_summary()
    honey_category = summary['categories']['Honey']['Wildflower']
    
    assert summary['total_products'] == 2
    assert honey_category['product_count'] == 2
    assert honey_category['total_quantity'] == 80.0  # 50 + 30