"""
MongoDB database configuration and connection management.
Similar structure to SQL database.py but using Motor (async MongoDB driver).
"""

import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Global MongoDB client
client: AsyncIOMotorClient = None
database: AsyncIOMotorDatabase = None


def get_client() -> AsyncIOMotorClient:
    """Get MongoDB client (singleton pattern)"""
    global client
    if client is None:
        mongodb_url = settings.mongodb_url
        client = AsyncIOMotorClient(
            mongodb_url,
            serverSelectionTimeoutMS=5000,
            maxPoolSize=settings.mongodb_pool_size,
        )
    return client


def get_database() -> AsyncIOMotorDatabase:
    """Get MongoDB database instance"""
    global database
    if database is None:
        db_name = settings.mongodb_database_name
        database = get_client()[db_name]
    return database


async def get_db():
    """
    Get MongoDB database (dependency injection for FastAPI)
    Similar to get_db() in SQL version
    """
    yield get_database()


async def check_database_connection() -> tuple[bool, str]:
    """Check MongoDB connection and return status"""
    try:
        # Ping the server
        await get_client().admin.command("ping")
        return True, "connected"
    except ServerSelectionTimeoutError as e:
        return False, f"Connection timeout: {str(e)}"
    except Exception as e:
        return False, str(e)


async def init_db():
    """
    Initialize MongoDB connection and create indexes.
    Similar to init_db() in SQL version but creates indexes instead of tables.
    """
    is_connected, connection_msg = await check_database_connection()

    if is_connected:
        logger.info("MongoDB: Connected successfully")
        try:
            # Import models to register indexes
            from app.infrastructure.db.user.model import User  # noqa: F401

            # Create indexes
            db = get_database()
            # User collection indexes
            await db.users.create_index("email", unique=True, sparse=True)
            await db.users.create_index("phone", unique=True, sparse=True)
            await db.users.create_index("created_at")

            logger.info("MongoDB: Indexes initialized successfully")
        except Exception as e:
            logger.warning(f"MongoDB: Failed to create indexes: {e}")
    else:
        logger.warning(
            f"MongoDB: Connection failed - {connection_msg}. "
            "App will start but database operations will fail."
        )


async def close_db():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        client = None
