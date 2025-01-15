# Database Setup Instructions

## Prerequisites
1. Install MySQL Server
2. Install Python requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Setup Steps

1. Create the database and user:
   ```bash
   mysql -u root -p < scripts/setup_database.sql
   ```

2. Set up your environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. Initialize Alembic migrations:
   ```bash
   alembic init migrations
   ```

4. Generate initial migration:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

5. Run the migrations:
   ```bash
   alembic upgrade head
   ```

## Verify Setup

```python
from src.database.connection import db

# Test connection
with db.get_session() as session:
    # Run a simple query
    result = session.execute("SELECT 1").scalar()
    print(f"Connection successful: {result == 1}")
```

## Common Issues

1. Connection Refused:
   - Check if MySQL service is running
   - Verify credentials in .env file
   - Check host and port settings

2. Permission Denied:
   - Verify user privileges
   - Check database existence

3. Character Set Issues:
   - Database uses utf8mb4 encoding
   - Check table and column collations