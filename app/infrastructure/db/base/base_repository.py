"""
Abstract base repository for MongoDB with common CRUD operations.
Similar structure to SQL base_repository.py but using Motor/MongoDB queries.
"""

from abc import ABC
from datetime import datetime
from typing import Any, Generic, TypeVar

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.common.utils.pagination import PaginatedResponse, PaginationParams

# TypeVar for generic repository pattern
ModelType = TypeVar("ModelType")


class BaseRepository(ABC, Generic[ModelType]):
    """
    Abstract base repository with common MongoDB operations.

    Usage:
        class UserRepository(BaseRepository[User]):
            def __init__(self):
                super().__init__("users", User)
    """

    def __init__(self, collection_name: str, model_class: type):
        """
        Initialize repository with collection name and model class.

        Args:
            collection_name: MongoDB collection name (e.g., "users", "courses")
            model_class: Pydantic model class for serialization
        """
        self.collection_name = collection_name
        self.model_class = model_class

    def _get_collection(self, db: AsyncIOMotorDatabase):
        """Get MongoDB collection"""
        return db[self.collection_name]

    def _to_dict(self, obj: ModelType, exclude_id: bool = False) -> dict[str, Any]:
        """Convert model to dictionary"""
        if hasattr(obj, "model_dump"):
            data = obj.model_dump()
        elif hasattr(obj, "dict"):
            data = obj.dict()
        else:
            data = dict(obj)

        # Remove id field as MongoDB uses _id
        if exclude_id and "id" in data or "id" in data:
            data.pop("id")
        return data

    async def create(self, db: AsyncIOMotorDatabase, obj: ModelType) -> ModelType:
        """
        Create a new document in the database.

        Args:
            db: Database instance
            obj: Model instance to create

        Returns:
            Created model instance with generated _id
        """
        collection = self._get_collection(db)
        data = self._to_dict(obj, exclude_id=True)
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = None

        result = await collection.insert_one(data)
        created = await collection.find_one({"_id": result.inserted_id})
        return self._dict_to_model(created)

    async def get_by_id(self, db: AsyncIOMotorDatabase, id: str) -> ModelType | None:
        """
        Get a document by its _id.

        Args:
            db: Database instance
            id: Document _id (string)

        Returns:
            Model instance if found, None otherwise
        """
        collection = self._get_collection(db)
        try:
            doc = await collection.find_one({"_id": ObjectId(id)})
            return self._dict_to_model(doc) if doc else None
        except Exception:
            return None

    async def get_all(
        self,
        db: AsyncIOMotorDatabase,
        skip: int = 0,
        limit: int = 100,
        filter_dict: dict[str, Any] | None = None,
    ) -> list[ModelType]:
        """
        Get all documents with pagination.

        Args:
            db: Database instance
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            filter_dict: Optional filter dictionary

        Returns:
            List of model instances
        """
        collection = self._get_collection(db)
        filter_dict = filter_dict or {}
        cursor = collection.find(filter_dict).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [self._dict_to_model(doc) for doc in docs]

    async def get_all_paginated(
        self,
        db: AsyncIOMotorDatabase,
        pagination: PaginationParams,
        filter_dict: dict[str, Any] | None = None,
    ) -> PaginatedResponse[ModelType]:
        """
        Get all documents with pagination and metadata.
        Similar to SQL version.
        """
        total = await self.count(db, filter_dict)
        items = await self.get_all(
            db, skip=pagination.skip, limit=pagination.limit, filter_dict=filter_dict
        )

        from app.common.utils.pagination import PaginationMeta

        meta = PaginationMeta.create(
            total=total, page=pagination.page, page_size=pagination.page_size
        )

        return PaginatedResponse(items=items, meta=meta)

    async def update(
        self, db: AsyncIOMotorDatabase, id: str, update_data: dict[str, Any]
    ) -> ModelType | None:
        """
        Update a document.

        Args:
            db: Database instance
            id: Document _id
            update_data: Dictionary with fields to update

        Returns:
            Updated model instance
        """
        collection = self._get_collection(db)
        update_data["updated_at"] = datetime.utcnow()

        result = await collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

        if result.modified_count:
            updated = await collection.find_one({"_id": ObjectId(id)})
            return self._dict_to_model(updated)
        return None

    async def delete(self, db: AsyncIOMotorDatabase, id: str) -> bool:
        """
        Delete a document by _id.

        Args:
            db: Database instance
            id: Document _id

        Returns:
            True if deleted, False if not found
        """
        collection = self._get_collection(db)
        try:
            result = await collection.delete_one({"_id": ObjectId(id)})
            return result.deleted_count > 0
        except Exception:
            return False

    async def count(
        self, db: AsyncIOMotorDatabase, filter_dict: dict[str, Any] | None = None
    ) -> int:
        """
        Count documents.

        Args:
            db: Database instance
            filter_dict: Optional filter dictionary

        Returns:
            Total count
        """
        collection = self._get_collection(db)
        filter_dict = filter_dict or {}
        return await collection.count_documents(filter_dict)

    def _dict_to_model(self, doc: dict[str, Any] | None) -> ModelType | None:
        """Convert MongoDB document to model instance"""
        if not doc:
            return None
        # Convert _id to id
        if "_id" in doc:
            doc["id"] = str(doc["_id"])
            doc.pop("_id")
        return self.model_class(**doc)
