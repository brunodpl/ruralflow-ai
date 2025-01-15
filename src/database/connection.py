from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import os

class DatabaseConnection:
    def __init__(self):
        # MySQL connection string format: mysql+pymysql://username:password@host:port/database_name
        self.DATABASE_URL = os.getenv(
            'DATABASE_URL',
            'mysql+pymysql://root:password@localhost:3306/ruralflow'
        )
        
        # Create engine with MySQL-specific configuration
        self.engine = create_engine(
            self.DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,  # Recycle connections after 30 minutes
            pool_pre_ping=True,  # Enable connection health checks
            # MySQL specific settings
            connect_args={
                'charset': 'utf8mb4',  # Support full Unicode character set
                'connect_timeout': 30,  # Connection timeout in seconds
            }
        )
        
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False
        )
        
        self.Base = declarative_base()
    
    def create_tables(self):
        """Create all tables in the database"""
        self.Base.metadata.create_all(bind=self.engine)
    
    @contextmanager
    def get_session(self) -> Session:
        """Get a database session with automatic cleanup"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

# Create a single instance of DatabaseConnection
db = DatabaseConnection()