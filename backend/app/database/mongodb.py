"""
MongoDB async client using Motor.
Handles connection lifecycle, collection access, and index creation.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING
from loguru import logger
from app.config import settings

# Module-level client and database references
_client: AsyncIOMotorClient | None = None
_database: AsyncIOMotorDatabase | None = None

DATABASE_NAME = "resume_analyzer"


async def connect_db() -> None:
    """Create Motor client and connect to MongoDB Atlas."""
    global _client, _database
    try:
        _client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            maxPoolSize=10,
            minPoolSize=1,
            serverSelectionTimeoutMS=5000
        )
        _database = _client[DATABASE_NAME]
        # Verify connection with a ping
        await _client.admin.command("ping")
        logger.info(f"Connected to MongoDB Atlas database: {DATABASE_NAME}")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def disconnect_db() -> None:
    """Close the Motor client connection."""
    global _client, _database
    if _client:
        _client.close()
        _client = None
        _database = None
        logger.info("Disconnected from MongoDB")


def get_database() -> AsyncIOMotorDatabase:
    """Return the active database instance."""
    if _database is None:
        raise RuntimeError("Database not connected. Call connect_db() first.")
    return _database


def get_collection(name: str):
    """Return a collection reference by name."""
    db = get_database()
    return db[name]


async def create_indexes() -> None:
    """Create database indexes for optimal query performance."""
    db = get_database()
    try:
        # Users collection: unique email index
        await db.users.create_index(
            [("email", ASCENDING)],
            unique=True,
            name="idx_users_email"
        )
        logger.info("Created index: users.email (unique)")

        # Resumes collection: user_id index for fast lookups
        await db.resumes.create_index(
            [("user_id", ASCENDING)],
            name="idx_resumes_user_id"
        )
        await db.resumes.create_index(
            [("user_id", ASCENDING), ("uploaded_at", DESCENDING)],
            name="idx_resumes_user_uploaded"
        )
        logger.info("Created indexes: resumes.user_id, resumes.user_id+uploaded_at")

        # Analyses collection: compound index for user history queries
        await db.analyses.create_index(
            [("user_id", ASCENDING), ("created_at", DESCENDING)],
            name="idx_analyses_user_created"
        )
        await db.analyses.create_index(
            [("resume_id", ASCENDING)],
            name="idx_analyses_resume_id"
        )
        logger.info("Created indexes: analyses.user_id+created_at, analyses.resume_id")

    except Exception as e:
        logger.error(f"Error creating indexes: {e}")
        raise
