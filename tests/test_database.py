"""
Tests for database module.
"""
import pytest
import os
import sys
import asyncio

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

# Set test database path
os.environ["DB_PATH"] = "test_data/test_database.sqlite3"


def cleanup_test_db():
    """Cleanup test database."""
    db_path = os.environ.get("DB_PATH", "test_data/test_database.sqlite3")
    if os.path.exists(db_path):
        os.remove(db_path)
    db_dir = os.path.dirname(db_path)
    if os.path.exists(db_dir) and not os.listdir(db_dir):
        os.rmdir(db_dir)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Setup and teardown for each test."""
    yield
    cleanup_test_db()


def test_init_db():
    """Test database initialization."""
    from database import init_db, DB_PATH
    
    asyncio.run(init_db())
    assert os.path.exists(DB_PATH)


def test_save_lead():
    """Test saving a lead."""
    from database import save_lead, init_db
    
    async def run_test():
        await init_db()
        lead_id = await save_lead(
            user_id=123456789,
            username="testuser",
            answers=["Иван", "IT", "Рост продаж", "100k", "1 месяц", "да, example.com", "@testuser"]
        )
        return lead_id
    
    lead_id = asyncio.run(run_test())
    
    assert lead_id is not None
    assert lead_id > 0


def test_get_leads_count():
    """Test getting leads count."""
    from database import save_lead, get_leads_count, init_db
    
    async def run_test():
        await init_db()
        initial_count = await get_leads_count()
        
        await save_lead(
            user_id=111,
            username="user1",
            answers=["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
        )
        
        await save_lead(
            user_id=222,
            username="user2",
            answers=["B1", "B2", "B3", "B4", "B5", "B6", "B7"]
        )
        
        final_count = await get_leads_count()
        return initial_count, final_count
    
    initial_count, final_count = asyncio.run(run_test())
    assert final_count == initial_count + 2
