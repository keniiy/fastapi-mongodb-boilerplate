"""
Pytest configuration and fixtures.
Sets up test database, client, and common fixtures for MongoDB.
"""

import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

# Set test environment variables BEFORE importing app
os.environ["MONGODB_URL"] = os.getenv("TEST_MONGODB_URL", "mongodb://localhost:27017")
os.environ["MONGODB_DATABASE_NAME"] = "test_db"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-minimum-32-chars"
os.environ["DEBUG"] = "true"
os.environ["ENVIRONMENT"] = "test"
os.environ["RATE_LIMIT_ENABLED"] = "false"  # Disable rate limiting in tests

from app.app import app
from app.infrastructure.db.config import get_database, get_db


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db():
    """Create test database and clean up after"""
    from app.infrastructure.db.config import get_client, get_database

    client = get_client()
    db = get_database()
    db_name = os.getenv("MONGODB_DATABASE_NAME", "test_db")
    test_db_instance = client[db_name]

    yield test_db_instance

    # Clean up: drop all collections
    collections = await test_db_instance.list_collection_names()
    for collection_name in collections:
        await test_db_instance.drop_collection(collection_name)


@pytest.fixture(scope="function")
async def client(test_db) -> AsyncGenerator[AsyncClient, None]:
    """Create test HTTP client with dependency override"""

    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Sample user data for tests"""
    return {"email": "test@example.com", "password": "testpassword123"}


@pytest.fixture
def test_user_phone_data():
    """Sample user data with phone for tests"""
    return {"phone": "+1234567890", "password": "testpassword123"}
