from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from ..database.connection import db
from ..database.models import MarketData, Product, Producer

class CollectorDatabaseManager:
    def __init__(self):
        self.db = db
    
    def save_market_data(self, data: Dict[str, Any]) -> MarketData:
        """Save collected market data to the database"""
        with self.db.get_session() as session:
            market_data = MarketData(
                product_category=data['product_category'],
                price=data['price'],
                market_location=data['market_location'],
                source=data['source'],
                metadata=data.get('metadata', {})
            )
            session.add(market_data)
            session.commit()
            return market_data
    
    def get_latest_market_data(self, product_category: str, limit: int = 10) -> List[MarketData]:
        """Retrieve the latest market data for a specific product category"""
        with self.db.get_session() as session:
            return session.query(MarketData)\
                .filter(MarketData.product_category == product_category)\
                .order_by(desc(MarketData.timestamp))\
                .limit(limit)\
                .all()
    
    def update_product_prices(self, market_data: MarketData) -> None:
        """Update product prices based on new market data"""
        with self.db.get_session() as session:
            products = session.query(Product)\
                .filter(Product.category == market_data.product_category)\
                .all()
            
            for product in products:
                # Implement price update logic here
                # This could include market trends, seasonality, etc.
                product.metadata['last_market_price'] = market_data.price
                product.updated_at = datetime.utcnow()
            
            session.commit()
    
    def get_product_stats(self, product_category: str) -> Dict[str, Any]:
        """Get statistical information about products and market data"""
        with self.db.get_session() as session:
            market_data = session.query(MarketData)\
                .filter(MarketData.product_category == product_category)\
                .order_by(desc(MarketData.timestamp))\
                .limit(100)\
                .all()
            
            if not market_data:
                return {}
            
            prices = [data.price for data in market_data]
            return {
                'average_price': sum(prices) / len(prices),
                'max_price': max(prices),
                'min_price': min(prices),
                'data_points': len(prices),
                'latest_update': market_data[0].timestamp
            }